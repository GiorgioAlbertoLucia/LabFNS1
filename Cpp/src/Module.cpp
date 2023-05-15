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

Module::Module(const Module& mod)
{
    nmodule = mod.nmodule;
    fBits = mod.fBits;
    fChannels = mod.fChannels;
    fActiveChannels = mod.fActiveChannels;
    fName = mod.fName;

    switch(fBits)
    {
        case 8:     fData8bit = mod.fData8bit;
        case 16:    
        {
            fData16bit = mod.fData16bit;
            std::cout << "copy const cout\n";
            for(auto i: mod.fData16bit)     printf("%02X ", i);
            std::cout << "\n";
            std::cout << "copy const cout\n";
            for(auto i:fData16bit)          printf("%02X ", i);
            std::cout << "\n";
        }
        case 32: 
        {
            fData32bit = mod.fData32bit;
            std::cout << "copy const cout\n";
            for(auto i: mod.fData16bit)     printf("%02X ", i);
            std::cout << "\n";
            std::cout << "copy const cout\n";
            for(auto i:fData16bit)          printf("%02X ", i);
            std::cout << "\n";
        }
    }

}

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
    for(auto i: data)  printf("%02X ", i);
    std::cout << std::endl;
    fData8bit=data;
    std::cout << "vec 8 bit size = " << fData8bit.size() << "\n";
    return *this;
}

Module& Module::SetData(std::vector<uint16_t> data)
{
    //CheckData(data);
    for(auto i: data)   printf("%02X ", i);
    std::cout << std::endl;
    fData16bit=data;
    std::cout << "vec 16 bit size = " << fData16bit.size() << "\n";
    return *this;
}

Module& Module::SetData(std::vector<uint32_t> data)
{
    //CheckData(data);
    for(auto i: data)   printf("%02X ", i);
    std::cout << std::endl;
    fData32bit=data;
    std::cout << "vec 32 bit size = " << fData32bit.size() << "\n";
    return *this;
}


Module& Module::Print()
{
    std::cout << "Module " << nmodule << " : " << fName << "\n";
    std::cout<<"[ ";
    if(fBits == 8)  
    {
        std::cout << "fBits = " << fBits << std::endl;
        std::cout << "vec size 8 bit = " << fData8bit.size() << "\n";
        std::cout << "vec size 16 bit = " << fData16bit.size() << "\n";
        std::cout << "vec size 32 bit = " << fData32bit.size() << "\n";
        for(uint8_t i: fData8bit) std::cout << std::hex << i << " ";
    }
    else if(fBits == 16)  
    {
        std::cout << "fBits = " << fBits << std::endl;
        std::cout << "vec size 8 bit = " << fData8bit.size() << "\n";
        std::cout << "vec size 16 bit = " << fData16bit.size() << "\n";
        std::cout << "vec size 32 bit = " << fData32bit.size() << "\n";
        for(uint16_t i: fData16bit) std::cout << std::hex << i << " ";
    }
    else if(fBits == 32)
    {
        std::cout << "fBits = " << fBits << std::endl;
        std::cout << "vec size 8 bit = " << fData8bit.size() << "\n";
        std::cout << "vec size 16 bit = " << fData16bit.size() << "\n";
        std::cout << "vec size 32 bit = " << fData32bit.size() << "\n";
        for(uint32_t i: fData32bit) std::cout << std::hex << i << " ";
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


void Module::SetBranchAddress(TTree& tree, unsigned countmodule)
{
/*
 *  Function that sets the address of the branch of the output tree to the
 *  vectors containing the intersections
 *  -------------------------
 *  Parameters:
 *  tree: TTree&
 *      Tree for data output
 * 
 *  countmodule: unsigned
 *      running count of modules
 * 
 */
    switch (fBits)
    {
    case 8:
        for (unsigned i=0; i<fData8bit.size(); i++)
        {
            tree.SetBranchAddress((std::string("Module")+std::to_string(countmodule)+"_"+std::to_string(i)).c_str(), (uint8_t*) &fData8bit[i]);
        }
        break;
    
    case 16:
        for (unsigned i=0; i<fData16bit.size(); i++)
        {
            tree.SetBranchAddress((std::string("Module")+std::to_string(countmodule)+"_"+std::to_string(i)).c_str(), (uint16_t*) &fData16bit[i]);
        }
        break;
    
    case 32:
        for (unsigned i=0; i<fData32bit.size(); i++)
        {
            tree.SetBranchAddress((std::string("Module")+std::to_string(countmodule)+"_"+std::to_string(i)).c_str(), (uint32_t*) &fData32bit[i]);
        }        break;
    
    default:
        break;
    }
}
