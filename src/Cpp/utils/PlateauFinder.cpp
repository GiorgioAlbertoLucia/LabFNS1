// script che aiuta a capire fin dove si ha un andamento lineare

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

void PlateauFinder::FindPlateau()
{
    for (int i = 2; i <= fNpoints; i++)
    {
        if (fDirection == "up")
            fFits.push_back(new TF1((std::string("function")+std::to_string(i)).c_str(), "[0]+[1]*x", fXmin, fHisto->GetBinCenter(i)));

        else if (fDirection == "down")
            fFits.push_back(new TF1((std::string("function")+std::to_string(i)).c_str(), "[0]+[1]*x", fHisto->GetBinCenter(fNpoints-i+1), fXmax));
        
        fCanvas->cd(i - 1);

        TH1D* ClonedHisto = (TH1D*)(fHisto->DrawCopy("",""));
        ClonedHisto -> Fit(fFits.back(),"RQ");

        std::cout << "Chi^2:" << fFits.back()->GetChisquare() << ", number of DoF: " << fFits.back()->GetNDF() <<
                ", Chi^2 @ confidence level 5%: "<< ROOT::Math::chisquared_quantile_c(0.05,fFits.back()->GetNDF());
        
        if (fFits.back()->GetChisquare() <= ROOT::Math::chisquared_quantile_c(0.05,fFits.back()->GetNDF()))
            std::cout<<"\t-> PASSED";
        else 
            std::cout<<"\t-> FAILED";

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