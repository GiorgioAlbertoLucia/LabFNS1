//#include "Event.hpp"
#include "Run.hpp"


Run::Run(std::string cfgFileName) :
fTreeData("TreeData","TreeData")
{
    Yaml::Parse(fConfigFile, cfgFileName.c_str());
    NewDumper dumpy(fConfigFile["DataFileName"].As<std::string>().c_str());
    fEv = Event(0,cfgFileName,dumpy);
    TFile outfile(fConfigFile["TTreeFileName"].As<std::string>().c_str(),"recreate");
    fTreeData.SetDirectory(&outfile);
    TreeSettings();
    std::cout<<dumpy.getNEvents()<<std::endl;
    for (unsigned i=0; i<dumpy.getNEvents(); i++)
    {
        if (i!=0)
            fEv.Next();
        fEv.Print();
        fTreeData.Fill();
    }
    fTreeData.Write("fTreeData",1ULL << ( 2 ));
    outfile.Close();

    /*
    Yaml::Parse(fConfigFile, cfgFileName.c_str());
    fDataFileName = fConfigFile["DataFileName"].As<std::string>();
    fNmodules = fConfigFile["NModules"].As<unsigned>();

    Yaml::Node& modules = fConfigFile["Modules"];
    for(auto it = modules.Begin(); it != modules.End(); it++)
    {
        Yaml::Node& ModuleSetting = (*it).second;
        fModules.push_back(Module(fModules.size(),ModuleSetting["Bits"].As<unsigned>(), ModuleSetting["Channels"].As<unsigned>(), 
            ModuleSetting["ActiveChannels"].As<unsigned>(), std::vector<uint16_t>{1,2}));
    }

    TFile outfile(fConfigFile["TTreeFileName"].As<std::string>().c_str(),"recreate");
    fTreeData.SetDirectory(&outfile);
    TreeSettings();
    for (int i = 0; i < 40000; i++)
    {
        for (auto& i: fModules)
            i.SetData(std::vector<uint16_t>{(uint16_t)gRandom->Integer(100),(uint16_t)gRandom->Integer(100)});
        fTreeData.Fill();
    }
    
    fTreeData.Write("fTreeData",1ULL << ( 2 ));     // 1ULL << ( 2 ) = TObject's kWriteDelete
    //fTreeData.Write("fTreeData");     // 1ULL << ( 2 ) = TObject's kWriteDelete
    outfile.Close();

    std::string outpath = "../../../data/input/";
    std::string filepath = outpath + fDataFileName;

    */
}


void Run::TreeSettings()
{
    uint8_t   ptr8bit;                  //used to define Branch type
    uint16_t  ptr16bit;                 //used to define Branch type
    uint32_t  ptr32bit;                 //used to define Branch type

    std::cout<<"Nmodules: "<<fEv.GetNmodules()<<std::endl;
    for (unsigned idxModules = 0; idxModules<fEv.GetNmodules(); idxModules++)
    {
        switch (fEv.getModule(idxModules).GetBits())
        {
        case 8:
            for (unsigned idxChannel=0; idxChannel<fEv.getModule(idxModules).GetActiveChannels(); idxChannel++)
                fTreeData.Branch((std::string("Module")+std::to_string(idxModules)+"_"+std::to_string(idxChannel)).c_str(), &ptr8bit, 32000);

            break;

        case 16:
            for (unsigned idxChannel=0; idxChannel<fEv.getModule(idxModules).GetActiveChannels(); idxChannel++)
                fTreeData.Branch((std::string("Module")+std::to_string(idxModules)+"_"+std::to_string(idxChannel)).c_str(), &ptr16bit, 32000);

            break;

        case 32:
            for (unsigned idxChannel=0; idxChannel<fEv.getModule(idxModules).GetActiveChannels(); idxChannel++)
                fTreeData.Branch((std::string("Module")+std::to_string(idxModules)+"_"+std::to_string(idxChannel)).c_str(), &ptr32bit, 32000);

            break;
        
        default:
            throw runtime_error("Only 8, 16 and 32 bit data is supported");
            break;
        }
    }

    fEv.SetBranchAddress(fTreeData);
}