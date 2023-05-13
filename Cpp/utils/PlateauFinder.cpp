// Script for finding a linear plateau

#include "PlateauFinder.h"

PlateauFinder::PlateauFinder(): fOutname("out.pdf"), fDirection("up") 
{
    fHisto = PlateauFinder::FakeHistoforTest();
    fNpoints = fHisto->GetNbinsX();
    fCanvas = new TCanvas("Canvas", "Canvas", 1280, 720);
    fCanvas->Divide(4, (fNpoints - 2) % 4 == 0 ? (fNpoints - 2) / 4 : (fNpoints - 2) / 4 + 1);
    fCanvas->SetFillColor(0);
    fXmin = fHisto->GetBinCenter(1);
    fXmax = fHisto->GetBinCenter(fNpoints);
}


PlateauFinder::PlateauFinder(TH1D* histo, std::string direction, std::string outname): fHisto(histo), fOutname(outname), fDirection(direction) 
{
    fNpoints = fHisto->GetNbinsX();
    fCanvas = new TCanvas("Canvas", "Canvas", 1280, 720);
    fCanvas->Divide(4, (fNpoints - 2) % 4 == 0 ? (fNpoints - 2) / 4 : (fNpoints - 2) / 4 + 1);
    fCanvas->SetFillColor(0);
    fXmin = fHisto->GetBinCenter(1);
    fXmax = fHisto->GetBinCenter(fNpoints);
}

PlateauFinder::PlateauFinder(TH1D* histo, std::string direction, double xmax, double xmin, std::string outname): 
fHisto(histo), fOutname(outname), fDirection(direction), fXmax(xmax), fXmin(xmin)       //TODO: add checks on xmax and xmin
{
    fNpoints = fHisto->GetNbinsX();
    fCanvas = new TCanvas("Canvas", "Canvas", 1280, 720);
    fCanvas->Divide(4, (fNpoints - 2) % 4 == 0 ? (fNpoints - 2) / 4 : (fNpoints - 2) / 4 + 1);
    fCanvas->SetFillColor(0);
}

/**
 * @brief Function that runs the "algorithm" for finding the plateau
 */
void PlateauFinder::FindPlateau()
{
    for (int i = 2; i <= fNpoints; i++)
    {
        // Creates fitting function and adds it to fFits
        if (fDirection == "up")
            fFits.push_back(new TF1((std::string("function")+std::to_string(i)).c_str(), "[0]+[1]*x", fXmin, fHisto->GetBinCenter(i)));

        else if (fDirection == "down")
            fFits.push_back(new TF1((std::string("function")+std::to_string(i)).c_str(), "[0]+[1]*x", fHisto->GetBinCenter(fNpoints-i+1), fXmax));
        
        // Opens pad
        fCanvas->cd(i - 1);

        TH1D* ClonedHisto = (TH1D*)(fHisto->DrawCopy("",""));
        ClonedHisto -> SetStats(0);
        ClonedHisto -> Fit(fFits.back(),"RQ");

        std::cout << "Chi^2:" << std::fixed << std::setprecision(5) <<fFits.back()->GetChisquare() << ", number of DoF: " << fFits.back()->GetNDF() <<
                ", Chi^2 @ confidence level 5%: "<< ROOT::Math::chisquared_quantile_c(0.05,fFits.back()->GetNDF());
        
        // Checks whether the chi^2 test succedeed
        if ((fFits.back()->GetChisquare() - ROOT::Math::chisquared_quantile_c(0.05,fFits.back()->GetNDF())) < 1e-6)
        {
            std::cout<<"\t-> PASSED";
            fPassed.push_back(true);
        }
        else 
        {
            std::cout<<"\t-> FAILED";
            fPassed.push_back(false);
        }

        std::cout<< "." << std::endl;
        std::cout << "--------------------------------------------------------------------------------------------------------" << std::endl;
    }
    fCanvas->cd();
    fCanvas->Draw();
}

TH1D* PlateauFinder::FakeHistoforTest()
{
    double x[] = {1,2,3,4,5,6,7,8,9};
    double y[] = {1,2,3,4,5,5.01,5.02,5.03};
    double sigy[] = {0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1};

    TH1D* histo = new TH1D("histo","histo", (sizeof(x)/sizeof(*x))-1, x);
    for (int i=0; i<9;i++)
    {
        histo->Fill(x[i],y[i]);
        histo->SetBinError(i+1,sigy[i]);
    }
    return histo;
}

/**
 * @brief Function that returns the x position of the first point at which the chi^2 test failed
 * 
 * @return double 
 */
double PlateauFinder::GetxFirstFailed()
{
    for (unsigned i=0; i<fPassed.size(); i++)
    {
        if (!fPassed[i])
        {
            if (fDirection=="up")
                // if fPassed[0] is false, then test failed when considering the 1st+2nd bins -> i+2
                return fHisto->GetBinCenter(i+2);
            else
                // if fPassed[0] is false, then test failed when considering the fNpoints-th+(fNpoints-1)-th bins -> fNpoints-1-i
                return fHisto->GetBinCenter(fNpoints-1-i);
        }

    }
    std::cout<<"\033[93mThe test hasn't failed, returning 0\033[0m"<<std::endl;
    return 0;
}