/*
    Implementation of FileManager
    Read txt, csv, functions to skip comments
*/

#include <Riostream.h>
#include <string>
#include <fstream>
#include <filesystem>

#include "fileManager.hpp"


/*
    PUBLIC
*/

/**
 * @brief Return column of the dataset, selecting it by its column name.
 * 
 * @param columnName 
 * @return double* 
 */
double * FileManager::getColumn(const char * columnName) const
{
    int index = 0;
    while(index < FileManager::fNColumns)
    {
        if(FileManager::fDataNames[index] == columnName)   return FileManager::getColumn(index);
        index++;
    }
    std::cerr << "Column not found." << std::endl;
    return FileManager::getColumn(-1);
}

/**
 * @brief Append a column to the existing dataset. This will NOT automatically added to the file.
 * 
 * @param column 
 * @param columnName 
 */
void FileManager::addColumn(double * column, const char * columnName)
{
    // create backup
    const int size = FileManager::fNColumns;
    std::string tempName[size];
    double temp[FileManager::fNColumns][FileManager::fNRows];

    for(int col=0; col<FileManager::fNColumns; col++)
    {
        tempName[col] = FileManager::fDataNames[col];
        for(int row=0; row<FileManager::fNRows; row++)  temp[col][row] = FileManager::fData[col][row];
    }

    // update
    FileManager::fNColumns++;
    delete []FileManager::fDataNames;
    FileManager::fDataNames = new std::string[FileManager::fNColumns];
    
    for(int i=0; i<size; i++)   FileManager::fDataNames[i] = tempName[i];
    FileManager::fDataNames[size] = columnName;

    for(int col=0; col<FileManager::fNColumns-1; col++) delete []FileManager::fData[col];
    delete []FileManager::fData;
    FileManager::fData = new double * [FileManager::fNColumns];
    for(int col=0; col<FileManager::fNColumns; col++) FileManager::fData[col] = new double[FileManager::fNRows];

    for(int col=0; col<size; col++) for(int row=0; row<FileManager::fNRows; row++)  fData[col][row] = temp[col][row];
    for(int row=0; row<FileManager::fNRows; row++)  fData[size][row] = column[row];
}

/**
 * @brief Append a column to the existing dataset. This will NOT automatically added to the file.
 * 
 * @param column 
 * @param columnName 
 */
void FileManager::addColumn(std::vector<double>& column, const char * columnName)
{
    // create backup
    const int size = FileManager::fNColumns;
    std::string tempName[size];

    double temp[FileManager::fNColumns][FileManager::fNRows];
    for(int col=0; col<FileManager::fNColumns; col++)
    {
        for(int row=0; row<FileManager::fNRows; row++)  temp[col][row] = FileManager::fData[col][row];
    }

    // update
    FileManager::fNColumns++;
    delete []FileManager::fDataNames;
    FileManager::fDataNames = new std::string[FileManager::fNColumns];
    
    for(int i=0; i<size; i++)   FileManager::fDataNames[i] = tempName[i];
    FileManager::fDataNames[size] = columnName;

    for(int col=0; col<FileManager::fNColumns-1; col++) delete []FileManager::fData[col];
    delete []FileManager::fData;
    FileManager::fData = new double * [FileManager::fNColumns];
    for(int col=0; col<FileManager::fNColumns; col++) FileManager::fData[col] = new double[FileManager::fNRows];

    for(int col=0; col<size; col++) for(int row=0; row<FileManager::fNRows; row++)  fData[col][row] = temp[col][row];
    for(int row=0; row<FileManager::fNRows; row++)  fData[size][row] = column[row];
}

/**
 * @brief Print column names and content of the file.
 * 
 */
void FileManager::print() const
{
    for(int col=0; col<FileManager::fNColumns; col++)   std::cout << FileManager::fDataNames[col] << " ";
    std::cout << std::endl;

    for(int row=0; row<FileManager::fNRows; row++)
    {
        for(int col=0; col<FileManager::fNColumns; col++)
        {
            std::cout << FileManager::fData[col][row] << " ";
        }
        std::cout << std::endl;
    }
}

/**
 * @brief Overloads the file and writes in all currently stored data (comments are not overloaded).
 * 
 */
