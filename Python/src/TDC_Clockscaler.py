import pandas as pd
import numpy as np
import uproot
import math
from ROOT import TF1,TAxis, TH1D, TCanvas, kAzure, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFitResultPtr

import sys
sys.path.append('Python/utils')

from StyleFormatter import SetGlobalStyle, SetObjectStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)
treeTDC_Clock=uproot.open("data/input/data_tree.root")["fTreeData"]

#rootFilePath = 'LabFNS1/data/output/TDC.root'
 #rootFile = TFile(rootFilePath, 'recreate')

df=treeTDC_Clock.arrays(library='pd')
df=df[["2228A_-_tdc__ch6","C257_-_scaler__ch15"]]
df["TDC_time"]=df["2228A_-_tdc__ch6"]*2.5


cS1 = TCanvas("cS1","cS1",1500,1500)
cS1.cd()
cS1.SetLogy()
hTDC=TH1D("hTDC","hTDC",125,0,5000)
for x in df["TDC_time"]: hTDC.Fill(x)

funz=TF1("funz","[0]+[1]*exp(x*[2])",20,1000)
funz1=TF1("funz1","[0]+[1]*exp(x*[2])",2000,5000)
funz2=TF1("funz2","[0]+[1]*exp(x*[2])+[3]*exp(x*[4])",0,5000)
funz.SetParameter(1,65)
funz.SetParameter(2,-0.01)
#funz2.SetParameter(0,)
funz1.SetParameter(2,-0.00045)
funz2.SetParameter(2,-0.00045)
funz2.SetParameter(4,-0.01)
funz.SetLineColor(kAzure)
funz1.SetLineColor(kRed)
funz2.SetLineColor(kGreen)
hTDC.Fit(funz,"RM+")
hTDC.Fit(funz1,"RM+")
hTDC.Fit(funz2,"RM+")
gStyle.SetOptFit(1);


hTDC.Draw("E")

leg = TLegend(0.435, 0.71, 0.85, 0.59)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)
leg.AddEntry(hTDC, 'TDC', 'lf')
leg.Draw("same")
input("Press enter to close")