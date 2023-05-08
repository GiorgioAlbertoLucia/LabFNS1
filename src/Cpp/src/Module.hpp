#ifndef MODULE_H
#define MODULE_H

#include <iostream>
#include <vector>
#include <typeinfo>
#include <stdexcept>
#include <cstdint>

class Module
{
public:
    Module() = default;
    Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels);
    Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint8_t> data);
    Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint16_t> data);
    Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint32_t> data);


    Module& SetData(std::vector<uint8_t>);
    Module& SetData(std::vector<uint16_t>);
    Module& SetData(std::vector<uint32_t>);
    enum fDataTypes {fUnsigned, fDouble};

    Module& SetBits(unsigned bits)              {fBits = bits; return *this;}
    Module& SetType(unsigned type)              {fType=type; return *this;}

    Module& Print();

    unsigned GetBits() const                    {return fBits;}
    unsigned GetChannels() const                {return fChannels;}
    unsigned GetActiveChannels() const          {return fActiveChannels;}
    
    std::vector<uint8_t> GetData8bit() const    {return fData;}
    std::vector<uint16_t> GetData16bit() const  {return fData;}
    std::vector<uint32_t> GetData32bit() const  {return fData;}
    

private:
    unsigned fBits, fChannels, fActiveChannels;
    std::vector<uint8_t> fData8bit;
    std::vector<uint16_t> fData16bit;
    std::vector<uint32_t> fData32bit;
    
    void CheckData(std::vector<uint8_t> data);
    void CheckData(std::vector<uint16_t> data);
    void CheckData(std::vector<uint32_t> data);
};



#endif
