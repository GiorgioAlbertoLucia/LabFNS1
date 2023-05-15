#ifndef EVENT_H
#define EVENT_H

#include <iostream>
#include <stdint.h>
#include <vector>
#include <typeinfo>

#include "Module.hpp"
#include "../yaml/Yaml.hpp"

class Event
{
public:
    Event();
    Event(unsigned eventNumber, std::string cfgFileName, NewDumper& dumpy);
    Event(unsigned evennumb, unsigned nmodules, vector<unsigned> &vectortype, vector<unsigned>& nchan,  NewDumper &Newdumpy);
    bool CheckStatus();                                                     // Checks CAMAC Q state for each module

    Event& SetStatus(uint16_t status)                                       {fStatus=status;        return *this;}
    Event& SetNmodules(unsigned Nmodules);                                   
    Event& SetEventNumber(unsigned EventNumber)                           {fEventNumber=EventNumber;    return *this;}

    uint16_t GetStatus()                        {return fStatus;}
    unsigned GetNmodules()                      {return fNmodules;}
    unsigned GetEventNumber()                   {return fEventNumber;}

    Module getModule(const int indexmod)        {return fmodulesvector[indexmod];}
    std::vector<Module> getModules()            {return fmodulesvector;}

    Event& Print();

protected:
    void InitializeEvent(NewDumper& dumpy);

private:
    Yaml::Node fConfigFile;

    unsigned int fEventNumber;
    uint16_t fStatus;
    unsigned int fNmodules;

    std::vector<Module> fmodulesvector;

};



#endif