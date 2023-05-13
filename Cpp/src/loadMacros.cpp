#include <TSystem.h>
#include <TString.h>
#include "../../Python/loader.hpp"

void loadMacros(TString myopt="")
{
    //loader();
    gSystem->AddIncludePath((string("-I ")+gSystem->GetWorkingDirectory()+"Cpp/build").c_str());
    
    TString opt;
    if (myopt.Contains("force"))    opt="kfg-";          
    else                            opt="kg-";

    // clean build directory
    if (myopt.Contains("clean"))    gSystem->Exec("bash clean.sh");

    gSystem->CompileMacro("Cpp/src/hello.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/utils/newDumper.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/utils/fileManager.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/src/Module.cpp",opt.Data(),"","Cpp/build");
    gSystem->CompileMacro("Cpp/src/Event.cpp",opt.Data(),"","Cpp/build");
}