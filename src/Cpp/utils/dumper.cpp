#include <Riostream.h>
#include <string>
#include <fstream>
#include <vector>

#include "dumper.hpp"

Dumper::Dumper(const char * filePath, const char * outputPath):
    fFilePath(filePath), fOutputPath(outputPath)
{
    
}

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

const int Dumper::getSize() const
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

void Dumper::testPrint() const
{
    vector<unsigned char> bytes(Dumper::getSize(), 0);

    std::fstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary);
    
    streamer.read((char*)&bytes[0], bytes.size());
    for (int i = 0; i < 512; ++i) {
        printf("%02X ", bytes[i]);
        if(i%16 == 15)   std::cout << "\n";
    }
}