#ifndef RUN_H
#define RUN_H

#include <vector>
#include <string>
#include "Module.hpp"
#include "TTree.h"
#include "TFile.h"
#include "TObject.h"
#include "TRandom3.h"
#include "../yaml/Yaml.cpp"

class Run
{

public:
    Run(std::string cfgFileName);
    
private:
    Yaml::Node fConfigFile;
    std::vector<Module> fModules;
    std::string fDataFileName;
    unsigned fNmodules;
    TTree fTreeData;
    void TreeSettings();
};
 
 
#endif
