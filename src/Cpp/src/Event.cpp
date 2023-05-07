#include "Event.hpp"

/*    PUBLIC    */

Event::Event(std::string cfgFileName)
{
    Yaml::Parse(fConfigFile ,cfgFileName.c_str());
    SetNmodules(fConfigFile["NModules"].As<unsigned>());

    std::vector<std::string> datatypes;

    Yaml::Node& modules = fConfigFile["Modules"];
    //Creates vector of modules with the settings from config file
    for(auto it = modules.Begin(); it != modules.End(); it++)
    {
        Yaml::Node& ModuleSetting = (*it).second;
        fModules.push_back(Module(ModuleSetting["Bits"].As<unsigned>(), ModuleSetting["Channels"].As<unsigned>(), 
            ModuleSetting["ActiveChannels"].As<unsigned>()));
        datatypes.push_back(ModuleSetting["DataType"].As<std::string>() );
    }
    //TODO: check consistency of Nmodules and size of fModules

    SetDataTypes(datatypes);

    //TODO: Fill events with dumper
    SetEventsRandom();

    Print();

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
        // Checks leftmost bit which has not been checked yet
        if (! (1 & fStatus>>(15-i)))
            return false;
    return true;
}

Event& Event::SetEventsRandom()
{
    std::vector<uint64_t> vec;
    for (auto& i: fModules)
    {
        for (unsigned j=0; j<i.GetActiveChannels(); j++)
            vec.push_back(gRandom->Integer(100));
        i.SetData(vec);
        vec.clear();
    }
    return *this;        
}

Event& Event::Print()
{
    for (unsigned i=0; i<fModules.size(); i++)
    {
        std::cout<<"Module "<<i<<": ";
        fModules[i].Print();
        std::cout<<std::endl;
    }
    return *this;
}


Event& Event::SetNmodules(unsigned Nmodules)
{
    fNmodules=Nmodules;
    return *this;
}

Event& Event::SetDataTypes(std::vector<std::string> DataTypes)
{
    CheckTypesConsistency(DataTypes);
    for (auto& i:DataTypes)
    {
        if (i=="unsigned")
            fDataTypesVector.push_back(fUnsigned);
        else if (i=="double")
            fDataTypesVector.push_back(fDouble);
    }    
    return *this;
}

Event& Event::SetModuleNDouble(unsigned n, std::vector<double> Data)
{
    if (fDataTypesVector.size()>n && fDataTypesVector[n]==fDouble)
        fModules[n].SetDataDouble(Data);
    else if (fDataTypesVector[n]!=fDouble)
        throw runtime_error(std::string("The") + std::to_string(n) +std::string("th module does not store double data"));
    else if (fDataTypesVector.size()<=n)
        throw runtime_error(std::string("The") + std::to_string(n) +std::string("th data type is not specified"));
    return *this;
}

Event& Event::SetModuleNUnsigned(unsigned n, std::vector<uint64_t> Data)
{
    if (fDataTypesVector.size()>n && fDataTypesVector[n]==fUnsigned)
        fModules[n].SetData(Data);
    else if (fDataTypesVector[n]!=fUnsigned)
        throw runtime_error(std::string("The") + std::to_string(n) +std::string("th module does not store double data"));
    else if (fDataTypesVector.size()<=n)
        throw runtime_error(std::string("The") + std::to_string(n) +std::string("th data type is not specified"));
    return *this;
}

void Event::CheckTypesConsistency(std::vector<std::string> DataTypes)
{
    if (DataTypes.size()!=fNmodules)
        throw runtime_error("The number of specified data types differs from the number of modules");
    for (auto& i:DataTypes)
        if (i!="double" && i!="unsigned")
            throw runtime_error("Only double and unsigned types are allowed");
}
