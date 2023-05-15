#ifndef MODULE_H
#define MODULE_H

#include <iostream>
#include <vector>
#include <typeinfo>
#include <stdexcept>
#include <cstdint>
#include "../utils/newDumper.hpp"

class Module
{
public:
    Module() = default;
    Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, const char * name = " ");
    Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint8_t> data, const char * name = " ");
    Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint16_t> data, const char * name = " ");
    Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint32_t> data, const char * name = " ");


    Module& SetData(std::vector<uint8_t>);
    Module& SetData(std::vector<uint16_t>);
    Module& SetData(std::vector<uint32_t>);

    Module& SetBits(unsigned bits)              {fBits = bits; return *this;}

    Module& Print();

    unsigned GetBits() const                    {return fBits;}
    unsigned GetChannels() const                {return fChannels;}
    unsigned GetActiveChannels() const          {return fActiveChannels;}
    
    std::vector<uint8_t> GetData8bit() const    {return fData8bit;}
    std::vector<uint16_t> GetData16bit() const  {return fData16bit;}
    std::vector<uint32_t> GetData32bit() const  {return fData32bit;}
    //void setnModule(Event&);
    

private:
    std::string fName;

    unsigned fBits, fChannels, fActiveChannels;
    int nmodule;                                // module number 

    std::vector<uint8_t> fData8bit;
    std::vector<uint16_t> fData16bit;
    std::vector<uint32_t> fData32bit;

    
    void CheckData(std::vector<uint8_t> data);
    void CheckData(std::vector<uint16_t> data);
    void CheckData(std::vector<uint32_t> data);
};



#endif
