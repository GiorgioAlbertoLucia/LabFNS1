#ifndef EVENT_H
#define EVENT_H

#include <iostream>
#include <cstdint>
#include <vector>
#include <string>
#include <typeinfo>
#include <variant>
#include <stdexcept>
#include "../../../utils/yaml/Yaml.hpp"

#include "Module.hpp"
#include "TRandom3.h"

class Event
{
public:
    Event() = default;
    Event(std::string cfgFileName);
    bool CheckStatus();                                                     // Checks CAMAC Q state for each module

    Event& SetEventsRandom();

    uint16_t GetStatus()                                                    {return fStatus;}
    unsigned GetNmodules()                                                  {return fNmodules;}
    unsigned GetEventNumber()                                               {return fEventNumber;}
    std::vector<double> GetModuleNDouble(unsigned n)                        {return fModules[n].GetDataDouble();}
    std::vector<uint64_t> GetModuleN(unsigned n)                            {return fModules[n].GetData();}

    Event& Print();
       

private:
    Yaml::Node fConfigFile;

    Event& SetStatus(uint16_t status)                                       {fStatus=status;        return *this;}
    Event& SetEventNumber(unsigned EventNumber)                             {fEventNumber=EventNumber;    return *this;}
    Event& SetModuleNUnsigned(unsigned n, std::vector<uint64_t> Data);
    Event& SetModuleNDouble(unsigned n, std::vector<double> Data);
    Event& SetNmodules(unsigned Nmodules);                                   
    Event& SetDataTypes(std::vector<std::string> DataTypes);                    
    Event& SetModuleNBits(unsigned n, unsigned bits)                        {return *this;}

    void CheckTypesConsistency(std::vector<std::string> DataTypes);
    
    unsigned fEventNumber;
    uint16_t fStatus;
    unsigned fNmodules;
    std::vector<Module> fModules;


    std::vector<unsigned> fDataTypesVector;

};



#endif