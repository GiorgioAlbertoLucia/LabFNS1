#include <Riostream.h>
#include <string>
#include <fstream>
#include <vector>
#include <stdint.h>

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

void Dumper::readData(int nbytes) const
{
    vector<unsigned char> bytes(Dumper::getSize(), 0);

    std::fstream streamer(fFilePath.c_str(), std::ios::in | std::ios::binary); 

    streamer.read((char*)&bytes[0], bytes.size());
    if(nbytes==1)
    {
        vector<uint8_t> bytesvec(Dumper::getsize()/1);
        for(int jj=0;jj<bytesvec.size(),j++)
        {
          bytesvec[jj]=atoi(bytes[jj]);
        }
    }
    else 
    {
        if(nbytes==2)
        {
            vector<uint16_t*> bytesvec(Dumper::getsize()/2);
            vector<unsigned char> twobytes(2);
            int yy=0;
            //unsigned char aa;
            /*
            la parte commentata è se vogliamo invertire direttamente dall'array di bytes, quella non commentata se vogliamo
            lasciare l'array originale e solo storare i caratteri invertiti e convertiti in un altro array 
            */
            for(int uu=0;uu<bytesvec.size();uu++)
            {
                if((uu%2)==0)
                {
                    //aa=bytes[uu];
                    //bytes[uu]=bytes[uu+1];
                    //bytes[uu+1]=aa;
                    twobytes[1]=bytes[uu];
                    twobytes[0]=bytes[uu+1];
                    bytesvec[yy]=(uint16_t*)twobytes;
                    yy++;
                }
            }

        }
        else
        {
            vector<uint32_t> bytesvec(Dumper::getsize()/4);
            vector<unsigned char> fourbytes(4);
            //unsigned char aa;
            int yy=0;
            for(int uu=0;uu<bytesvec.size(),uu++)
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
                    bytesvec[yy]=(uint32_t*)fourbytes;
                    yy++;
                }
            }
        }
    }
}


