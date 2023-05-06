#include <TSystem.h>
#include <TString.h>

void loadMacros(TString myopt="")
{
    gSystem->AddIncludePath((string("-I ")+gSystem->GetWorkingDirectory()+"src/Cpp/build").c_str());
    
    TString opt;
    if (myopt.Contains("force"))    opt="kfg-";          
    else                            opt="kg-";

    // clean build directory
    if (myopt.Contains("clean"))    gSystem->Exec("bash clean.sh");

    gSystem->CompileMacro("src/Cpp/src/hello.cpp",opt.Data(),"","src/Cpp/build");
    gSystem->CompileMacro("src/Cpp/utils/newDumper.cpp",opt.Data(),"","src/Cpp/build");
    gSystem->CompileMacro("src/Cpp/utils/fileManager.cpp",opt.Data(),"","src/Cpp/build");
}