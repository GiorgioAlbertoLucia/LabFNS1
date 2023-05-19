import sys
import pandas as pd
import numpy as np
import uproot
from ROOT import TH1D, TH2D, TCanvas, kAzure, kRed, kGreen, kSpring, kBlack, kDarkBodyRadiator, TLegend, TLatex, TLine, TText, gStyle, gPad, gROOT


sys.append
from ..utils.StyleFormatter import SetGlobalStyle, SetObjectStyle

#gROOT.SetBatch()

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

Tree=uproot.open("/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/data/input/DataFullRun.root")["fTreeData"]

##########
#   S1   #
##########

Df=Tree.arrays(library='pd')

Df=Df[["Module4_10","Module4_11","Module5_0"]]
DfPassed=Df.query("Module5_0==1")
DfNotPassed=Df.query("Module5_0==0")

cS1 = TCanvas("S1","S1",1500,1500)
yMincS1 = 0.0001
yMaxcS1 = 0.01
hFrame = cS1.DrawFrame(Df["Module4_10"].min()*0.9,yMincS1,Df["Module4_10"].max()*1.02,yMaxcS1,"ADC Normalised counts; Channel; Counts")
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
leg.AddEntry(hS1All, 'With and without S2 signal', 'lf')
leg.AddEntry(hS1Passed, 'Without S2 signal', 'lf')
leg.Draw("same")

text =TLatex(0.45, 0.73,"S1 Scintillator + PMXP2020")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.55,"Using V259 pattern unit #mu")
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

lineAtPedestal = TLine(245, gPad.GetUymax(), 245, gPad.GetUymin())
lineAtPedestal.SetLineColor(kBlack)
lineAtPedestal.SetLineWidth(1)
lineAtPedestal.SetLineStyle(7)
lineAtPedestal.Draw("same")

pedestal= TText(0.21,0.7,"Pedestal")
pedestal.SetNDC()
pedestal.SetTextSize(gStyle.GetTextSize()*0.7)
pedestal.SetTextAngle(90)
pedestal.SetTextFont(42)
pedestal.Draw("same")

cS1.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cS1.pdf')

cS1NotPassed = TCanvas("S1","S1",1500,1500)
hFrame = cS1NotPassed.DrawFrame(Df["Module4_10"].min()*0.9,0.0001,Df["Module4_10"].max()*1.02,0.01,"ADC Normalised counts; Channel; Counts")

hS1All.Draw("hist,same")

hS1NotPassed = TH1D("hS1NotPassed","hS1NotPassed",2048,0,2048)
hS1NotPassed.FillN(len(DfNotPassed["Module4_10"]),np.asarray(DfNotPassed["Module4_10"],'d'),np.asarray([1]*len(DfNotPassed["Module4_10"]),'d'))
hS1NotPassed.Scale(1/len(DfNotPassed))
hS1NotPassed.Rebin(2)
SetObjectStyle(hS1NotPassed,color=kSpring-5,fillalpha=0.5,linewidth=1)
hS1NotPassed.Draw("hist,same")

hS1Passed.Draw("hist,same")

leg = TLegend(0.435, 0.71, 0.85, 0.53)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("S1 Normalised counts")
leg.AddEntry(hS1All, 'With and without S2 signal', 'lf')
leg.AddEntry(hS1Passed, 'Without S2 signal', 'lf')
leg.AddEntry(hS1NotPassed, 'With S2 signal', 'lf')
leg.Draw("same")

text =TLatex(0.45, 0.73,"S1 Scintillator + PMXP2020")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.49,"Using V259 pattern unit")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.43,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.45, 0.37,"Discriminator threshold value: (#font[122]{-}39.6 #pm 0.5) mV")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()

lineAtPedestal = TLine(245, gPad.GetUymax(), 245, gPad.GetUymin())
lineAtPedestal.SetLineColor(kBlack)
lineAtPedestal.SetLineWidth(1)
lineAtPedestal.SetLineStyle(7)
lineAtPedestal.Draw("same")

pedestal= TText(0.21,0.7,"Pedestal")
pedestal.SetNDC()
pedestal.SetTextSize(gStyle.GetTextSize()*0.7)
pedestal.SetTextAngle(90)
pedestal.SetTextFont(42)
pedestal.Draw("same")

cS1NotPassed.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cS1All.pdf')


##########
#   SG   #
##########

