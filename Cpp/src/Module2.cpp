#include "Module.hpp"

/*
    PUBLIC
*/

Module::Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint8_t> data):
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels)
{
    SetData(data);
}

Module::Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint16_t> data):
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels)
{
    SetData(data);
}

Module::Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint32_t> data):
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels)
{
    SetData(data);
}

Module::Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels):
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels)
{}


Module& Module::SetData(std::vector<uint8_t> data)
{
    CheckData(data);
    fData=data;
    return *this;
}

Module& Module::SetData(std::vector<uint16_t> data)
{
    CheckData(data);
    fData=data;
    return *this;
}

Module& Module::SetData(std::vector<uint32_t> data)
{
    CheckData(data);
    fData=data;
    return *this;
}

Module& Module::Print()
{
    std::cout<<"[ ";
    if (fType==fUnsigned)
        for (auto& i:fData)
            std::cout<<i<<" ";
    else if (fType==fDouble)
        for (auto& i:fDataDouble)
            std::cout<<i<<" ";
    std::cout<<"] ";
    
    return *this;
}

/*
    PRIVATE
*/


void Module::CheckData(std::vector<uint8_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}

void Module::CheckData(std::vector<uint16_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}

void Module::CheckData(std::vector<uint32_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}

