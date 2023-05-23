import pandas as pd
import numpy as np
import uproot
import math
from ROOT import TF1,TAxis, TH1D,TH2D, TCanvas, kAzure,kBlue, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFitResultPtr, TFile,TGraphErrors,gPad

#import sys
#sys.path.append('Python/utils')

#from StyleFormatter import SetGlobalStyle, SetObjectStyle

#SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

def diamondsWP(input_path,root_file):

    df=pd.read_csv(input_path)
    df["HV err"]=5 
    df["centroid err"]=1 #bho è solo per avere il plot questo va rivisto
    df[" FWHM err"]=1 #anche qui da calcolare dopo
    df["Net Area err"]=1 #stessa cosa
    df["resolution"]=df["FWHM (chn)"]/df["centroid (chn)"]
    df["resolution err"]=np.sqrt((df[" FWHM err"]/df["centroid (chn)"])**2+(df["FWHM (chn)"]*df["centroid err"]/(df["centroid (chn)"]**2))**2)

    graphResolution=TGraphErrors(len(df),np.asarray(df['HV (V)'],'d'),np.asarray(df['resolution'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['resolution err'],'d'))
    graphResolution.SetTitle("Risoluzione vs HV")
    graphResolution.GetXaxis().SetTitle("HV [V]")
    graphResolution.GetYaxis().SetTitle("Risoluzione")

    graphCentr=TGraphErrors(len(df),np.asarray(df['HV (V)'],'d'),np.asarray(df['centroid (chn)'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['centroid err'],'d'))
    graphCentr.SetTitle("Centroide vs HV")
    graphCentr.GetXaxis().SetTitle("HV [V]")
    graphCentr.GetYaxis().SetTitle("Centroide")

    cR = TCanvas("cR", "cR" ,1280, 720)
    cR.cd()
    #SetObjectStyle(graphResolution,color=kAzure+3)
    graphResolution.Draw("AP")
    input("press enter to to close")
    cC = TCanvas("cC", "cC" ,1280, 720)
    cC.cd()
    #SetObjectStyle(graphCentr,color=kAzure+3)
    graphCentr.Draw("AP")
    input("press enter to to close2")
    gPad.Modified()
    gPad.Update()

    root_file.cd()
    cR.Write()
    cC.Write()

if __name__ == '__main__':
    
    outfilePath = 'data/output/Diamond/WorkingPoint.root'
    root_file = TFile(outfilePath, 'recreate')
    filePaths = 'data/input/Diamonds/Monday/HVdiamond.csv'
    diamondsWP(filePaths,root_file)





