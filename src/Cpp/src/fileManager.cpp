/*
    Implementation of FileManager
    Read txt, csv, functions to skip comments
*/

#include <Riostream.h>
#include <string>
#include <fstream>
#include <filesystem>

#include "fileManager.hpp"

FileManager::FileManager(const char * filePath)
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