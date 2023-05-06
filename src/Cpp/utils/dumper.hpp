#include <Riostream.h>
#include <string>

class Dumper
{
    public:
        Dumper(){};
        Dumper(const char * filePath, const char * outputPath);
        ~Dumper(){};

        const int getSize() const;
        void printSize() const;
        void testPrint() const;
        void readToTxt() const;
        void readData(int nbytes) const;


    private:
        std::string fFilePath;
        std::string fOutputPath;
};