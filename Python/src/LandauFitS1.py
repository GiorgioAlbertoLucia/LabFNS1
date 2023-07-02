import sys
import pandas as pd
import numpy as np
import uproot
from ROOT import TH1D, TH2D, TF1, TCanvas, kAzure, kRed, kGreen, kSpring, Math, kBlack, kDarkBodyRadiator, TLegend, TLatex, TLine, TText, gStyle, gPad, gROOT
sys.path.append('Python/utils')
from Pedestal import DrawPedestral
from StyleFormatter import SetGlobalStyle, SetObjectStyle

gROOT.SetBatch()

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

Tree=uproot.open("data/input/DataFullRun.root")["fTreeData"]

Df=Tree.arrays(library='pd')

Df=Df[["Module4_10","Module4_11","Module5_0"]]
DfPassed=Df.query("Module5_0==0")

cS1 = TCanvas("S1","S1",1500,1000)
yMincS1 = 0.0001
yMaxcS1 = 0.01
hFrame = cS1.DrawFrame(Df["Module4_10"].min()*0.9,yMincS1,Df["Module4_10"].max()*1.02,yMaxcS1,"ADC Normalised counts; Channel; Counts")

hS1Passed = TH1D("hS1Passed","hS1Passed",2048,0,2048)
hS1Passed.FillN(len(DfPassed["Module4_10"]),np.asarray(DfPassed["Module4_10"],'d'),np.asarray([1]*len(DfPassed["Module4_10"]),'d'))
hS1Passed.Scale(1/len(DfPassed))
hS1Passed.Rebin(2)
SetObjectStyle(hS1Passed,color=kAzure+3,fillalpha=0.5,linewidth=1)
hS1Passed.Draw("hist,same")

landau = TF1("landau","[0]*TMath::Landau(x,[1],[2],0)+gaus(3)",360,800)
landau.SetParameters(1.81279e-01,444,47,0.)
SetObjectStyle(landau,color=kRed, linewidth=2)
#landau.FixParameter(0,0.0475)
#landau.FixParameter(2,47)
hS1Passed.Fit(landau,"RM")

leg = TLegend(0.435, 0.71, 0.85, 0.59)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("S1 Normalised counts")
leg.AddEntry(hS1Passed, 'S1 ADC distribution', 'lf')
leg.AddEntry(landau, 'Landau fit', 'l')
leg.Draw("same")

text =TLatex(0.45, 0.73,"S1 Scintillator + PMXP2020")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.55,"Using V259 pattern unit")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.49,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.45, 0.43,"Discriminator threshold value: (#font[122]{-}39.6 #pm 0.5) mV")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()


print('Chi2 = ', landau.GetChisquare())
print('NDF = ', landau.GetNDF())
print('p-value = ', landau.GetProb())
print('Critical Chi2 = ', Math.chisquared_quantile_c(0.05,landau.GetNDF()))

landau.Draw("same")

cS1.Draw()
cS1.SaveAs("data/output/Figures/MuonLifetime/LandauS1.png","recreate")