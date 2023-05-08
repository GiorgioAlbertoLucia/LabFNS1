#include "Module.hpp"

Module::Module(unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint64_t> data):
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


Module& Module::SetData(std::vector<uint64_t> data)
{
    CheckData(data);
    fData=data;
    return *this;
}

Module& Module::SetDataDouble(std::vector<double> data)
{
    CheckData(data);
    fDataDouble=data;
    return *this;
}

void Module::CheckData(std::vector<uint64_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}


void Module::CheckData(std::vector<double> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
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