#ifndef MODULE_H
#define MODULE_H

#include <iostream>
#include <vector>
#include <typeinfo>
#include <stdexcept>

class Module
{
public:
    Module() = default;
    Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<unsigned> data);

    Module& SetData(std::vector<unsigned>);

    unsigned GetBits()                  {return fBits;}
    unsigned GetChannels()              {return fChannels;}
    
    std::vector<unsigned> GetData()     {return fData;}
    std::vector<double> GetDataDouble() {return fDataDouble;}

private:
    unsigned fBits, fChannels, fActiveChannels;
    std::vector<unsigned> fData;
    std::vector<double> fDataDouble;

    void CheckData(std::vector<unsigned> data);
};



#endif
