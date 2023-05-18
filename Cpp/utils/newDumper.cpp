#include <Riostream.h>
#include <string>
#include <cstring>
#include <fstream>
#include <vector>
#include <stdint.h>
#include <iterator>
#include <variant>
#include <vector>
#include <cstdint>

#include <TString.h>    /* to use Form */

#include "newDumper.hpp"

/*  PROTECTED   */

/**
 * @brief Finds the position where each event begins and stores it in the fEventPosition vector and the total number
 * of events in the file.
 * 
 */
void NewDumper::findEvents()
{
    std::ifstream streamer(fFilePath.c_str(), std::ios::binary);

    const int BUFFER_SIZE = 16;
    char buffer[BUFFER_SIZE];

    fEventPosition.push_back(0);
    while(streamer)
    {
        streamer.read(buffer, BUFFER_SIZE);
        if(strncmp(buffer, "HHHHHHHHHHHHHHHH", BUFFER_SIZE) == 0)   fEventPosition.push_back(streamer.tellg());
    }
    streamer.close();
    
    if(fEventPosition.size() == 0)  std::cerr << "\033[93mEvent not found\033[0m" << "\n";
    
    fnEvents = fEventPosition.size() - 1;   // the position of the end of the file is stored as well
}

/*    PUBLIC    */

NewDumper::NewDumper(const char * filePath):
    fFilePath(filePath)
{
    NewDumper::findEvents();
}

NewDumper::~NewDumper()
{

}


/**
 * @brief Returns the size of the file (number of bytes)
 * 
 * @return const int 
 */
unsigned int NewDumper::getSize() const
{

    std::fstream streamer(fFilePath.c_str(), std::ios::binary|std::ios::in|std::ios::ate);
    if(streamer)
    {
        streamer.seekg(0, std::ios::end);
        std::streamsize size = streamer.tellg();
        return size;
    } 
    else    throw std::exception();
    return 0;
}


/**
 * @brief Read the size of the event directly from the .dat file.
 * 
 * @param event 
 * @return unsigned int 
 */
unsigned int NewDumper::readEventSize(const int event) const
{
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);
    int eventBeginPos = 0;

    if(streamer.good())
    {
        for(unsigned int current_event = 0; current_event < fnEvents; current_event++)
        {
            std::vector<uint8_t> buffer(2, 0);
            streamer.read(reinterpret_cast<char*>(buffer.data()), 2);

            uint16_t eventSize = (buffer[0] << 8) | buffer[1];
            if(current_event == event)  return (unsigned int)eventSize;

            eventBeginPos += eventSize;
            streamer.seekg(eventSize, std::ios::beg);
        }
        streamer.close();
    }
    else    throw std::exception();
    return 0;
}

/**
 * @brief Read the module status as a 16-bit variable. The module status information is stored in byte 6-7 of each event.
 * 
 * @param event 
 * @return uint16_t 
 */
uint16_t NewDumper::readModulesStatus(const int event) const
{
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);

    if(streamer.good())
    {
        streamer.seekg(fEventPosition[event]+6, std::ios::beg);
        std::vector<uint8_t> buffer(2, 0);
        streamer.read(reinterpret_cast<char*>(buffer.data()), 2);
        uint16_t moduleStatus = (buffer[0] << 8) | buffer[1];
        streamer.close();

        return moduleStatus;
    }
    else    throw std::exception();
    return 0;
}

/**
 * @brief Reads a section of the file between two given position into a vector of uint8_t.
 * 
 * @param begin first byte
 * @param end last byte (not printed)
 */
std::vector<uint8_t> NewDumper::readSection(const unsigned int begin, const unsigned int end) const
{
    const unsigned int size = end - begin;
    std::vector<uint8_t> bytes(size, 0);
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);

    if(streamer.good())
    {
        streamer.seekg(begin);
        bytes.reserve(size);
        streamer.read(reinterpret_cast<char*>(&bytes[0]), size);
        streamer.close();
    }
    else    
    {   
        std::cerr << "NewDumper was unable to open the file" << std::endl;
        throw std::exception();
    }
    
    return bytes;
}



/**
 * @brief Prints an event in ASCII. Actual data will not be read correctly on terminal, but key information of detectors will
 * be available. Instead of printing out on the terminal, an output file can be produced.
 * 
 * @param event 
 * @param onFile whether to produce an output file
 * @param outFile path to the file to write the event to
 */
void NewDumper::printEvent(const unsigned int event, const bool onFile, const char * outFile) const
{
    std::string outFileStr(outFile);
    if(strcmp(outFile, "") == 0)   outFileStr = Form("data/output/dump_%devent.txt", event);

    if(event >= fnEvents) throw std::exception();

    NewDumper::printSection(fEventPosition[event], fEventPosition[event+1], onFile, outFileStr.c_str());
}

/**
 * @brief Prints a section of the file between two given position (bytes of the file will be converted in ASCII). It is
 * possible to print to a file instead of printing out to the terminal.
 * 
 * @param begin first byte
 * @param end last byte (not printed)
 * @param onFile whether to produce and output file
 * @param outFile path to the file to write to
 */
