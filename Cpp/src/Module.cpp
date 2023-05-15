#include "Module.hpp"
#include "vector"

/*
    PUBLIC
*/

Module::Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint8_t> data, const char * name):
nmodule(nmodule),
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels),
fName(name)
{
    SetData(data);
}

Module::Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint16_t> data, const char * name):
nmodule(nmodule),
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels),
fName(name)
{
    SetData(data);
}

Module::Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, std::vector<uint32_t> data, const char * name):
nmodule(nmodule),
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels),
fName(name)
{
    SetData(data);
}

Module::Module(const int nmodule, unsigned nBits, unsigned nChannels, unsigned ActiveChannels, const char * name):
nmodule(nmodule),
fBits(nBits), 
fChannels(nChannels),
fActiveChannels(ActiveChannels),
fName(name)
{}

/*
void Module::importData(NewDumper& dumpy, unsigned eventnumber, unsigned nmodules)
{
    const unsigned int start=0,stop=0,pos=0;
    pos=// per ogni modulo precedente fBits/8* fnChannels devi prenderli da event c
    //c'è vettore con tutti i moduli fino all'elemento che è il numero del modulo attuale. IL MORTO DICE FINITO
    for(int a=0;a<nmodule;a++)
    {

    }



    start=16+64*nmodules+dumpy.getEventPosition(eventnumber)+pos;


    if((fBits/8)==1)
    { 
        fData8bit=dumpy.readData<uint8_t>(start,stop);
    }
    else
    {
        if((fBits/8)==2)
        {
            fData16bit=dumpy.readData<uint16_t>(start,stop);
        }
        else
        {
            if((fBits/8)==4) fData32bit=dumpy.readData<uint32_t>(start,stop);
            else cout<<"Something goes wrong"<<endl;
        }
    }

}*/


Module& Module::SetData(std::vector<uint8_t> data)
{
    //CheckData(data);
    for(auto i: data)   std::cout << std::hex << i << " ";
    std::cout << std::endl;
    fData8bit=data;
    return *this;
}

Module& Module::SetData(std::vector<uint16_t> data)
{
    //CheckData(data);
    for(auto i: data)   std::cout << std::hex << i << " ";
    std::cout << std::endl;
    fData16bit=data;
    return *this;
}

Module& Module::SetData(std::vector<uint32_t> data)
{
    //CheckData(data);
    for(auto i: data)   std::cout << std::hex << i << " ";
    std::cout << std::endl;
    fData32bit=data;
    return *this;
}


Module& Module::Print()
{
    std::cout << "Module " << nmodule << " : " << fName << "\n";
    std::cout<<"[ ";
    if(fBits == 8)  
    {
        std::cout << "fBits = " << fBits << std::endl;
        for(uint8_t i: fData8bit) std::cout << i << " ";
    }
    else if(fBits == 16)  
    {
        std::cout << "fBits = " << fBits << std::endl;
        for(uint16_t i: fData16bit) std::cout << i << " ";
    }
    else if(fBits == 32)
    {
        std::cout << "fBits = " << fBits << std::endl;
        for(uint32_t i: fData32bit) std::cout << i << " ";
    }
    std::cout<<"] ";
    
    return *this;
}


/*
    PRIVATE
*/


void Module::CheckData(std::vector<uint8_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}

void Module::CheckData(std::vector<uint16_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}

void Module::CheckData(std::vector<uint32_t> data)
{
    if (data.size()!=fActiveChannels)
        throw runtime_error("The number of data is different from the one specified as ActiveChannels");
}




