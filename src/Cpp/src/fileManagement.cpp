/*
    Read txt, csv, functions to skip comments

*/

/**
 * @brief Abstract class to open, read and write files
 * 
 */
class FileManager
{
    public:
        virtual ~FileManager(){};
        // bool getNamesDefined() = 0; -> returns True if namesDefined is true: i.e. if the first line contains column names
        // void appendColumn(vector<double>& columnVector, const char * columnName = "");
        // void getColumn(int index, vector<double>& dataVector);   -> fill data vector with column values  
        //

    protected:
        int nCommentLines();    // returns the number of comment lines

}

class TxtManager: public FileManager
{


}