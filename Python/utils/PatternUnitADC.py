import pandas as pd
import numpy as np
import uproot
from ROOT import TH1D, TCanvas, kAzure, kRed, TLegend, TLatex, gStyle

from StyleFormatter import SetGlobalStyle, SetObjectStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

Tree=uproot.open("/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/data/input/Test.root")["fTreeData"]

##########
#   S1   #
##########

Df=Tree.arrays(library='pd')

Df=Df[["Module4_10","Module4_11","Module5_0"]]
DfPassed=Df.query("Module5_0==1")

cS1 = TCanvas("S1","S1",1500,1500)
hFrame = cS1.DrawFrame(Df["Module4_10"].min()*0.9,0.0001,Df["Module4_10"].max()*1.02,0.01,"S1 Normalised counts; Channel; Counts")
hS1All = TH1D("hS1All","hS1All",2048,0,2048)
hS1All.FillN(len(Df["Module4_10"]),np.asarray(Df["Module4_10"],'d'),np.asarray([1]*len(Df["Module4_10"]),'d'))
hS1All.Scale(1/len(Df))
hS1All.Rebin(2)
SetObjectStyle(hS1All,color=kAzure+3,fillalpha=0.9,linewidth=1)

hS1All.Draw("hist,same")

hS1Passed = TH1D("hS1Passed","hS1Passed",2048,0,2048)
hS1Passed.FillN(len(DfPassed["Module4_10"]),np.asarray(DfPassed["Module4_10"],'d'),np.asarray([1]*len(DfPassed["Module4_10"]),'d'))
hS1Passed.Scale(1/len(DfPassed))
hS1Passed.Rebin(2)
SetObjectStyle(hS1Passed,color=kRed,fillalpha=0.5,linewidth=1)
hS1Passed.Draw("hist,same")

leg = TLegend(0.435, 0.71, 0.85, 0.59)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("S1 Normalised counts")
leg.AddEntry(hS1All, 'Without SG inhibit', 'lf')
leg.AddEntry(hS1Passed, 'With SG inhibit', 'lf')
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
text3 =TLatex(0.45, 0.49,"Acquisition time: 300 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.45, 0.43,"Discriminator threshold value: (-39.6 #pm 0.5) mV")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()


cS1.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cS1.pdf')



##########
#   SG   #
##########

cSG = TCanvas("SG","SG",1500,1500)
hFrame = cSG.DrawFrame(Df["Module4_11"].min()*0.9,0.0001,Df["Module4_11"].max()*1.02,0.006,"SG Normalised counts; Channel; Counts")
hSGAll = TH1D("hSGAll","hSGAll",2048,0,2048)
hSGAll.FillN(len(Df["Module4_11"]),np.asarray(Df["Module4_11"],'d'),np.asarray([1]*len(Df["Module4_11"]),'d'))
hSGAll.Scale(1/len(Df))
hSGAll.Rebin(2)
SetObjectStyle(hSGAll,color=kAzure+3,fillalpha=0.9,linewidth=1)

hSGAll.Draw("hist,same")

DfPassed=Df.query("Module5_0==1")
hSGPassed = TH1D("hSGPassed","hSGPassed",2048,0,2048)
hSGPassed.FillN(len(DfPassed["Module4_11"]),np.asarray(DfPassed["Module4_11"],'d'),np.asarray([1]*len(DfPassed["Module4_11"]),'d'))
hSGPassed.Scale(1/len(DfPassed))
hSGPassed.Rebin(2)
SetObjectStyle(hSGPassed,color=kRed,fillalpha=0.5,linewidth=1)
hSGPassed.Draw("hist,same")

leg = TLegend(0.465, 0.81, 0.85, 0.69)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("SG Normalised counts")
leg.AddEntry(hSGAll, 'Without S2 inhibit', 'lf')
leg.AddEntry(hSGPassed, 'With S2 inhibit', 'lf')
leg.Draw("same")

text =TLatex(0.48, 0.83,"SG Scintillator + PM R1513")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.48, 0.65,"Using V259 pattern unit")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.48, 0.59,"Acquisition time: 300 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.48, 0.53,"Discriminator threshold value: (-10.2 #pm 0.5) mV")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()


cSG.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cSG.pdf')