/*
 *  Finds linear plateau based on chi^2 statistical test
 */

#ifndef PLATEAUFINDER_H
#define PLATEAUFINDER_H

#include <iostream>
#include <iomanip>
#include <TH1D.h>
#include <TF1.h>
#include <TCanvas.h>
#include <string>
#include <vector>
#include <TMath.h>

/**
 * @brief Class for finding linear plateau based on chi^2 statistical test
 * 
 */
class PlateauFinder
{
    public:
        PlateauFinder();
        PlateauFinder(TH1D* histo, std::string direction, std::string outname="out.pdf");
        PlateauFinder(TH1D* histo, std::string direction, double max, double min, std::string outname="out.pdf");
        ~PlateauFinder()    {for (unsigned i=0; i<fFits.size(); i++) delete fFits[i]; delete fCanvas;}
        
        void FindPlateau();
        TH1D* FakeHistoforTest();
        void DrawCanvas()                           {fCanvas->Draw();}
        void SaveCanvas()                           {fCanvas->SaveAs(fOutname.c_str());}

        void Sethisto(TH1D* histo)                  {fHisto=histo;}
        void SetXmin(double xmin)                   {fXmin=xmin;}
        void SetXmax(double xmax)                   {fXmax=xmax;}
        void SetOutname(std::string outname)        {fOutname=outname;}
        void SetDirection(std::string direction)    {fDirection=direction;}

        TH1D* GetHisto()                            {return fHisto;}
        std::vector<TF1*> GetFits()                 {return fFits;}
        std::string GetDirection()                  {return fDirection;}
        double GetxFirstFailed();
                             

    private:
        TH1D* fHisto;                       // Histogram containing the data points
        TCanvas* fCanvas;                   // Canvas with all the different fits
        std::string fOutname;               // Output name for printing fCanvas

        unsigned fNpoints;                  // Number of points in the desired range
        std::vector<TF1*> fFits;            // Vector containing fitting functions
        double fXmin, fXmax;                // Ranges for plateau finding
        std::string fDirection;             // "up" or "down", choose whether to fix min point or max point

        std::vector<bool> fPassed;          // Vector containg boolean variable set to true if the corresponding fit passed the chi^2 test

};

#endif
