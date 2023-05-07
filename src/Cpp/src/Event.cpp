#include "Event.hpp"

Event::Event()
{}

Event::Event(unsigned int eventnumber, NewDumper dumper):
{

    //std::vector<uint8_t> eventbytes;
    //std::ifstream streamer((dumper.fFilePath).c_str(), std::ios::in | std::ios::binary);
    //if(streamer.good())
    //{
    //    streamer.seekg(dumper.getEventPosition(eventnumber), ios_base::beg);
    //    std::vector<uint8_t> vec_buffer((std::istreambuf_iterator<char>(streamer)), (std::istreambuf_iterator<char>()));
    //    eventbytes = vec_buffer;
    //    streamer.close();
    //}
    //else    throw std::exception();
//
//
    //SetStatus(((uint16_t)eventbytes[2] << 8) | eventbytes[1]);
    //if(CheckStatus()){
    //    
    //    SetEventNumber(dumper.readData({eventbytes[0]}));
//
    //    for(unsigned channel = 0; channel<fNmodules; channel++){
    //        unsigned int offset = 16;
//
    //        fData[channel].push_back(dumper.readData({eventbytes[offset+channel*64],eventbytes[offset+channel*64]+1,
    //                                                  eventbytes[offset+channel*64]+2,eventbytes[offset+channel*64]+3}));
    //    }
//
    //}    
}

/**
 * @brief Function that checks the CAMAC Q state of the modules
 * 
 * @return bool 
 */
bool Event::CheckStatus()
{
    for (unsigned i=0; i<fNmodules; i++)
        // Checks if leftmost bit which has not been checked yet is equal to 1
        if (! (1 & fStatus>>(15-i)))
            return false;
    return true;
}

Event& Event::SetNmodules(unsigned Nmodules)
{
    fNmodules=Nmodules;
    if (fData.size()>0)
        std::cout<<"\033[93mChanging the number of modules deletes the existing data, be careful!\033[0m"<<std::endl;
    fData.clear();
    for (unsigned i=0; i<fNmodules; i++)
        fData.push_back({});
    return *this;
}

Event& Event::SetModuleNDouble(unsigned n, std::vector<double> Data)
{
    if (fDataTypesVector.size()>n && fDataTypesVector[n]==fDouble)
    {
        fDataVector newdata;
        for (auto i: Data)
            newdata.push_back(i);
        SetModuleNData(n, newdata);
    }
    else if (fDataTypesVector[n]!=fDouble)
        std::cout<<"\033[93mThe "<<n<<" th module does not store double data\033[0m"<<std::endl;
    else if (fDataTypesVector.size()<=n)
        std::cout<<"\033[93mThe "<<n<<" th data type is not specified\033[0m"<<std::endl;    
    return *this;
}

Event& Event::SetModuleNUnsigned(unsigned n, std::vector<unsigned> Data)
{
    if (fDataTypesVector.size()>n && fDataTypesVector[n]==fUnsigned)
    {
        fDataVector newdata;
        for (auto i: Data)
            newdata.push_back(i);
        SetModuleNData(n, newdata);
    }
    else if (fDataTypesVector[n]!=fUnsigned)
        std::cout<<"\033[93mThe "<<n<<" th module does not store unsigned data\033[0m"<<std::endl;
    else if (fDataTypesVector.size()<=n)
        std::cout<<"\033[93mThe "<<n<<" th data type is not specified\033[0m"<<std::endl;   
    return *this;
}


std::vector<double> Event::GetModuleNDouble(unsigned n)      
{
    std::vector<double> vec;
    for (auto i:fData[n])
        vec.push_back(std::get<double>(i));
    return vec;
}

std::vector<unsigned> Event::GetModuleNUnsigned(unsigned n)      
{
    std::vector<unsigned> vec;
    for (auto i:fData[n])
        vec.push_back(std::get<unsigned>(i));
    return vec;
}