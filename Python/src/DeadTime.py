import pandas as pd
import numpy as np
import uproot
import sys
sys.path.append('Python/utils')

from ROOT import TH1D, TCanvas, TPad, TLegend, kAzure, kOrange, gPad, gStyle, gROOT

from StyleFormatter import SetGlobalStyle, SetObjectStyle

#gROOT.SetBatch()

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

Tree=uproot.open("data/input/DataFullRun.root")["fTreeData"]

##########
#   S1   #
##########

Df=Tree.arrays(library='pd')

Df=Df[["Module1_0","Module2_0","Module5_0"]]
print(Df["Module1_0"].max())
print("Not Inhibited", 2**16*8+Df.iloc[-2]["Module1_0"])
print("Inhibited", 2**16*8+Df.iloc[-2]["Module2_0"])
print("Contamination", (len(Df.query("Module5_0==1")))/(2**16*8+Df.iloc[-2]["Module2_0"]))
print("N_bad_T", len(Df.query("Module5_0==1")))


events=list(range(len(Df)))

c = TCanvas("NotInhibited","NotInhibited",1000,1000)


c.Draw()
pBotLeft = TPad("p1","p1",0.,0.,0.5,0.3)
pBotLeft.SetTopMargin(0.)
pBotLeft.SetBottomMargin(0.2)
pBotLeft.Draw()
pUpLeft = TPad("p3","p3",0.,0.3,0.5,1.)
#pUpLeft.SetRightMargin(0.14)
pUpLeft.SetBottomMargin(0.)
pUpLeft.Draw()
pRight = TPad("p2","p2",0.5,0.,1.,1.)
pRight.SetBottomMargin(0.1)
pRight.Draw()

pUpLeft.cd()
hUpLeftFrame=pUpLeft.DrawFrame(0,2,len(events),20e6,"Scaler register content;Event number;Register content")
hUpLeftFrame.GetXaxis().SetMaxDigits(10)
hInhibited = TH1D("Inhibited","Inhibited",3000,0,len(events))

hInhibited.FillN(len(Df["Module2_0"]),np.asarray(events,'d'),np.asarray(Df["Module2_0"],'d'))
SetObjectStyle(hInhibited,color=kOrange-3,fillalpha=0.5,linewidth=1)
hInhibited.Draw("same")

hNotInhibited = TH1D("NotInhibited","NotInhibited",3000,0,len(events))
hNotInhibited.FillN(len(Df["Module1_0"]),np.asarray(events,'d'), np.asarray(Df["Module1_0"],'d'))
SetObjectStyle(hNotInhibited,color=kAzure+3,fillalpha=0.5,linewidth=1)
hNotInhibited.Draw("same")

leg = TLegend(0.435, 0.81, 0.85, 0.69)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
#leg.SetHeader("S1 Normalised counts")
leg.AddEntry(hNotInhibited, 'Not inhibited', 'p')
leg.AddEntry(hInhibited, 'Inhibited', 'p')
leg.Draw("same")

pBotLeft.cd()
hBotLeftFrame=pBotLeft.DrawFrame(0,0,len(events),2.3e6,";Event number;Difference")
hBotLeftFrame.GetYaxis().SetTitleSize(0.08)
hBotLeftFrame.GetXaxis().SetTitleSize(0.09)
hBotLeftFrame.GetXaxis().SetLabelSize(0.05)
hBotLeftFrame.GetXaxis().SetLabelSize(0.05)
hBotLeftFrame.GetYaxis().SetTitleOffset(0.8)
hBotLeftFrame.GetXaxis().SetTitleOffset(0.8)
hDifference = TH1D("Difference","Difference",3000,0,len(events))
hDifference.FillN(len(Df["Module1_0"]),np.asarray(events,'d'), np.asarray(Df["Module1_0"]-Df["Module2_0"],'d'))
SetObjectStyle(hDifference,color=kAzure+3,fillalpha=1,linewidth=1)
hDifference.Draw("same")
pBotLeft.Modified()
pBotLeft.Update()

pRight.cd()
hComparison = TH1D("Total counts","Total counts;;Counts",2,0,2)
hComparison.Fill(0,2**16*8+Df.iloc[-2]["Module1_0"])
hComparison.Fill(1,2**16*8+Df.iloc[-2]["Module2_0"])
hComparison.SetAxisRange(0., 600000.,"Y")
hComparison.GetXaxis().SetBinLabel(1,"Not inhibited")
hComparison.GetXaxis().SetBinLabel(2,"Inhibited")
hComparison.GetXaxis().CenterLabels()
SetObjectStyle(hComparison,color=kOrange-3,fillalpha=0.5,linewidth=1)
hComparison.Draw("hist,same")

c.cd()
c.Update()
c.cd(0)
c.SaveAs("/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/src/DeadTime.pdf")
