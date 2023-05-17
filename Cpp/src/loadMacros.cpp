#include <TSystem.h>
#include <TString.h>
#include "../../Python/src/loader.hpp"

void loadMacros(TString myopt="")
{
    //loader();
    gSystem->AddIncludePath((string("-I ")+gSystem->GetWorkingDirectory()+"Cpp/build").c_str());
    
    TString opt;
    if (myopt.Contains("force"))    opt="kfg-";          
    else                            opt="kg-";

    // clean build directory
    if (myopt.Contains("clean"))    gSystem->Exec("bash clean.sh");

    gSystem->CompileMacro("Cpp/yaml/Yaml.cpp",opt.Data(),"","Cpp/build");
    //gSystem->CompileMacro("Cpp/src/hello.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/utils/newDumper.cpp",opt.Data(),"","Cpp/build");
    //gSystem->CompileMacro("Cpp/utils/fileManager.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/src/Module.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/src/Event.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/src/Run.cpp",opt.Data(),"","Cpp/build");
    //gROOT->ProcessLine(".x /home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Cpp/src/event_test.cpp");
    //gROOT->ProcessLine("NewDumper dumpy(\"data/input/example_pedestal.dat\");");
    //gROOT->ProcessLine("Event b(0, \"Cpp/configs/config_Events2.yml\", dumpy);");
    //gROOT->ProcessLine("Run a(\"Cpp/configs/config_Events2.yml\");");
}