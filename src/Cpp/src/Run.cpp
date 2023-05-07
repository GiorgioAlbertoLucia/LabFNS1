//#include "Event.hpp"
#include "Run.hpp"


Run::Run(std::string cfgFileName)
{
    Yaml::Parse(fConfigFile, cfgFileName.c_str());
    fDataFileName = fConfigFile["DataFileName"].As<std::string>();
    fNmodules = fConfigFile["NModules"].As<unsigned>();

    Yaml::Node& modules = fConfigFile["Modules"];
    for(auto it = modules.Begin(); it != modules.End(); it++)
    {
        Yaml::Node& ModuleSetting = (*it).second;
        std::cout<< ModuleSetting["DataType"].As<std::string>()<<std::endl;
        fModules.push_back(Module(ModuleSetting["Bits"].As<unsigned>(), ModuleSetting["Channels"].As<unsigned>(), 
            ModuleSetting["ActiveChannels"].As<unsigned>(), {1,2}));
        std::cout<< fModules.back().GetChannels() << std::endl;
    }
    //for(int i=1; i<fNmodules; i++){
    //    unsigned int nbits = fConfigFile["Module" + std::to_string(i)]["Bits"].as<unsigned int>();
    //    unsigned int nchannels = fConfigFile["Module" + std::to_string(i)]["Channels"].as<unsigned int>();
    //    Module module(nbytes, nchannels);
    //    fModules.push_back(module);
    //}

    std::string outpath = "../../../data/input/";
    std::string filepath = outpath + fDataFileName;

    //NewDumper dumper(filepath.c_str(), outpath.c_str());

    //for(unsigned i=0; i<dumper.getNEvents(); i++){
    //    Event event(i, dumper);
    //    fModules[i].fillData(event.fData[i]);
    //}
    
}