void NewDumper::printSection(const unsigned int begin, const unsigned int end, const bool onFile, const char * outFile) const
{
    std::vector<uint8_t> bytes;
    const unsigned int size = end - begin;
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);
    
    if(streamer.good())
    {
        streamer.seekg(begin);
        bytes.reserve(size);
        streamer.read(reinterpret_cast<char*>(&bytes[0]), size);
        streamer.close();
        //std::vector<uint8_t> vec_buffer((std::istreambuf_iterator<char>(streamer)), (std::istreambuf_iterator<char>()));
        //bytes = vec_buffer;
        //streamer.close();
    }
    else    throw std::exception();

    if(onFile)
    {
        std::ofstream outStreamer(outFile, std::ios::out);
        for (unsigned int i = begin; i < end; ++i) 
        {
            outStreamer << bytes[i];
            if(i%16 == 15)   outStreamer << "\n";
        }

        for (unsigned int i = begin; i < end; ++i) 
        {
            outStreamer << std::hex << bytes[i];
            if(i%16 == 15)   outStreamer << "\n";
        }
    }
    else
    {
        for (unsigned int i = 0; i < size; ++i) 
        {
            std::cout << bytes[i];
            if(i%16 == 15)   std::cout << "\n";
        }

        for (unsigned int i = 0; i < size; ++i) 
        {
            printf("%02X ", bytes[i]);
            if(i%16 == 15)   std::cout << "\n";
        }
    }
}

/**
 * @brief Prints modules information (stored after the first 16 bytes, 64 bytes per module)
 * 
 * @param nModules number of modules used 
 * @param onFile whether the output should be save to a file
 * @param outFile file to save the output to
 */
void NewDumper::printModulesInfo(const int nModules, const bool onFile, const char * outFile) const
{
    std::vector<uint8_t> bytes(64*nModules);
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);
    streamer.seekg(16, std::ios::beg);

    if(streamer.good())
    {
        streamer.read(reinterpret_cast<char*>(bytes.data()), 64*nModules);
        streamer.close();
    }
    else    throw std::exception();

    if(onFile)
    {
        std::ofstream outStreamer(outFile, std::ios::out);
        for (unsigned int i = 0; i < bytes.size(); i++) 
        {
            outStreamer <<  bytes[i];
            if(i%64 == 63)   outStreamer << "\n";
        }
    }
    else
    {
        for (unsigned int i = 0; i < bytes.size(); i++) 
        {
            std::cout <<  bytes[i];
            if(i%64 == 63)   std::cout << "\n";
        }
    }
}

template<>
std::vector<uint8_t> NewDumper::readData(const unsigned int startpoint, const unsigned int stoppoint) const
{
    //static_assert(std::is_same_v<T, uint8_t>, "Invalid type parameter. Type parameter must be uint8_t.");
    std::vector<unsigned char> bytes=readSection(startpoint,stoppoint);//esempio
    int sizeD=bytes.size();
    std::vector<uint8_t> vet(sizeD, 0);
    unsigned char onebyte[1];
    uint8_t bytesvec[sizeD];
    for(int jj=0;jj<sizeD;jj++)
    {
        onebyte[0]=bytes[jj];
        bytesvec[jj]=*(uint8_t*)onebyte;
    }
    for(int ii=0;ii<sizeD;ii++) vet[ii] = bytesvec[ii];
    return vet;
}

template<>
std::vector<uint16_t> NewDumper::readData(const unsigned int startpoint, const unsigned int stoppoint) const
{
    //static_assert(std::is_same_v<T, uint16_t>, "Invalid type parameter. Type parameter must be uint16_t.");
    std::vector<unsigned char> bytes=readSection(startpoint,stoppoint);
    //std::cout << "vec size (from readSection in readData) = " << bytes.size() << "\n";
    int sizeD=bytes.size();
    std::vector<uint16_t> vet(int(sizeD/2), 0);
    unsigned char twobytes[2];
    int yy=0;
    uint16_t bytesvec[int(sizeD/2)];
    for(int uu=0;uu<sizeD;uu++)
    {
                if((uu%2)==0)
                {
                    //aa=bytes[uu];
                    //bytes[uu]=bytes[uu+1];
                    //bytes[uu+1]=aa;
                    twobytes[1]=bytes[uu];
                    twobytes[0]=bytes[uu+1];
                    bytesvec[yy]=*(uint16_t*)twobytes;
                    yy++;
                }
    }
    for(int ii=0;ii<int(sizeD/2);ii++) vet[ii] = bytesvec[ii];
    return vet;
}

