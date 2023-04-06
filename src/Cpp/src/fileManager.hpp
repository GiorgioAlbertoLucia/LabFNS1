/*
    Read txt, csv, functions to skip comments
*/

#ifndef FILEMANAGER_H
#define FILEMANAGER_H

#include <string>

/**
 * @brief Class to open, read and write files
 * 
 */
class FileManager
{
    public:
        FileManager(const char * filePath);
        FileManager(std::string filePath);
        ~FileManager(){};
        
        // bool getNamesDefined() = 0; -> returns True if namesDefined is true: i.e. if the first line contains column names
        // void appendColumn(vector<double>& columnVector, const char * columnName = "");
        // void getColumn(int index, vector<double>& dataVector);   -> fill data vector with column values  
        //

        // getColumn
        // operator[] (with int and const char)
        // addColumn

        int getNCommentLines() const  {return FileManager::fNCommentLines;};
        int getNRows() const          {return FileManager::fNRows;};
        int getNColumns() const       {return FileManager::fNColumns;};

        void print() const;

    protected:
        int nCommentLines() const;      // returns the number of comment lines
        int nRows() const;              // returns the number of rows (non-comments)
        int nColumns() const;           // returns the number of columns

        void fillNamesArray();          // initializes column names array
        void uploadData();              // upload data from file to fData matrix

    private:
        std::string fFilePath;          // path to file
        std::string fExtension;         // file extension

        int fNCommentLines;
        int fNRows;
        int fNColumns;
        std::string *fDataNames;        // column names
        double **fData;                 // stored data (2-dim array)

};

#endif
