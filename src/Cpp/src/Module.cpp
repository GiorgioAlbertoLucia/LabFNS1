#include "Module.hpp"

Module::Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<unsigned> data):
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels)
{
    SetData(data);
}


Module& Module::SetData(std::vector<unsigned> data)
{
    CheckData(data);
    fData=data;
    return *this;
}


void Module::CheckData(std::vector<unsigned> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}