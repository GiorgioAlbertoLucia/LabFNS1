#include <TFile.h>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include<TF1.h>
#include <TMath.h>

void effi(){

    TFile file("data/output/HVeffSG.root");
    TCanvas * c = (TCanvas*)file.Get("c1");
    c->cd();
    TGraphErrors* g = (TGraphErrors*)c->GetListOfPrimitives()->FindObject("Graph");
    TF1*funz = new TF1("funz","([0]/(1+ TMath::Exp(-[1]*(x-[2]))", 1100, 1900);
    funz->SetParameter(0,0.7);
    funz->SetParameter(2,1200);
    funz->SetLineColor(2); // Rosso
    g->Fit(funz,"RM+");
    g->Draw("AP");




}