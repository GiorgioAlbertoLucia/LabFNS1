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
    Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint64_t> data);

    Module& SetData(std::vector<uint64_t>);
    Module& SetDataDouble(std::vector<double>);
    Module& SetBits(unsigned bits)              {fBits = bits; return *this;}

    Module& Print();

    unsigned GetBits()                  {return fBits;}
    unsigned GetChannels()              {return fChannels;}
    unsigned GetActiveChannels()        {return fActiveChannels;}
    
    std::vector<uint64_t> GetData()     {return fData;}
    std::vector<double> GetDataDouble() {return fDataDouble;}

private:
    unsigned fBits, fChannels, fActiveChannels;
    std::vector<uint64_t> fData;
    std::vector<double> fDataDouble;

    void CheckData(std::vector<uint64_t> data);
    void CheckData(std::vector<double> data);
};



#endif
