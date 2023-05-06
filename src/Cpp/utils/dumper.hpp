#include <Riostream.h>
#include <string>
#include <vector>
#include <format>

class Dumper
{
    public:
        Dumper(){};
        Dumper(const char * filePath, const char * outputPath);
        ~Dumper();

        std::vector<unsigned int> getEventPositions() const {return fEventPosition;};
        unsigned int getEventPosition(const unsigned int event) const {return fEventPosition[event];};
        unsigned int getNEvents() const {return fnEvents;};
        int getSize() const;

        void printEvent(const unsigned int event, const bool onFile = false, const char * outFile = "") const;
        void printSection(const unsigned int begin, const unsigned int end, const bool onFile = false, const char * outFile = "") const;

        /////////////////////////////

        int endOfEvent(const int event) const;

        void checkFirstEventSize() const;
        void printLine(const int pos) const;
        void printSize() const;
        void testPrint(const int begin, const int end) const;
        void readToTxt() const;
        void readData(int nbytes) const;

    protected:
        void findEvents();

    private:
        std::string fFilePath;
        std::string fOutputPath;

        std::vector<unsigned int> fEventPosition;       // vector containing the position of the beginning of each event
        unsigned int fnEvents;                          // total number of events stored in the file

        char * fDumpedBytes;         // [fBytesSize] array containing entire file byte by byte
        int fBytesSize;
};