template<>
std::vector<uint32_t> NewDumper::readData(const unsigned int startpoint, const unsigned int stoppoint) const
{
    //static_assert(std::is_same_v<T, uint32_t>, "Invalid type parameter. Type parameter must be uint32_t.");
    std::vector<unsigned char> bytes=readSection(startpoint,stoppoint);//esempio
    int sizeD=bytes.size();
    std::vector<uint32_t> vet(int(sizeD/4), 0);
    unsigned char fourbytes[4];
    int yy=0;
    uint16_t bytesvec[int(sizeD/4)];
    for(int uu=0;uu<sizeD;uu++)
    {
          
        if((uu%4)==0)
        {
            /*int bb=0, cc=3;
            while(bb<cc)
            {
                aa=bytes[uu+bb];
                bytes[uu+bb]=bytes[uu+cc];
                bytes[uu+cc]=aa;
            }
            for(int hl=0;hl<4;hl++) fourbytes[hl]=bytes[uu+hl];
            */
            fourbytes[0]=bytes[uu+3];
            fourbytes[1]=bytes[uu+2];
            fourbytes[2]=bytes[uu+1];
            fourbytes[3]=bytes[uu];
            bytesvec[yy]=*(uint32_t*)fourbytes;
            yy++;
        }
            
    }
    for(int ii=0;ii<int(sizeD/4);ii++) vet[ii] = bytesvec[ii];
    return vet;
}


////////////////////////////////////// OLD FUNCTIONS //////////////////////////////////

/**
 * @brief Prints the size of the file
 * 
 */
void NewDumper::printSize() const
{
    std::fstream streamer(fFilePath.c_str(), std::ios::binary|std::ios::in|std::ios::ate);
   if(streamer)
   {
        std::fstream::pos_type size = streamer.tellg();
        std::cout << fFilePath << " " << size << "\n";
   } 
   else perror(fFilePath.c_str());
}

/**
 * @brief Function to test how to read and print a binary file (between two positions)
 * 
 * @param begin 
 * @param end 
 */
void NewDumper::testPrint(const int begin, const int end) const
{
    std::vector<uint8_t> bytes;
    std::ifstream streamer(fFilePath.c_str(), std::ios::binary);
    if(streamer.good())
    {
        std::vector<unsigned char> vec_buffer((std::istreambuf_iterator<char>(streamer)), (std::istreambuf_iterator<char>()));
        bytes = vec_buffer;
        streamer.close();
    }
    else    throw std::exception();

    for (int i = begin; i < end; ++i) {
        printf("%02X ", bytes[i]);
        if(i%16 == 15)   std::cout << "\n";
    }
    for (int i = begin; i < end; ++i) {
        std::cout <<  bytes[i];
        if(i%16 == 15)   std::cout << "\n";
    }
}

/**
 * @brief Prints 16 bytes from the selected position (both in hexadecimal and in ascii)
 * 
 * @param pos 
 */
void NewDumper::printLine(const int pos) const
{
    const int size = NewDumper::getSize();
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);
    std::vector<uint8_t> buffer(size, 0);

    if(streamer.good())         streamer.read(reinterpret_cast<char*>(buffer.data()), 16);
    else    throw std::exception();

    for(int i=0; i<16; i++)     std::cout << buffer[pos+i];
    std::cout << "\n";
    for(int i=0; i<16; i++)     printf("%02X ", buffer[pos+i]);
    std::cout << "\n";
}

void NewDumper::checkFirstEventSize() const 
{
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);

    if(streamer.good())
    {
        std::vector<uint8_t> buffer(2, 0);
        streamer.read(reinterpret_cast<char*>(buffer.data()), 2);
        uint16_t firstEventSize = (buffer[0] << 8) | buffer[1];
        std::cout << "The first event size is " << std::hex << firstEventSize << " (in dec: ";
        std::cout << std::dec << firstEventSize << ").\n";

        //std::vector<uint8_t> vec_buffer((std::istreambuf_iterator<char>(streamer)), (std::istreambuf_iterator<char>()));
        //bytes = vec_buffer;
        //streamer.close();
    }
    else    throw std::exception();

    //uint8_t temp[2];
    //for(int i=0; i<2; i++)  temp[i] = bytes[i];
    //uint16_t firstEventSize = *((uint16_t*)temp);
//
    //std::cout << "The first event size is " << int(firstEventSize) << ".\n";
    //for(int i=int(firstEventSize)-16; i<int(firstEventSize); i++) std::cout << bytes[i];
    //std::cout << "\n";
}

/**
 * @brief Returns the position for the end of the selected event.
 * 
 * @param event 
 * @return const int 
 */
int NewDumper::endOfEvent(const int event) const
{
    int current_event = 0;
    std::ifstream streamer(fFilePath.c_str(), std::ios::binary);

    const int BUFFER_SIZE = 16;
    char buffer[BUFFER_SIZE];
    
    while(streamer)
    {
        streamer.read(buffer, BUFFER_SIZE);
        if(strncmp(buffer, "HHHHHHHHHHHHHHHH", BUFFER_SIZE) == 0)   
        {
            std::cout << "Event " << current_event << " ends at line " << streamer.tellg() << ".\n";
            if(current_event == event)  
            {
                streamer.close();
                return streamer.tellg();
            }
            current_event++;
        }
    }
    streamer.close();
    std::cerr << "\033[93mEvent not found\033[0m" << "\n";
    return 0;

}


