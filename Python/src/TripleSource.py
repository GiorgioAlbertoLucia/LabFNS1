import pandas as pd
import numpy as np
import sys
#import argparse

sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta, TF1, gStyle, TPaveStats, gPad,TGraphErrors, TLatex,TFile

def CreateHist(infile,data):

    with open(infile, 'r', errors='ignore') as file:#with chiude i automatico il file

        lines = file.readlines()[1:-1]
        start_index = lines.index('<<DATA>>\n') + 1
        end_index = lines.index('<<END>>\n')

        for line in lines[start_index:end_index]:
            value = int(line.strip())  # Convert the line to an integer
            data.append(value)  # Append the value to the list
   
    df = pd.DataFrame(data, columns=['Value'])
    hist = TH1D("Hist","Hist",len(df),0,len(df))
    for i, x in enumerate(df["Value"]): 
        hist.Fill(i, x)
        hist.SetBinError(i,np.sqrt(x))
    return hist 

def HistoFromCtoE(data,aa,bb,nbin):
    histE = TH1D("HistE","HistE",nbin,0,nbin)
    
    df = pd.DataFrame(data, columns=['Value'])
    
    for i, x in enumerate(df["Value"]): 
        histE.Fill(i*aa+bb, x)
        histE.SetBinError(i,np.sqrt(x))
    return histE 