void FileManager::update() const
{
    std::string comments[FileManager::fNCommentLines];

    std::fstream reader(FileManager::fFilePath, std::ios::in);
    for(int i=0; i<FileManager::fNCommentLines; i++)    getline(reader, comments[i]);
    reader.close();

    std::fstream writer(FileManager::fFilePath, std::ios::out);
    for(int i=0; i<FileManager::fNCommentLines; i++)    writer << comments[i] << "\n";

    for(int col=0; col<FileManager::fNColumns; col++)   
    {
        if(col != FileManager::fNColumns-1) writer << FileManager::fDataNames[col] << " ";
        else                                writer << FileManager::fDataNames[col] << "\n";
    }

    for(int row=0; row<FileManager::fNRows; row++)
    {
        for(int col=0; col<FileManager::fNColumns; col++)   
        {
            if(col != FileManager::fNColumns-1) writer << FileManager::fData[col][row] << " ";
            else                                writer << FileManager::fData[col][row];
        }
        if(row != FileManager::fNRows-1)    writer << "\n";
    }

    writer.close();
}

/**
 * @brief Initialize all data member with informations and content of a given file.
 * 
 * @param filePath 
 */
void FileManager::open(const char * filePath)
{
    FileManager::fFilePath = std::string(filePath);
    FileManager::fExtension = FileManager::fFilePath.substr(FileManager::fFilePath.find_last_of(".") + 1);

    FileManager::fNCommentLines = FileManager::nCommentLines();
    FileManager::fNRows = FileManager::nRows();
    FileManager::fNColumns = FileManager::nColumns();

    FileManager::fillNamesArray();
    FileManager::uploadData();
}

/**
 * @brief Deletes all dynamically allocated variables and sets all data member to default values.
 * 
 */
void FileManager::close()
{
    delete[] FileManager::fDataNames;
    
    for(int col=0; col<FileManager::fNColumns; col++)   delete[] FileManager::fData[col];
    delete[] FileManager::fData;

    FileManager::fNColumns = 0;
    FileManager::fNRows = 0;
    FileManager::fNCommentLines = 0;

    FileManager::fFilePath = std::string("_no_file.txt");
}

/*
    PROTECTED
*/

/**
 * @brief Upload data from file to a 2-dimensional array.
 * 
 */
void FileManager::uploadData()
{
    std::ifstream streamer(FileManager::fFilePath.c_str());
    std::string line;
    double val;
    for(int i=0; i<FileManager::fNCommentLines+1; i++)  getline(streamer, line);    // skip comments and column names

    FileManager::fData = new double*[FileManager::fNColumns];
    for(int col=0; col<FileManager::fNColumns; col++) FileManager::fData[col] = new double[FileManager::fNRows];

    for(int row=0; row<FileManager::fNRows; row++)
    {
        for(int col=0; col<FileManager::fNColumns; col++)
        {
            streamer >> val;
            FileManager::fData[col][row] = val;
        }
    }
    streamer.close();
}

/**
 * @brief Function to store the names of the columns in an array.
 * 
 */
void FileManager::fillNamesArray()
{
    std::ifstream streamer(FileManager::fFilePath.c_str());
    std::string line, val;
    for(int i=0; i<FileManager::fNCommentLines; i++)  getline(streamer, line);      // skip comments

    FileManager::fDataNames = new std::string[FileManager::fNColumns];

    int i=0;
    while(streamer.peek() != '\n' && streamer >> val)   
    {
        fDataNames[i] = val;
        i++;
    }
    streamer.close();
}

/**
 * @brief Function to return the number of columns in the file.
 * 
 * @return const int 
 */
int FileManager::nColumns() const
{
    std::ifstream streamer(FileManager::fFilePath.c_str());
    std::string line;
    double val;
    int columns = 0;

    // first line is reserved for column names
    for(int i=0; i<FileManager::fNCommentLines+1; i++)  getline(streamer, line);
    while(streamer.peek() != '\n' && streamer >> val)   ++columns;
    streamer.close();

    return columns;
}

/**
 * @brief Function to return the number of lines in the file (non-comments).
 * 
 * @return const int 
 */
int FileManager::nRows() const
{
    std::ifstream streamer(FileManager::fFilePath.c_str());
    std::string line;
    int rows = 0;

    while(getline(streamer, line))  rows++;
    streamer.close();

    // first non-comment line is reserved for names of the variables stored
    return rows - FileManager::fNCommentLines - 1;
}

/**
 * @brief Function to return the number of comment (or empty) lines in the chosen file. Comment lines begin with "#".
 * 
 * @return int 
 */
int FileManager::nCommentLines() const
{
    std::ifstream streamer(FileManager::fFilePath.c_str());
    std::string line;
    int commentLines = 0;

    while(getline(streamer, line))  if(line.empty() || line.at(0) == '#')   commentLines++;
    streamer.close();

    return commentLines;
}