import pandas as pd
import numpy as np
import sys
#import argparse

sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta, TF1, gStyle, TPaveStats, gPad,TGraphErrors, TLatex

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
    infilenames= ['data/input/gamma/friday/pos4min7deg.mca','data/input/gamma/friday/pos5min11deg.mca',
                  'data/input/gamma/friday/pos6min15deg.mca','data/input/gamma/friday/pos7min19deg.mca',
                  'data/input/gamma/friday/pos8min23deg.mca','data/input/gamma/friday/pos9min27deg.mca',
                  'data/input/gamma/friday/pos10min31deg.mca']
    colors = [kBlue , kRed, kGreen, kOrange, kBlack, kAzure+3, kMagenta]

    histos=[]
    cc = TCanvas('cc','cc',1000,1000)
    for idx, (infilename,color) in enumerate(zip(infilenames,colors)):
        hosto=CreateHist(infilename)
        histos.append(hosto)
        SetObjectStyle(histos[idx],color=color, fillalpha=0.5)
        histos[idx].Draw("hist,same")
        del hosto
   
        cc.Modified()
        cc.Update()
    cc.Draw()
    
    input()