if __name__ == '__main__':
    data = []
    outfilePath = 'data/output/Diamond/TripleSorce.root'
    root_file = TFile(outfilePath, 'recreate')

    infilename='data/input/Diamonds/Tuesday/sorgente_tripla.mca'
    c = TCanvas('c','c',1000,1000)
    histo=CreateHist(infilename,data)
    histo.Draw("E")

    gStyle.SetOptFit(1111)
    Americio = TF1('Americio', "gaus", 1700, 1720)
    Curio = TF1('CUrio', "gaus", 1800, 1825)
    Neptunio1=TF1('Neptunio1', "gaus", 1430, 1460)
    Neptunio2=TF1('Neptunio2', "gaus", 1470, 1500)
    Neptunio3=TF1('Neptunio2', "gaus", 1510, 1525)


    histo.Fit(Americio,"RM")
    c.Update()
    histo.Fit(Curio,"RM")
    c.Update()
    histo.Fit(Neptunio1,"RM")
    c.Update()
    histo.Fit(Neptunio2,"RM")
    c.Update()
    histo.Fit(Neptunio3,"RM")

    Neptunio=TF1('Neptunio', "gaus(0)+gaus(3)+gaus(6)", 1425, 1530)
    Neptunio2picchi=TF1("Neptunio2picchi","gaus(0)+gaus(3)",1470,1500)
    Neptunio.SetParNames("Norm_{1}", "#mu_{1}", "#sigma_{1}", "Norm_{2}", "#mu_{2}", "#sigma_{2}", "Norm_{3}", "#mu_{3}", "#sigma_{3}")
    Neptunio.SetParameter(1,Neptunio1.GetParameter(1))
    Neptunio.SetParLimits(1,1443,1444)
    Neptunio.SetParameter(4,Neptunio2.GetParameter(1))
    Neptunio.SetParLimits(4,1485,1486)
    Neptunio.SetParameter(7,Neptunio3.GetParameter(1))
    Neptunio.SetParLimits(7,1515,1516)
    Neptunio.SetParameter(2,Neptunio1.GetParameter(2))
    Neptunio.SetParLimits(2,5.0,5.6)
    Neptunio.SetParameter(5,Neptunio2.GetParameter(2))
    Neptunio.SetParLimits(5,5.6,6.6)
    Neptunio.SetParameter(8,Neptunio3.GetParameter(2))
    Neptunio.SetParLimits(8,2.5,3)

    Neptunio2picchi.SetParameters(1,1483)
    Neptunio2picchi.SetParameters(4,1490)

  
    #Neptunio.SetParameter(3,Neptunio1.GetParameter(3))
    #Neptunio.SetParameter(6,Neptunio2.GetParameter(3))
    #Neptunio.SetParameter(9,Neptunio3.GetParameter(3))


    c.Update()
    histo.Fit(Neptunio,"RM")
    
    
    Americio.SetLineColor(kGreen)
    Curio.SetLineColor(kBlue+3)
    Neptunio1.SetLineColor(kRed)
    Neptunio2.SetLineColor(kRed+2)
    Neptunio3.SetLineColor(kRed+4)
    Neptunio.SetLineColor(kOrange-3)

    Americio.Draw("same")
    Curio.Draw("same")
    #Neptunio3.Draw("same")
    #Neptunio2.Draw("same")
   # Neptunio1.Draw("same")
    #Neptunio.Draw("same")

    print("primo picco= ",Neptunio1.GetChisquare()/Neptunio1.GetNDF(),end='\n') 
    print("secondo picco= ",Neptunio2.GetChisquare()/Neptunio2.GetNDF(),end='\n') 
    print("terzo picco= ",Neptunio3.GetChisquare()//Neptunio3.GetNDF(),end='\n') 
    gStyle.SetOptFit(1111)
    stat = TPaveStats()
    stat1 = TPaveStats()
    stat = Americio.FindObject("stats")
    stat1 = Curio.FindObject("stats")
    if(stat and stat1):
        stat.SetTextColor(kBlue+3);
        stat1.SetTextColor(kOrange-3);
        height = stat1.GetY2NDC() - stat1.GetY1NDC();
        stat1.SetY1NDC(stat.GetY1NDC() - height);
        stat1.SetY2NDC(stat.GetY1NDC() );
        stat1.Draw('same');
        stat.Draw('same');
    c.Modified()
    c.Update()
    root_file.cd()
    c.Write()
    gPad.Update()

    c1 = TCanvas('c1','c1',1000,1000)
    c1.cd()
    points=[1710,1810,1485 ]
    sigmapoint=[5,6,6]
    energy=[5480.0,5795.0,4780.70]
    energyerr=[0.,0.,0.]
    retcal = TGraphErrors(3,np.asarray(energy,'d'),np.asarray(points,'d'),
                     np.asarray(energyerr,'d'),np.asarray(sigmapoint,'d'))
    retta=TF1("retta","[0]+[1]*x",-10,6000)
    retcal.SetTitle("Retta calibrazione")
    retcal.GetXaxis().SetTitle("Energy [keV]")
    retcal.GetYaxis().SetTitle("Channels")
    retcal.Fit(retta,"RM")
    retcal.Draw("AP")
    retcal.SetMarkerStyle(8)
    retcal.SetMarkerSize(1.2)
    retta.Draw("same")
    text =TLatex(0.30, 0.7,"Calibration Fit")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.30, 0.62,"Diamond detector, with triple source")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.30, 0.56,"chn= a*Energy + b")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()
    text4 =TLatex(0.30, 0.48,"a=(0.3206 #pm 0.0014) keV^{-1}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw()
    text5 =TLatex(0.30, 0.40,"b= -47 #pm 7")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize()*0.7)
    text5.SetTextFont(42)
    text5.Draw()
    c1.Modified()
    c1.Update()
    root_file.cd()
    c1.Write()

    c2 = TCanvas('c2','c2',1000,1000)
    c2.cd()
    Neptunio2picchi=TF1("Neptunio2picchi","gaus(0)+gaus(3)+gaus(6)",1470,1500)
    Neptunio2picchi.SetLineColor(kBlack)
    Neptunio2picchi.SetParameters(1,1483)
    Neptunio2picchi.SetParLimits(1,1475,1490)
    Neptunio2picchi.SetParameters(4,1490)
    Neptunio2picchi.SetParLimits(4,1480,1492)
    Neptunio2picchi.SetParLimits(8,0,100)
    histo.Fit(Neptunio2picchi,"RM")
    histo.Draw("E")
    Neptunio2picchi.Draw("same")
    root_file.cd()
    c2.Write()

    c3 = TCanvas('c3','c3',1000,1000)
    c3.cd()
    histE =HistoFromCtoE(data,retta.GetParameter(1),retta.GetParameter(0),histo.GetNbinsX())
    histE.Draw("hist")

    input()
    

