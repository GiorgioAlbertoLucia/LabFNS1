#ifndef EVENT_H
#define EVENT_H

#include <iostream>
#include <stdint.h>
#include <vector>
#include <typeinfo>
#include <variant>
#include "../utils/newDumper.hpp"

class Event
{
public:
    Event();
    Event(unsigned int eventnumber, NewDumper dumper);
    bool CheckStatus();                                                     // Checks CAMAC Q state for each module
    enum fDataTypes {fUnsigned, fDouble};
    using fDataVector = std::vector<std::variant<unsigned, double>>;

    Event& SetStatus(uint16_t status)                                       {fStatus=status;        return *this;}
    Event& SetNmodules(unsigned Nmodules);                                   
    Event& SetEventNumber(unsigned EventNumber)                             {fEventNumber=EventNumber;    return *this;}
    Event& SetDataTypes(std::vector<unsigned> DataTypes)                    {fDataTypesVector=DataTypes;    return *this;}
    Event& SetModuleNDouble(unsigned n, std::vector<double> Data);
    Event& SetModuleNUnsigned(unsigned n, std::vector<unsigned> Data);

    uint16_t GetStatus()                        {return fStatus;}
    unsigned GetNmodules()                      {return fNmodules;}
    unsigned GetEventNumber()                   {return fEventNumber;}
    fDataVector GetModuleNData(unsigned n)      {return fData[n];}
    std::vector<double> GetModuleNDouble(unsigned n);
    std::vector<unsigned> GetModuleNUnsigned(unsigned n);
       

private:
    unsigned fEventNumber;
    uint16_t fStatus;
    unsigned fNmodules;

    std::vector<unsigned> fDataTypesVector;

    std::vector<fDataVector> fData;
    
    Event& SetModuleNData(unsigned n, fDataVector Data)                     {fData[n]=Data; return *this;}
};



#endif