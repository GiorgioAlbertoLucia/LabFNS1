#include "Event.h"
#include "vector"



Event::Event()
{}

Event::Event(unsigned evenumb ,unsigned nmodules, vector<unsigned> &vectortype, std::vector<unsigned>& nchan, NewDumper &Newdumpy):
fNmodules(nmodules),
fDataTypesVector(vectortype),
fEventNumber(evenumb)
{
    for(int ii=0;ii<nmodules;ii++)
    {
        unsigned int start=0,stop=0,offset=0;
        
        if(ii>0)
        {
            for(int a=0;a<ii;a++)
            {
                offset=offset+unsigned(fmodulesvector[a].GetChannels()*fDataTypesVector[a]/8);
            }
        }
        start=16+64*nmodules+Newdumpy.getEventPosition(fEventNumber)+offset;
        stop=start+unsigned(fmodulesvector[ii].GetChannels()*fDataTypesVector[ii]/8);

        Module mod(ii,vectortype[ii],nchan[ii], 0);
        if(vectortype[ii]==8) 
        {
            std::vector<uint8_t> temp = Newdumpy.readData<uint8_t>(start,stop);
            mod.SetData(temp);
        }
        if(vectortype[ii]==16) 
        {
            std::vector<uint16_t> temp = Newdumpy.readData<uint16_t>(start,stop);
            mod.SetData(temp);
        }
        else
        {
            if(vectortype[ii]==32) 
            {
                std::vector<uint32_t> temp = Newdumpy.readData<uint32_t>(start,stop);
                mod.SetData(temp);
            }
            else cout<<"something goes wrong"<<endl;
        }
        fmodulesvector.push_back(mod);
    }


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

/*
Event& Event::SetModuleNDouble(unsigned n, std::vector<double> Data)
{
    if (fDataTypesVector.size()>n && fDataTypesVector[n]==fDouble)
    {
        fDataVector newdata;
        for (auto i: Data)
            newdata.push_back(i);
        SetModuleNData(n, newdata);
    }
    else if (fDataTypesVector[n]!=fDouble)
        std::cout<<"\033[93mThe "<<n<<" th module does not store double data\033[0m"<<std::endl;
    else if (fDataTypesVector.size()<=n)
        std::cout<<"\033[93mThe "<<n<<" th data type is not specified\033[0m"<<std::endl;    
    return *this;
}

Event& Event::SetModuleNUnsigned(unsigned n, std::vector<unsigned> Data)
{
    if (fDataTypesVector.size()>n && fDataTypesVector[n]==fUnsigned)
    {
        fDataVector newdata;
        for (auto i: Data)
            newdata.push_back(i);
        SetModuleNData(n, newdata);
    }
    else if (fDataTypesVector[n]!=fUnsigned)
        std::cout<<"\033[93mThe "<<n<<" th module does not store unsigned data\033[0m"<<std::endl;
    else if (fDataTypesVector.size()<=n)
        std::cout<<"\033[93mThe "<<n<<" th data type is not specified\033[0m"<<std::endl;   
    return *this;
}


std::vector<double> Event::GetModuleNDouble(unsigned n)      
{
    std::vector<double> vec;
    for (auto i:fData[n])
        vec.push_back(std::get<double>(i));
    return vec;
}

std::vector<unsigned> Event::GetModuleNUnsigned(unsigned n)      
{
    std::vector<unsigned> vec;
    for (auto i:fData[n])
        vec.push_back(std::get<unsigned>(i));
    return vec;
}
*/