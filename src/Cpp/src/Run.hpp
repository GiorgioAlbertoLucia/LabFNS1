#ifndef RUN_H
#define RUN_H

#include <vector>
#include <string>
#include "Module.hpp"
#include "../../../utils/yaml/Yaml.hpp"

class Run
{

public:
    Run(std::string cfgFileName);
    
private:
    Yaml::Node fConfigFile;
    std::vector<Module> fModules;
    std::string fDataFileName;
    unsigned fNmodules;
};
 
 
#endif