cSG = TCanvas("SG","SG",1500,1500)
hFrame = cSG.DrawFrame(Df["Module4_11"].min()*0.9,0.0001,Df["Module4_11"].max()*1.02,0.006,"ADC Normalised counts; Channel; Counts")
hSGAll = TH1D("hSGAll","hSGAll",2048,0,2048)
hSGAll.FillN(len(Df["Module4_11"]),np.asarray(Df["Module4_11"],'d'),np.asarray([1]*len(Df["Module4_11"]),'d'))
hSGAll.Scale(1/len(Df))
hSGAll.Rebin(2)
SetObjectStyle(hSGAll,color=kAzure+3,fillalpha=0.9,linewidth=1)

hSGAll.Draw("hist,same")

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
leg.AddEntry(hSGAll, 'With and without S2 signal', 'lf')
leg.AddEntry(hSGPassed, 'Without S2 signal', 'lf')
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
text3 =TLatex(0.48, 0.59,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.48, 0.53,"Discriminator threshold value: (#font[122]{-}10.2 #pm 0.5) mV")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()


cSG.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cSG.pdf')

cSGNotPassed = TCanvas("SG","SG",1500,1500)
hFrame = cSGNotPassed.DrawFrame(Df["Module4_11"].min()*0.9,0.0001,Df["Module4_11"].max()*1.02,0.006,"ADC Normalised counts; Channel; Counts")

hSGAll.Draw("hist,same")

hSGNotPassed = TH1D("hSGNotPassed","hSGNotPassed",2048,0,2048)
hSGNotPassed.FillN(len(DfNotPassed["Module4_11"]),np.asarray(DfNotPassed["Module4_11"],'d'),np.asarray([1]*len(DfNotPassed["Module4_11"]),'d'))
hSGNotPassed.Scale(1/len(DfNotPassed))
hSGNotPassed.Rebin(2)
SetObjectStyle(hSGNotPassed,color=kSpring-5,fillalpha=0.5,linewidth=1)
hSGNotPassed.Draw("hist,same")
hSGPassed.Draw("hist,same")

leg = TLegend(0.465, 0.81, 0.85, 0.63)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("SG Normalised counts")
leg.AddEntry(hSGAll, 'With and without S2 signal', 'lf')
leg.AddEntry(hSGPassed, 'Without S2 signal', 'lf')
leg.AddEntry(hSGNotPassed, 'With S2 signal', 'lf')
leg.Draw("same")

text =TLatex(0.48, 0.83,"SG Scintillator + PM R1513")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.48, 0.59,"Using V259 pattern unit")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.48, 0.53,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.48, 0.47,"Discriminator threshold value: (#font[122]{-}10.2 #pm 0.5) mV")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()

cSGNotPassed.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cSGAll.pdf')


##############
# Comparison #
##############
SetGlobalStyle(padleftmargin=0.11, padbottommargin=0.12, padrightmargin=0.13, padtopmargin=0.1, titleoffsety=1.05, titleoffsetx=0.9,titleoffsetz=0.8, titleoffset= 0.7, opttitle=1)

cComp = TCanvas("Comparison","Comparison",1500,1500)


hComp = TH2D("Comparison","Comparison SG; Channel no Pattern Unit; Channel without S2 signal;Counts",2048,0,2048,2048,0,2048)
hComp.FillN(len(DfPassed),np.asarray(Df["Module4_11"],'d'),np.asarray(DfPassed["Module4_11"],'d'),np.asarray([1]*len(DfPassed["Module4_11"]),'d'))

hComp.Rebin2D(8,8)
gStyle.SetPalette(kDarkBodyRadiator, 0)
hComp.Draw("COLZ")
gPad.Modified()
gPad.Update()

cComp.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cCompSG.root')
cComp.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cCompSG.pdf')

cCompS1SG = TCanvas("ComparisonS1SG","ComparisonS1SG",1500,1500)
cCompS1SG.SetLogz()
hComp = TH2D("ComparisonS1SG","Comparison of S1 and SG;Channel (S1 without S2 signal);Channel (SG without S2 signal);Counts",2048,0,2048,2048,0,2048)
hComp.FillN(len(DfPassed),np.asarray(DfPassed["Module4_10"],'d'),np.asarray(DfPassed["Module4_11"],'d'),np.asarray([1]*len(DfPassed["Module4_11"]),'d'))

hComp.Rebin2D(8,8)
gStyle.SetPalette(kDarkBodyRadiator, 0)
hComp.Draw("COLZ")
gPad.Modified()
gPad.Update()

cCompS1SG.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cCompS1SG.root')
cCompS1SG.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cCompS1SG.pdf')