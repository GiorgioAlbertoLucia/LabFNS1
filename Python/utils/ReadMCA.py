import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta

def CreateHist(infile,number):
    df = pd.read_csv(infile,'\n',skiprows=14,header=None,skipfooter=44, engine='python')
    hist = TH1D("Hist"+str(number),"Hist"+str(number),len(df),0,len(df))
    hist.FillN(len(df),np.array(list(range(len(df))),'d'),np.asarray(df,'d'))
    return hist


if __name__ == '__main__':
    infilenames= ['data/input/Monday/-30lun1.mca','data/input/Monday/-30lun2.mca',
                 'data/input/Monday/-30lun3.mca','data/input/Monday/-30lun4.mca',
                 'data/input/Monday/-30lun5.mca','data/input/Monday/-30lun6.mca',
                'data/input/Monday/-30lun7.mca']
    colors = [kBlue , kRed, kGreen, kOrange, kBlack, kAzure, kMagenta]

    histos=[]
    c = TCanvas('c','c',1000,1000)
    for idx, (infilename,color) in enumerate(zip(infilenames,colors)):
        histos.append(CreateHist(infilename,idx))
        SetObjectStyle(histos[idx],color=color, fillalpha=0.5)
        histos[idx].Draw("hist,same")
   
        c.Modified()
        c.Update()
    c.SaveAs('data/output/Test.pdf')
    input()
