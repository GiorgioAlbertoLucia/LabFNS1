import sys
import pandas as pd
import numpy as np
import uproot
from ROOT import TH1D, TCanvas, kAzure, kRed, kGreen, kSpring, kBlack, TLegend, TLatex, TLine, TText, gStyle, gPad
sys.path.append('Python/utils')
from Pedestal import DrawPedestral
from StyleFormatter import SetGlobalStyle, SetObjectStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

Tree=uproot.open("/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/data/input/DataFullRun.root")["fTreeData"]

##########
#   TDC   #
##########

Df=Tree.arrays(library='pd')

Df=Df[["Module3_6","Module5_0"]]
DfPassed=Df.query("Module5_0==0")
DfNotPassed=Df.query("Module5_0==1")

cTDC = TCanvas("TDC","TDC",1500,1500)
cTDC.SetLogy()
yMincTDC = 1.e-6
yMaxcTDC = 0.2
hFrame = cTDC.DrawFrame(Df["Module3_6"].min()*0.9,yMincTDC,2048,yMaxcTDC,"TDC Normalised counts; Channel; Counts")
hTDCAll = TH1D("hTDCAll","hTDCAll",2048,0,2048)
hTDCAll.FillN(len(Df["Module3_6"]),np.asarray(Df["Module3_6"],'d'),np.asarray([1]*len(Df["Module3_6"]),'d'))
hTDCAll.Scale(1/len(Df))
hTDCAll.Rebin(2)
SetObjectStyle(hTDCAll,color=kAzure+3,fillalpha=0.9,linewidth=1)
hTDCAll.Draw("hist,same")

hTDCPassed = TH1D("hTDCPassed","hTDCPassed",2048,0,2048)
hTDCPassed.FillN(len(DfPassed["Module3_6"]),np.asarray(DfPassed["Module3_6"],'d'),np.asarray([1]*len(DfPassed["Module3_6"]),'d'))
hTDCPassed.Scale(1/len(DfPassed))
hTDCPassed.Rebin(2)
SetObjectStyle(hTDCPassed,color=kRed,fillalpha=0.5,linewidth=1)
hTDCPassed.Draw("hist,same")

leg = TLegend(0.435, 0.78, 0.85, 0.66)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("TDC Normalised counts")
leg.AddEntry(hTDCAll, 'With and without S2 signal', 'lf')
leg.AddEntry(hTDCPassed, 'Without S2 signal', 'lf')
leg.Draw("same")

text =TLatex(0.45, 0.8,"TDC LeCroy 2228A")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.62,"Using V259 pattern unit #mu")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.56,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()

cTDC.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cTDC.pdf')

cTDCNotPassed = TCanvas("TDC","TDC",1500,1500)
cTDCNotPassed.SetLogy()
hFrame = cTDCNotPassed.DrawFrame(Df["Module3_6"].min()*0.9,yMincTDC,2048,yMaxcTDC,"TDC Normalised counts; Channel; Counts")

hTDCAll.Draw("hist,same")

hTDCNotPassed = TH1D("hTDCNotPassed","hTDCNotPassed",2048,0,2048)
hTDCNotPassed.FillN(len(DfNotPassed["Module3_6"]),np.asarray(DfNotPassed["Module3_6"],'d'),np.asarray([1]*len(DfNotPassed["Module3_6"]),'d'))
hTDCNotPassed.Scale(1/len(DfNotPassed))
hTDCNotPassed.Rebin(2)
SetObjectStyle(hTDCNotPassed,color=kSpring-5,fillalpha=0.5,linewidth=1)
hTDCNotPassed.Draw("hist,same")

hTDCPassed.Draw("hist,same")

leg = TLegend(0.435, 0.78, 0.85, 0.60)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("TDC Normalised counts")
leg.AddEntry(hTDCAll, 'With and without S2 signal', 'lf')
leg.AddEntry(hTDCPassed, 'Without S2 signal', 'lf')
leg.AddEntry(hTDCNotPassed, 'With S2 signal', 'lf')
leg.Draw("same")

text =TLatex(0.45, 0.80,"TDC LeCroy 2228A")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.56,"Using V259 pattern unit")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.5,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()


cTDCNotPassed.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/utils/cTDCAll.pdf')

