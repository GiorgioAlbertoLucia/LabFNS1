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
        case 16:    fData16bit = mod.fData16bit;
        case 32:    fData32bit = mod.fData32bit;
    }

}


Module& Module::operator=(const Module& mod) noexcept
{
    if(this == &mod)    return *this;

    nmodule = mod.nmodule;
    fBits = mod.fBits;
    fChannels = mod.fChannels;
    fActiveChannels = mod.fActiveChannels;
    fName = mod.fName;

    switch(fBits)
    {
        case 8:     fData8bit = mod.fData8bit;
        case 16:    fData16bit = mod.fData16bit;
        case 32:    fData32bit = mod.fData32bit;
    }

    return *this;
}

std::ostream& operator<<(std::ostream& out, const Module& mod)
{
    out << "\033[93mModule " << mod.GetNmodule() << " : " << mod.GetName() << "\n";
    out<<"[ ";
    if(mod.GetBits() == 8)  
    {
        out << "fBits = " << mod.GetBits() << std::endl;
        out << "vec size 8 bit = " << mod.GetData8bit().size() << "\n";
        out << "vec size 16 bit = " << mod.GetData16bit().size() << "\n";
        out << "vec size 32 bit = " << mod.GetData32bit().size() << "\n";
        for(const uint8_t& i: mod.GetData8bit()) printf("%02X ", i);
    }
    else if(mod.GetBits() == 16)  
    {
        out << "fBits = " << mod.GetBits() << std::endl;
        out << "vec size 8 bit = " << mod.GetData8bit().size() << "\n";
        out << "vec size 16 bit = " << mod.GetData16bit().size() << "\n";
        out << "vec size 32 bit = " << mod.GetData32bit().size() << "\n";
        for(const uint16_t& i: mod.GetData16bit()) printf("%02X ", i);
    }
    else if(mod.GetBits() == 32)
    {
        out << "fBits = " << mod.GetBits() << std::endl;
        out << "vec size 8 bit = " << mod.GetData8bit().size() << "\n";
        out << "vec size 16 bit = " << mod.GetData16bit().size() << "\n";
        out << "vec size 32 bit = " << mod.GetData32bit().size() << "\n";
        for(const uint32_t& i: mod.GetData32bit()) printf("%02X ", i);
    }
    out << "] \033[0m";

    return out;
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
    fData8bit=data;
    return *this;
}

Module& Module::SetData(std::vector<uint16_t> data)
{
    //CheckData(data);
    fData16bit=data;
    return *this;
}

Module& Module::SetData(std::vector<uint32_t> data)
{
    //CheckData(data);
    fData32bit=data;
    return *this;
}


Module& Module::Print()
{
    std::cout << "\033[91mModule " << nmodule << " : " << fName << "\n";
    std::cout<<"[ ";
    if(fBits == 8)  
    {
        std::cout << "fBits = " << fBits << std::endl;
        std::cout << "vec size 8 bit = " << fData8bit.size() << "\n";
        std::cout << "vec size 16 bit = " << fData16bit.size() << "\n";
        std::cout << "vec size 32 bit = " << fData32bit.size() << "\n";
        for(const uint8_t& i: fData8bit) printf("%02X ", i);
    }
    else if(fBits == 16)  
    {
        std::cout << "fBits = " << fBits << std::endl;
        std::cout << "vec size 8 bit = " << fData8bit.size() << "\n";
        std::cout << "vec size 16 bit = " << fData16bit.size() << "\n";
        std::cout << "vec size 32 bit = " << fData32bit.size() << "\n";
        for(const uint16_t& i: fData16bit) printf("%02X ", i);
    }
    else if(fBits == 32)
    {
        std::cout << "fBits = " << fBits << std::endl;
        std::cout << "vec size 8 bit = " << fData8bit.size() << "\n";
        std::cout << "vec size 16 bit = " << fData16bit.size() << "\n";
        std::cout << "vec size 32 bit = " << fData32bit.size() << "\n";
        for(const uint32_t& i: fData32bit) printf("%02X ", i);
    }
    std::cout<<"] \033[0m";
    
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


void Module::SetBranchAddress(TTree& tree)
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
        for (unsigned i=0; i<fActiveChannels; i++)
            tree.SetBranchAddress((std::string("Module")+std::to_string(nmodule)+"_"+std::to_string(i)).c_str(), (uint8_t*) &fData8bit[i]);

        break;
    
    case 16:
        for (unsigned i=0; i<fActiveChannels; i++)
            tree.SetBranchAddress((std::string("Module")+std::to_string(nmodule)+"_"+std::to_string(i)).c_str(), (uint16_t*) &fData16bit[i]);

        break;
    
    case 32:
        for (unsigned i=0; i<fActiveChannels; i++)
            tree.SetBranchAddress((std::string("Module")+std::to_string(nmodule)+"_"+std::to_string(i)).c_str(), (uint32_t*) &fData32bit[i]);
        
        break;
    
    default:
        break;
    }
}
