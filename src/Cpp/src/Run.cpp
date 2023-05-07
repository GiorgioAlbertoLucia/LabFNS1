#include "event.hpp"
#include ".hpp"


Run::Run(string cfgFileName):fConfigFile(YAML::LoadFile(cfgFileName.Data())),
fDataFileName(fConfigFile["DataFileName"].as<std::string>()),
fNmodules(fConfigFile["NModules"].as<unsigned int>()),
{

    for(int i=1; i<fNmodules; i++){
        unsigned int nbits = fConfigFile["Module" + std::to_string(i)]["Bits"].as<unsigned int>();
        unsigned int nchannels = fConfigFile["Module" + std::to_string(i)]["Channels"].as<unsigned int>();
        Module module(nbytes, nchannels);
        fModules.push_back(module);
    }

    std::string outpath = "../../../data/input/";
    std::string filepath = outpath + fDataFileName;

    NewDumper dumper(filepath.c_str(), outpath.c_str());

    for(unsigned i=0; i<dumper.getNEvents(); i++){
        Event event(i, dumper);
        fModules[i].fillData(event.fData[i]);
    }
    
}