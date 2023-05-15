#include <TSystem.h>
#include <TString.h>
#include "../../Python/src/loader.hpp"

void loadYaml(TString myopt="")
{
    //loader();
    gSystem->AddIncludePath((string("-I ")+gSystem->GetWorkingDirectory()+"Cpp/build").c_str());
    
    TString opt;
    if (myopt.Contains("force"))    opt="kfg-";          
    else                            opt="kg-";

    // clean build directory
    if (myopt.Contains("clean"))    gSystem->Exec("bash clean.sh");

    gSystem->CompileMacro("Cpp/yaml/Yaml.cpp",opt.Data(),"","Cpp/build");
}