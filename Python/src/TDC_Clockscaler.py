import pandas as pd
import numpy as np
import uproot
import math
from ROOT import TF1,TAxis, TH1D,TH2D, TCanvas, kAzure,kBlue, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFitResultPtr

import sys
sys.path.append('Python/utils')

from StyleFormatter import SetGlobalStyle, SetObjectStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)
treeTDC_Clock=uproot.open("data/input/data_tree.root")["fTreeData"]
treeClock=uproot.open("data/input/thursday_tree.root")["fTreeData"]

#rootFilePath = 'LabFNS1/data/output/TDC.root'
 #rootFile = TFile(rootFilePath, 'recreate')

df=treeTDC_Clock.arrays(library='pd')
dfth=treeClock.arrays(library='pd')
df=df[["2228A_-_tdc__ch6","C257_-_scaler__ch15","2249W_-_adc__ch11","V259N_-_multi-hit_patter_unit__ch0"]]
df["TDC_time"]=df["2228A_-_tdc__ch6"]*2.5
df["Clock"]=df["C257_-_scaler__ch15"]*6000/70
df["PU"]=df["V259N_-_multi-hit_patter_unit__ch0"]
dfth["ClockTh"]=dfth["C257_-_scaler__ch15"]*10000/108
dfth["ClockADCTH"]=dfth["2249W_-_adc__ch11"]
df2 = dfth.query('6000 < ClockTh < 9000', inplace=False)
dfPU=df.query("PU==1")


cS1 = TCanvas("cS1","cS1",1500,1500)
cS1.cd()
cS1.SetLogy()
hTDC=TH1D("hTDC","hTDC",125,0,5000)

for x in df["TDC_time"]: hTDC.Fill(x)

hTDCPU=TH1D("hTDCPU","hTDCPU",125,0,5000)

for x in dfPU["TDC_time"]: hTDCPU.Fill(x)


funz=TF1("funz","[0]+[1]*exp(x*[2])",20,800)
funz1=TF1("funz1","[0]+[1]*exp(x*[2])",2000,5000)
funz2=TF1("funz2","[0]+[1]*exp(x*[2])",100,800)


#funz2.SetParameter(3,0)
#funz2.SetParameter(2,-0.01)
#funz2.FixParameter(4,-0.00045)

funz.SetLineColor(kBlue)
funz1.SetLineColor(kRed)
funz2.SetLineColor(kGreen)
#hTDC.Fit(funz,"RM+")
#hTDC.Fit(funz1,"RM+")
#hTDC.Fit(funz2,"RM+")
#gStyle.SetOptFit(1)



hTDC.Draw("E")
#hTDCPU.Draw("E")

hTDC.GetXaxis().SetTitle("Time [ns]")
hTDC.GetYaxis().SetTitle("Events")
#hTDCPU.GetXaxis().SetTitle("Time [ns]")
#hTDCPU.GetYaxis().SetTitle("Events")



text =TLatex(0.30, 0.7,"TDC LeCroy 2228A")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.30, 0.62,"Using V259 pattern unit #mu, signals without S2")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.30, 0.56,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
text4 =TLatex(0.30, 0.48,"Fake stop time:6 #mus")
text4.SetNDC()
text4.SetTextSize(gStyle.GetTextSize()*0.7)
text4.SetTextFont(42)
text4.Draw()


leg = TLegend(0.50, 0.71, 0.85, 0.59)
leg.SetTextFont(42)
leg.SetTextSize(gStyle.GetTextSize()*0.7)
leg.SetFillStyle(0)

leg.AddEntry(hTDC, 'TDC_data', 'lf')
leg.AddEntry(funz1, 'N_{0} + c_{1}exp(-#lambda_{dec}*t)', 'lf')
leg.AddEntry(funz, 'N_{0} + c_{1}exp(-#lambda_{dec}*t)+ c_{2}exp(-#lambda_{cat}*t)', 'lf')

#leg.Draw("same")
input("Press enter to close")

cS2 = TCanvas("cS2","cS2",1500,1500)
cS2.cd()
cS2.SetLogy()
hClock=TH1D("hClock","hClock",70,-0.5,6000.5)
for y in df["Clock"]: hClock.Fill(y)
SetObjectStyle(hClock,color=kAzure+3,fillalpha=0.9,linewidth=1)
hClock.Draw("hist")

hClock.GetXaxis().SetTitle("Time [ns]")
hClock.GetYaxis().SetTitle("Events")
text =TLatex(0.45, 0.8,"Scaler CAEN C257")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.62,"Acquisition time: 236985 s")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
input("Press enter to close 2")

cSGiov = TCanvas("cSGiov","cSGiov",1500,1500)
cSGiov.cd()
cSGiov.SetLogy()
hClockTh=TH1D("hClockTh","hClockTh",90,0.5,10000.5)
for y in dfth["ClockTh"]: hClockTh.Fill(y)
SetObjectStyle(hClockTh,color=kAzure+3,fillalpha=0.5,linewidth=1)
hClockTh.Draw("hist")

hClockTh.GetXaxis().SetTitle("Time [ns]")
hClockTh.GetYaxis().SetTitle("Events")
text =TLatex(0.45, 0.7,"Scaler CAEN C257")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.62,"Acquisition time: 57360 s")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.56,"Fake stop time:10 #mus")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
input("Press enter to close Clock scaler giov")

cS3 = TCanvas("cS3","cS3",1500,1500)
cS3.cd()
cS3.SetLogy()
hAfter=TH1D("hAfter","hAfter",2048, 0, 2048)
for z in df2["ClockADCTH"]: hAfter.Fill(z)
hAfter.Rebin( 16)


hAfter.GetXaxis().SetTitle("Energy [channel]")
hAfter.GetYaxis().SetTitle("Events")
funz5=TF1("funz5","gaus )",300,1400)
funz5.SetLineColor(kRed)
funz5.SetParameter(5,0.00045)
funz5.SetParameter(2,800)
hAfter.Fit(funz5,"RM+")
hAfter.Draw("E")

text =TLatex(0.45, 0.8,"ADC LeCroy 2249W")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.62,"Acquisition time: 57360 s")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize()*0.7)
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.56,"Fake stop time:10 #mus")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
input("Press enter to close 3")

cS4 = TCanvas("cS4","cS4",1500,1500)
cS4.cd()
hADCvsClock=TH2D("hADCvsClock","hADCvsClock",70,-0.5,10000.5,2050, 0, 2050);
for x, y in zip(df['Clock'], df['2249W_-_adc__ch11']):   hADCvsClock.Fill(x, y)

hADCvsClock.GetXaxis().SetTitle('Time [ns]')
hADCvsClock.GetYaxis().SetTitle('Energy (channel)')
hADCvsClock.Draw("LEGO1");
text =TLatex(0.45, 0.8,"ADC LeCroy 2249W")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize())
text.SetTextFont(42)
text.Draw()
text2 =TLatex(0.45, 0.62,"Scaler CAEN C257")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize())
text2.SetTextFont(42)
text2.Draw()
text3 =TLatex(0.45, 0.56,"Acquisition time: 236985 s")
text3.SetNDC()
text3.SetTextSize(gStyle.GetTextSize()*0.7)
text3.SetTextFont(42)
text3.Draw()
input("Press enter to close 4")





