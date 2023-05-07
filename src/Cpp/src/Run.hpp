#ifndef RUN_H
#define RUN_H

#include <vector>
#include <string>
#include "Module.hpp"
 
class Run
{

public:
    Run(string cfgFileName);
    
private:
    YAML::Node fConfigFile;
    std::vector<Module> fModules;
    unsigned int fNmodules;
};
 
 
#endif
