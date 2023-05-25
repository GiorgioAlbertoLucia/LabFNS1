import pandas as pd
import numpy as np
import sys
#import argparse

sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta, TF1, gStyle, TPaveStats, gPad

def CreateHist(infile):
    data = []

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

if __name__ == '__main__':

    #parser = argparse.ArgumentParser(description='Arguments')
    #parser.add_argument('infilename', metavar='text')
    #args = parser.parse_args()
    # infilename -> args.infilename 
   # python3 Python/src/TripleSouce.py data/input/...

    infilename='data/input/Diamonds/Tuesday/sorgente_tripla.mca'
    c = TCanvas('c','c',1000,1000)
    histo=CreateHist(infilename)
    histo.Draw("E")

    gStyle.SetOptFit(1111)
    Americio = TF1('Americio', "gaus", 1700, 1720)
    Curio = TF1('CUrio', "gaus", 1800, 1825)
    Neptunio1=TF1('Neptunio1', "gaus", 1430, 1460)
    Neptunio2=TF1('Neptunio2', "gaus", 1460, 1510)
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

    Neptunio=TF1('Neptunio', "gaus(0)+gaus(3)+gaus(6)", 1428, 1525)
    Neptunio.SetParNames("Norm_{1}", "#mu_{1}", "#sigma_{1}", "Norm_{2}", "#mu_{2}", "#sigma_{2}", "Norm_{3}", "#mu_{3}", "#sigma_{3}")
    Neptunio.SetParameter(1,Neptunio1.GetParameter(1))
    Neptunio.SetParameter(4,Neptunio2.GetParameter(1))
    Neptunio.SetParameter(7,Neptunio3.GetParameter(1))
    Neptunio.SetParameter(2,Neptunio1.GetParameter(2))
    Neptunio.SetParameter(5,Neptunio2.GetParameter(2))
    Neptunio.SetParameter(8,Neptunio3.GetParameter(2))

    c.Update()
    histo.Fit(Neptunio,"RM")
    


    Americio.SetLineColor(kOrange-3)
    Curio.SetLineColor(kBlue+3)
    Neptunio1.SetLineColor(kRed)
    Neptunio2.SetLineColor(kRed+2)
    Neptunio3.SetLineColor(kRed+4)
    Neptunio.SetLineColor(kOrange-3)
    Americio.Draw("same")
    Curio.Draw("same")
    #Neptunio3.Draw("same")
    #Neptunio2.Draw("same")
    #Neptunio1.Draw("same")
    Neptunio.Draw("same")
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
    gPad.Update()
    input()
    

 