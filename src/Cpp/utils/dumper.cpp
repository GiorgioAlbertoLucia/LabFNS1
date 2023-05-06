#include <Riostream.h>
#include <string>
#include <cstring>
#include <fstream>
#include <vector>
#include <stdint.h>
#include <iterator>

#include <TString.h>    /* to use Form */

#include "dumper.hpp"

/*  PROTECTED   */

/**
 * @brief Finds the position where each event begins and stores it in the fEventPosition vector and the total number
 * of events in the file.
 * 
 */
void Dumper::findEvents()
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

Dumper::Dumper(const char * filePath, const char * outputPath):
    fFilePath(filePath), fOutputPath(outputPath)
{
    Dumper::findEvents();

    fBytesSize = Dumper::getSize();
    fDumpedBytes = new char[fBytesSize];

    std::fstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);
    streamer.read((char*)&fDumpedBytes[0], fBytesSize);
}

Dumper::~Dumper()
{
    if(fBytesSize > 0)  delete []fDumpedBytes;
}

/**
 * @brief Prints an event in ASCII. Actual data will not be read correctly on terminal, but key information of detectors will
 * be available. Instead of printing out on the terminal, an output file can be produced.
 * 
 * @param event 
 * @param onFile whether to produce an output file
 * @param outFile path to the file to write the event to
 */
void Dumper::printEvent(const unsigned int event, const bool onFile, const char * outFile) const
{
    std::string outFileStr(outFile);
    if(outFile == "")   outFileStr = Form("data/output/dump_%devent.txt", event);

    const unsigned  int first_pos = fEventPosition[event];
    if(event >= fnEvents-1) throw std::exception();
    const unsigned int final_pos = fEventPosition[event+1];

    Dumper::printSection(first_pos, final_pos, onFile, outFileStr.c_str());
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
void Dumper::printSection(const unsigned int begin, const unsigned int end, const bool onFile, const char * outFile) const
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

    if(onFile)
    {
        std::ofstream outStreamer(outFile, std::ios::out);
        for (unsigned int i = begin; i < end; ++i) 
        {
            outStreamer <<  bytes[i];
            if(i%16 == 15)   outStreamer << "\n";
        }
    }
    else
    {
        for (unsigned int i = begin; i < end; ++i) 
        {
            std::cout <<  bytes[i];
            if(i%16 == 15)   std::cout << "\n";
        }
    }
}

/**
 * @brief Returns the size of the file (number of bytes)
 * 
 * @return const int 
 */
int Dumper::getSize() const
{
   std::fstream streamer(fFilePath.c_str(), std::ios::binary|std::ios::in|std::ios::ate);
   if(streamer)
   {
        std::fstream::pos_type size = streamer.tellg();
        return size;
   } 
   else perror(fFilePath.c_str());
   return 0;
}




////////////////////////////////////// OLD FUNCTIONS //////////////////////////////////

/**
 * @brief Prints the size of the file
 * 
 */
void Dumper::printSize() const
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
void Dumper::testPrint(const int begin, const int end) const
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
void Dumper::printLine(const int pos) const
{
    for(int i=0; i<16; i++)     std::cout << fDumpedBytes[pos+i];
    std::cout << "\n";
    for(int i=0; i<16; i++)     printf("%02X ", fDumpedBytes[pos+i]);
    std::cout << "\n";
}

void Dumper::checkFirstEventSize() const 
{
    std::vector<uint8_t> bytes;
    std::ifstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);

    if(streamer.good())
    {
        char buffer[2];
        streamer.read(buffer, 2);
        int firstEventSize = (buffer[0] << 8) | buffer[1];
        std::cout << "The first event size is " << int(firstEventSize) << ".\n";

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
int Dumper::endOfEvent(const int event) const
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