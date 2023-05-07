#ifndef MODULE_H
#define MODULE_H

#include <iostream>
#include <typeinfo>

class Module
{
public:
    Module(unsigned nbytes, unsigned nchannels);
    ~Module();

    unsigned GetBits()                  {return fBits;}
    unsigned GetChannels()              {return fChannels;}
    
    template<typename T>
    T GetData();
    

private:
    unsigned fBits, fChannels;
    std::vector<unsigned> fDataUnsigned;
    std::vector<double> fDataDouble;

};

template<typename T>
T Module::GetData()
{
    if (typeid(T).name()==typeid(std::vector<unsigned>).name())
        return static_cast<T>(fDataUnsigned);
    else if (typeid(T).name()==typeid(std::vector<double>).name())
        return static_cast<T>(fDataDouble);
}



#endif
