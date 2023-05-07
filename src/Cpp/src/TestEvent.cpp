#include <TSystem.h>
#include <TString.h>
#include "TROOT.h"

void TestEvent(TString myopt="")
{
    gSystem->AddIncludePath((string("-I ")+gSystem->GetWorkingDirectory()+"src/Cpp/build").c_str());
    
    TString opt;
    if (myopt.Contains("force"))    opt="kfg-";          
    else                            opt="kg-";

    // clean build directory
    if (myopt.Contains("clean"))    gSystem->Exec("bash clean.sh");

    gSystem->CompileMacro("src/Cpp/src/Run.cpp",opt.Data(),"","src/Cpp/build");
    gSystem->CompileMacro("utils/yaml/Yaml.cpp",opt.Data(),"","src/Cpp/build");
    gROOT->ProcessLine("Run a(\"/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/src/Cpp/configs/config_Events.yaml\")");
    gROOT->ProcessLine(".q");
}