import pandas as pd
import numpy as np
import sys
#import argparse

sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure,kGray, kMagenta, TF1, gStyle, TPaveStats, gPad,TGraphErrors, TLatex,TFile, kSpring,TLegend

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
    histE = TH1D("HistE","HistE",nbin,(0-bb)/aa,(nbin-bb)/aa)
    
    df = pd.DataFrame(data, columns=['Value'])
    
    for i, x in enumerate(df["Value"]): 
        histE.Fill((i-bb)/aa, x)
        histE.SetBinError(i,np.sqrt(x))
    return histE 


if __name__ == '__main__':
    data = []
    outfilePath = 'data/output/Diamond/TripleSorce.root'
    root_file = TFile(outfilePath, 'recreate')

    infilename='data/input/Diamonds/Tuesday/sorgente_tripla.mca'
    c = TCanvas('c','c',1000,1000)
    leg = TLegend(0.435, 0.71, 0.85, 0.59)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    histo=CreateHist(infilename,data)
    histo.Draw("E")

    gStyle.SetOptFit(1111)
    Americio = TF1('Americio', "gaus", 1700, 1720)
    Curio = TF1('CUrio', "gaus", 1800, 1825)
    #Neptunio1=TF1('Neptunio1', "gaus", 1430, 1460)
    #Neptunio2=TF1('Neptunio2', "gaus", 1470, 1500)
    #Neptunio3=TF1('Neptunio2', "gaus", 1510, 1525)


    histo.Fit(Americio,"RM")
    c.Update()
    histo.Fit(Curio,"RM")
    c.Update()
    #histo.Fit(Neptunio1,"RM")
    #c.Update()
    #histo.Fit(Neptunio2,"RM")
    #c.Update()
    #histo.Fit(Neptunio3,"RM")

    Neptunio=TF1('Neptunio', "gaus", 1470, 1500)
    #Neptunio2picchi=TF1("Neptunio2picchi","gaus(0)+gaus(3)",1470,1500)
    #Neptunio.SetParNames("Norm_{1}", "#mu_{1}", "#sigma_{1}", "Norm_{2}", "#mu_{2}", "#sigma_{2}", "Norm_{3}", "#mu_{3}", "#sigma_{3}")
    #Neptunio.SetParameter(1,Neptunio1.GetParameter(1))
    #Neptunio.SetParLimits(1,1443,1444)
    #Neptunio.SetParameter(4,Neptunio2.GetParameter(1))
    #Neptunio.SetParLimits(4,1485,1486)
    #Neptunio.SetParameter(7,Neptunio3.GetParameter(1))
    #Neptunio.SetParLimits(7,1515,1516)
    #Neptunio.SetParameter(2,Neptunio1.GetParameter(2))
    #Neptunio.SetParLimits(2,5.0,5.6)
    #Neptunio.SetParameter(5,Neptunio2.GetParameter(2))
    #Neptunio.SetParLimits(5,5.6,6.6)
    #Neptunio.SetParameter(8,Neptunio3.GetParameter(2))
    #Neptunio.SetParLimits(8,2.5,3)

    #Neptunio2picchi.SetParameters(1,1483)
    #Neptunio2picchi.SetParameters(4,1490)

  
    #Neptunio.SetParameter(3,Neptunio1.GetParameter(3))
    #Neptunio.SetParameter(6,Neptunio2.GetParameter(3))
    #Neptunio.SetParameter(9,Neptunio3.GetParameter(3))


    c.Update()
    histo.Fit(Neptunio,"RM")
    
    
    Americio.SetLineColor(kGreen)
    Curio.SetLineColor(kOrange-3)
    Neptunio.SetLineColor(kMagenta)
    #Neptunio1.SetLineColor(kRed)
    #Neptunio2.SetLineColor(kRed+2)
    #Neptunio3.SetLineColor(kRed+4)
    #Neptunio.SetLineColor(kOrange-3)

    Americio.Draw("same")
    Curio.Draw("same")
    Neptunio.Draw("same")
    #Neptunio3.Draw("same")
    #Neptunio2.Draw("same")
   # Neptunio1.Draw("same")
    #Neptunio.Draw("same")

    #print("primo picco= ",Neptunio1.GetChisquare()/Neptunio1.GetNDF(),end='\n') 
    #print("secondo picco= ",Neptunio2.GetChisquare()/Neptunio2.GetNDF(),end='\n') 
    #print("terzo picco= ",Neptunio3.GetChisquare()//Neptunio3.GetNDF(),end='\n') 
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
    leg.AddEntry(histo, "Data from triple source", 'lf')
    leg.AddEntry(Neptunio, "Gauss: fit on ^{237}Np", 'lf')
    leg.AddEntry(Americio, "Gauss: fit on ^{241}Am", 'lf')
    leg.AddEntry(Curio, "Gauss: fit on ^{244}Cm", 'lf')
    leg.Draw("same")

    text =TLatex(0.30, 0.7,"Diamond detector, spectrum of triple source ")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text1 =TLatex(0.30, 0.62,"Acquisition time:4000s")
    text1.SetNDC()
    text1.SetTextSize(gStyle.GetTextSize()*0.7)
    text1.SetTextFont(42)
    text1.Draw()
    
    
    c.Modified()
    c.Update()
    root_file.cd()
    c.Write()
    gPad.Update()

    c1 = TCanvas('c1','c1',1000,1000)
    c1.cd()
    points=[1710,1810,1485 ]
    sigmapoint=[5,6,6]
    energy=[5486,5805.0,4780.70]
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
    text4 =TLatex(0.30, 0.48,"a=(0.3207 #pm 0.0008) keV^{-1}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw()
    text5 =TLatex(0.30, 0.40,"b= (-5*10^{1} #pm 5*10^{1}) chn")
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
    Neptunio2picchi1=TF1("Neptunio2picchi1","gaus",1470,1500)
    Neptunio2picchi2=TF1("Neptunio2picchi1","gaus",1470,1500)
    Neptunio2picchi=TF1("Neptunio2picchi","gaus(0)+gaus(3)+gaus(6)",1470,1500)
    Neptunio2picchi.SetLineColor(kBlack)
    Neptunio2picchi1.SetLineColor(kRed)
    Neptunio2picchi2.SetLineColor(kSpring)
    Neptunio2picchi.SetParLimits(0,0,1000)
    Neptunio2picchi.SetParameter(0,147)
    Neptunio2picchi.SetParameter(2,4)
    Neptunio2picchi.SetParLimits(1,1481,1484)
    Neptunio2picchi.SetParameter(4,1490)
    Neptunio2picchi.SetParameter(3,154)
    Neptunio2picchi.SetParameter(5,5)
    Neptunio2picchi.SetParLimits(4,1485,1489)
    histo.Fit(Neptunio2picchi,"RM")
    Neptunio2picchi1.SetParameters(Neptunio2picchi.GetParameter(0),Neptunio2picchi.GetParameter(1),Neptunio2picchi.GetParameter(2))
    Neptunio2picchi2.SetParameters(Neptunio2picchi.GetParameter(3),Neptunio2picchi.GetParameter(4),Neptunio2picchi.GetParameter(5))
    #histo.Fit(Neptunio2picchi1,"RM")
    #histo.Fit(Neptunio2picchi2,"RM")
    histo.Draw("E")

    Neptunio2picchi.Draw("same")
    Neptunio2picchi1.Draw("same")
    Neptunio2picchi2.Draw("same")
    root_file.cd()
    c2.Write()

    c3 = TCanvas('c3','c3',1000,1000)
    c3.cd()
    histE =HistoFromCtoE(data,retta.GetParameter(1),retta.GetParameter(0),histo.GetNbinsX())

    histE.GetXaxis().SetTitle("Energy [keV]")
    histE.GetYaxis().SetTitle("Counts")
    Curio1=TF1("Curio1","gaus",5715,5850)
    Curio2=TF1("Curio2","gaus",5715,5850)
    CurioTot=TF1("CurioTot","gaus(0)+gaus(3)+[6]",5715,5850)
    CurioTot.SetParLimits(0,0,150)
    CurioTot.SetParameter(1,5763)
    CurioTot.SetParLimits(2,1,20)
    CurioTot.SetParLimits(4,5803,5807)
    CurioTot.SetParLimits(1,5760,5767)
    CurioTot.SetParameter(5,15)
    histE.Fit(CurioTot,"RM")
    Curio1.SetParameters(CurioTot.GetParameter(0),CurioTot.GetParameter(1),CurioTot.GetParameter(2))
    Curio2.SetParameters(CurioTot.GetParameter(3),CurioTot.GetParameter(4),CurioTot.GetParameter(5))
    CurioTot.SetLineColor(kRed+3)
    Curio1.SetLineColor(kRed)
    Curio2.SetLineColor(kRed+2)
    histE.Draw("E")
    CurioTot.Draw("same")
    Curio1.Draw("same")
    Curio2.Draw("same")

    '''Americio1=TF1("Americio1","gaus",5430,5540)
    Americio2=TF1("Americio2","gaus",5430,5540)
    #Americio1=TF1("Americio2","gaus",5410,5540)
    AmericioTot=TF1("AmericioTot","gaus(0)+gaus(3)+[6]",5425,5540)
    AmericioTot.SetParLimits(0,0,150)
    AmericioTot.SetParLimits(1,5440,5450)
    AmericioTot.SetParLimits(4,5482,5499)
    AmericioTot.SetParameter(5,15)
    histE.Fit(AmericioTot,"RM")
    Americio1.SetParameters(AmericioTot.GetParameter(0),AmericioTot.GetParameter(1),AmericioTot.GetParameter(2))
    Americio2.SetParameters(AmericioTot.GetParameter(3),AmericioTot.GetParameter(4),AmericioTot.GetParameter(5))
    #mericio3.SetParameters(AmericioTot.GetParameter(6),AmericioTot.GetParameter(7),AmericioTot.GetParameter(8))
    AmericioTot.SetLineColor(kGreen)
    Americio1.SetLineColor(kRed)
    Americio2.SetLineColor(kGreen+2)
    #Americio2.SetLineColor(kGreen+1)
    histE.Draw("E")
    AmericioTot.Draw("same")
    Americio1.Draw("same")
    Americio2.Draw("same")
    Americio3.Draw("same")'''

    NEptunioo1=TF1("NEptunioo1","gaus",4600,4910)
    NEptunioo2=TF1("NEptunioo2","gaus",4600,4910)
    NEptunioo3=TF1("NEptunioo3","gaus",4600,4910)
    NEptunioo4=TF1("NEptunioo4","gaus",4600,4910)
    NEptuniooTot=TF1("NEptuniooTot","gaus(0)+gaus(3)+gaus(6)+gaus(9) +[12]",4600,4910)
    NEptuniooTot.SetParLimits(4,4767,4780)
    NEptuniooTot.SetParLimits(7,4780,4791)
    NEptuniooTot.SetParLimits(10,4870,4880)
    NEptuniooTot.SetParLimits(1,4640,4646)
    NEptuniooTot.SetParLimits(2,0.5,100)
    NEptuniooTot.SetParLimits(5,0,100)
    NEptuniooTot.SetParLimits(8,1,30)
    NEptuniooTot.SetParLimits(11,1,10)
    NEptuniooTot.SetParLimits(0,1,40)
    NEptuniooTot.SetParLimits(6,0,130)
    NEptuniooTot.SetParLimits(3,1,60)
    NEptuniooTot.SetParLimits(9,1,120)
    
    #NEptuniooTot.SetParLimits(7,4785,4790)
    #NEptuniooTot.SetParLimits(6,0,170)
    #NEptuniooTot.SetParLimits(8,1,8)
    NEptuniooTot.SetParameter(5,15)
    histE.Fit(NEptuniooTot,"RM")
    NEptunioo1.SetParameters(NEptuniooTot.GetParameter(0),NEptuniooTot.GetParameter(1),NEptuniooTot.GetParameter(2))
    NEptunioo2.SetParameters(NEptuniooTot.GetParameter(3),NEptuniooTot.GetParameter(4),NEptuniooTot.GetParameter(5))
    NEptunioo3.SetParameters(NEptuniooTot.GetParameter(6),NEptuniooTot.GetParameter(7),NEptuniooTot.GetParameter(8))
    NEptunioo4.SetParameters(NEptuniooTot.GetParameter(9),NEptuniooTot.GetParameter(10),NEptuniooTot.GetParameter(11))
    NEptuniooTot.SetLineColor(kBlack)
    NEptunioo1.SetLineColor(kGray)
    NEptunioo2.SetLineColor(kGray+1)
    NEptunioo3.SetLineColor(kBlue)
    NEptunioo4.SetLineColor(kRed)
    histE.Draw("E")
    NEptuniooTot.Draw("same")
    NEptunioo1.Draw("same")
    NEptunioo2.Draw("same")
    NEptunioo3.Draw("same")
    NEptunioo4.Draw("same")



    '''leg1 = TLegend(0.435, 0.71, 0.85, 0.59)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.4)
    leg1.SetFillStyle(0)
    leg1.AddEntry(histE, "Data from triple source", 'lf')
    leg1.AddEntry(NEptunioo1, "Gauss1: ^{237}Np 4771 keV peak", 'lf')
    leg1.AddEntry(NEptunioo2, "Gauss2: ^{237}Np 4788 keV peak", 'lf')
    leg1.AddEntry(NEptunioo3, "Gauss3: ^{237}Np 4640 keV peak", 'lf')
    leg1.AddEntry(NEptunioo4, "Gauss4: ^{237}Np 4872 keV peak", 'lf')
    leg1.AddEntry(NEptuniooTot, "Gauss1 + Gauss2 + Gauss3 + Gauss4 : fit on ^{237}Np  peaks", 'lf')
    leg1.Draw("same")
    c3.SaveAs('test.png')'''
    input()
    

