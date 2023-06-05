import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TLegend, gStyle, TArrow, kGray, TLatex, TF1
from ReadMCA import DictHistos, FitStats

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.1, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=0.9, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

if __name__ == "__main__":

    infilename = 'data/input/Diamond/Stronzio/stronzio.mca'
    histofile = TFile('data/input/Diamond/Stronzio/StrontiumHistoEn1000.root', 'recreate')

    dict = {'Stronzio': [infilename,"en1000"]}
    color = kAzure-7
    DictHistos(dict, histofile, color, 8)

    # ENERGY LOSS DIAMOND 2.2 MeV
    # StopPowerDiamondElectronsNIST = 1.617 (MeV*cm2)/(g)
    StopPowerDiamondElectronsNIST = 1617 # (KeV*cm2)/(g)
    RhoDiamond = 3.52 # g/cm3
    DiamondThickness = 0.05 #cm
    EnergyLoss = StopPowerDiamondElectronsNIST*RhoDiamond*DiamondThickness
    print(EnergyLoss)

    StrontiumHistoCanva = TCanvas('MCA distribution counts', 'MCA distribution counts',1280,760)
    hFrame = StrontiumHistoCanva.DrawFrame(71.74,0.,dict['Stronzio'][1].GetBinCenter(dict['Stronzio'][1].GetNbinsX()-1),2000,"MCA counts distribution; E[keV]; Counts")
    SetObjectStyle(dict['Stronzio'][1],color=kAzure+3,fillalpha=0.5,linewidth=1)
    #dict['Stronzio'][1].Scale(1/dict['Stronzio'][1].GetMaximum())
    dict['Stronzio'][1].Draw("hist,same")
    Title =TLatex(0.56, 0.55,"^{90}Sr spectrum")
    Title.SetNDC()
    Title.SetTextSize(gStyle.GetTextSize()*1.1)
    Title.SetTextFont(42)
    Title.Draw()
    Title1 =TLatex(0.56, 0.50,"Acquisition time: 1200s")
    Title1.SetNDC()
    Title1.SetTextSize(gStyle.GetTextSize()*0.7)
    Title1.SetTextFont(42)
    Title1.Draw()
    StrontiumHistoCanva.Modified()
    StrontiumHistoCanva.Update()
    StrontiumHistoCanva.SaveAs('data/output/Diamond/StrontiumHisto.pdf')

    canvas = TCanvas("StrontiumElectrons", "c" ,1280, 720)
    FitLowBound1 = 250
    FitUppBound1 = 350
    #gStyle.SetTitleSize(3)
    Gaussian1 = TF1("f1","gaus(0)", FitLowBound1, FitUppBound1)
    Gaussian1.SetLineColor(kRed)
    Gaussian1.SetLineWidth(3)
    dict['Stronzio'][1].Fit(Gaussian1,"RM+","", FitLowBound1, FitUppBound1)
    FitStats(Gaussian1)

    FitLowBound2 = 110
    FitUppBound2 = 190
    #gStyle.SetTitleSize(3)
    Gaussian2 = TF1("f2","gaus(0)", FitLowBound2, FitUppBound2)
    Gaussian2.SetLineColor(kViolet)
    Gaussian2.SetLineWidth(3)
    dict['Stronzio'][1].Fit(Gaussian2,"RM+","", FitLowBound2, FitUppBound2)
    FitStats(Gaussian2)

    leg = TLegend(0.67, 0.6, 0.82, 0.8)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    leg.AddEntry(dict['Stronzio'][1], 'Data', 'lep')
    leg.AddEntry(Gaussian1, 'Average energy loss fit', 'lf')
    leg.AddEntry(Gaussian2, '0.54 MeV Beta peak fit', 'lf')
    
    hframe = canvas.DrawFrame(71.74,0.5,600,2400,"Strontium peaks fits; E[keV]; Counts")
    dict['Stronzio'][1].SetLineColor(kAzure-7)
    dict['Stronzio'][1].SetMarkerColor(kAzure-7)
    dict['Stronzio'][1].Draw("hist,p,e,same")
    Gaussian1.Draw("same")
    Gaussian2.Draw("same")
    leg.Draw("same")
    canvas.SaveAs('data/output/Diamond/AverageEnergyLossStrontium.pdf')