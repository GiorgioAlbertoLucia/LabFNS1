#include "Event.h"
#include <iostream>
#include <TSystem.h>

void RunEvent()
{
    //gSystem->CompileMacro("/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/src/Cpp/utils/PlateauFinder.cpp","","","src/Cpp/build");
    //gSystem->Load("PlateauFinder");
    Event a;
    a.SetStatus(15<<12).SetNmodules(4).SetDataTypes({Event::fUnsigned,Event::fDouble,Event::fDouble});
    a.SetModuleNDouble(1,{1.6,3.5,5.2}).SetModuleNUnsigned(0,{1,2,3,5,6});
    std::cout<<a.CheckStatus()<<std::endl;
    std::vector<double> vec = a.GetModuleNDouble(1);
    std::cout<<vec[2]<<std::endl;
    std::vector<unsigned> vec2 = a.GetModuleNUnsigned(0);
    std::cout<<vec2[4]<<std::endl;
}