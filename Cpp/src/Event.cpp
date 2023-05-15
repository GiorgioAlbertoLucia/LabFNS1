#include "Event.h"
#include "vector"

/*
    PROTECTED
*/

/**
 * @brief Initialize data members of the Event class and fill data into the modules.
 * 
 * @param vectortype 
 * @param nchan 
 */
void Event::InitializeEvent(NewDumper& Newdumpy)
{
    for(unsigned ii=0;ii<fNmodules;ii++)
    {
        unsigned int start=0,stop=0,offset=0;
        
        if(ii>0)
        {
            for(unsigned a=0;a<ii;a++)
            {
                offset=offset+unsigned(fmodulesvector[a].GetChannels()*fmodulesvector[a].GetBits()/8);
            }
        }
        Module& mod = fmodulesvector[ii];
        std::cout << "check bits: " << mod.GetBits() << "\n";
        start=16+64*fNmodules+Newdumpy.getEventPosition(fEventNumber)+offset;
        stop=start+unsigned(mod.GetChannels()*mod.GetBits()/8);

        printf("start = %d\n", start);
        printf("stop = %d\n", stop);
        printf("offset = %d\n", offset);
        
        if(mod.GetBits()==8) 
        {
            std::vector<uint8_t> temp = Newdumpy.readData<uint8_t>(start,stop);
            mod.SetData(temp);
        }
        if(mod.GetBits()==16) 
        {
            std::vector<uint16_t> temp = Newdumpy.readData<uint16_t>(start,stop);
            mod.SetData(temp);
        }
        else
        {
            if(mod.GetBits()==32) 
            {
                std::vector<uint32_t> temp = Newdumpy.readData<uint32_t>(start,stop);
                mod.SetData(temp);
            }
            else cout<<"something goes wrong"<<endl;
        }
    }
}

/*
    PUBLIC
*/

Event::Event()
{}

Event::Event(unsigned evenumb ,unsigned nmodules, std::vector<unsigned> &vectortype, std::vector<unsigned>& nchan, NewDumper& Newdumpy):
fNmodules(nmodules),
fEventNumber(evenumb)
{
    for(unsigned ii=0;ii<fNmodules;ii++) 
    {
        Module mod(ii,vectortype[ii],nchan[ii], 0);
        fmodulesvector.push_back(mod);
    }

    InitializeEvent(Newdumpy);
}

Event::Event(unsigned eventNumber, std::string cfgFileName, NewDumper& dumpy):
fEventNumber(eventNumber)
{
    Yaml::Parse(fConfigFile ,cfgFileName.c_str());
    fNmodules = fConfigFile["NModules"].As<unsigned>();
    fmodulesvector.reserve(fNmodules);

    Yaml::Node& modules = fConfigFile["Modules"];
    //Creates vector of modules with the settings from config file
    int nmodule = 0;
    for(auto it = modules.Begin(); it != modules.End(); it++)
    {
        Yaml::Node& ModuleSetting = (*it).second;
        Module mod(nmodule, ModuleSetting["Bits"].As<unsigned>(), ModuleSetting["Channels"].As<unsigned>(), 
            ModuleSetting["ActiveChannels"].As<unsigned>(), ModuleSetting["Name"].As<std::string>().c_str());
        fmodulesvector.push_back(mod);
        nmodule++;
    }

    InitializeEvent(dumpy);
    Print();
}

/**
 * @brief Function that checks the CAMAC Q state of the modules
 * 
 * @return bool 
 */
bool Event::CheckStatus()
{
    for (unsigned i=0; i<fNmodules; i++)
        // Checks if leftmost bit which has not been checked yet is equal to 1
        if (! (1 & fStatus>>(15-i)))
            return false;
    return true;
}

Event& Event::SetNmodules(unsigned Nmodules)
{
    fNmodules=Nmodules;
    //if (fData.size()>0)
    //    std::cout<<"\033[93mChanging the number of modules deletes the existing data, be careful!\033[0m"<<std::endl;
    //fData.clear();
    //for (unsigned i=0; i<fNmodules; i++)
    //    fData.push_back({});
    return *this;
}

Event& Event::Print()
{
    for (unsigned i=0; i<fmodulesvector.size(); i++)
    {
        fmodulesvector[i].Print();
        std::cout<<std::endl;
    }
    return *this;
}