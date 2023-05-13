#ifndef NEWDUMPER_H
#define NEWDUMPER_H

#include <Riostream.h>
#include <string>
#include <vector>
#include <variant>
#include <cstdint>
#include <memory>

class Basevec
{
    public:
        virtual ~Basevec()=default;
        

};

class Vec8: public Basevec
{
    public:
       std::vector<uint8_t> data;
};

class Vec16: public Basevec
{
    public:
        std::vector<uint16_t> data;
};

class Vec32: public Basevec
{
    public:
        std::vector<uint32_t> data;
};

class NewDumper
{
    public:
        NewDumper(){};
        NewDumper(const char * filePath, const char * outputPath);
        ~NewDumper();

        std::vector<unsigned int> getEventPositions() const {return fEventPosition;};
        unsigned int getEventPosition(const unsigned int event) const {return fEventPosition[event];};
        unsigned int getNEvents() const {return fnEvents;};
        unsigned int getSize() const;

        unsigned int readEventSize(const int event) const;
        uint16_t readModulesStatus(const int event) const;
        std::vector<uint8_t> readSection(const unsigned int begin, const unsigned int end) const;

        void printEvent(const unsigned int event, const bool onFile = false, const char * outFile = "") const;
        void printSection(const unsigned int begin, const unsigned int end, const bool onFile = false, const char * outFile = "") const;
        void printModulesInfo(const int nModules, const bool onFile = false, const char * outFile = "data/output/modulesInfo.txt") const;
        //Basevec readData(int nbytes) const;
        template<typename T>
        std::vector<T> readData(const unsigned int startpoint, const unsigned int stoppoint) const;
        
        //template<typename T>
        //std::vector<uint8_t> readData(const unsigned int startpoint, const unsigned int stoppoint) const;
        //template<typename T>
        //std::vector<uint16_t> readData(const unsigned int startpoint, const unsigned int stoppoint) const;
        //template<typename T>
        //std::vector<uint32_t> readData(const unsigned int startpoint, const unsigned int stoppoint) const;

        /////////////////////////////

        int endOfEvent(const int event) const;

        void checkFirstEventSize() const;
        void printLine(const int pos) const;
        void printSize() const;
        void testPrint(const int begin, const int end) const;
        void readToTxt() const;

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


#endif
//************************************************************



#endif