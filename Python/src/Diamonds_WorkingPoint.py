import pandas as pd
import numpy as np
import uproot
import math
import sys
sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TF1,TAxis, TH1D,TH2D, TCanvas, kAzure,kBlue, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFitResultPtr, TFile,TGraphErrors,gPad,kOrange,kBlack,kMagenta

#import sys
#sys.path.append('Python/utils')

#from StyleFormatter import SetGlobalStyle, SetObjectStyle

#SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

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


def diamondsWP(input_path,root_file):

    df=pd.read_csv(input_path)
    df["HV err"]=0
    df["centroid err post"]=[3,3,4,4,4,5,14,30,8,7,6,6,5,4]
    df["centroid post"]=[1328,1331,1327,1318,1321,1309,1272,1230,1357,1378,1370,1384,1387,1384] #bho è solo per avere il plot questo va rivisto
    df[" FWHM err"]=[0.89,0.24,0.2,0.2,0.2,0.2,0.2,1.56,0.45,0.3,0.3,0.3,0.45,0.3 ]#anche qui da calcolare dopo
    df["Net Area err"]=1 #stessa cosa
    df["resolution"]=df["FWHM (chn)"]/df["centroid post"]
    df["resolution err"]=np.sqrt((df[" FWHM err"]/df["centroid post"])**2+(df["FWHM (chn)"]*df["centroid err post"]/(df["centroid post"]**2))**2)

    graphResolution=TGraphErrors(len(df),np.asarray(df['HV (V)'],'d'),np.asarray(df['resolution'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['resolution err'],'d'))
    graphResolution.SetTitle("Risoluzione vs HV")
    graphResolution.GetXaxis().SetTitle("HV [V]")
    graphResolution.GetYaxis().SetTitle("Resolution")
    graphResolution.SetMarkerStyle(8)
    graphResolution.SetMarkerSize(1.25)
    graphResolution.SetMarkerColor(kAzure+3)

    graphCentr=TGraphErrors(len(df),np.asarray(df['HV (V)'],'d'),np.asarray(df['centroid post'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['centroid err post'],'d'))
    graphCentr.SetTitle("Centroide vs HV")
    graphCentr.GetXaxis().SetTitle("HV [V]")
    graphCentr.GetYaxis().SetTitle("Centroid [chn]")
    graphCentr.SetMarkerStyle(8)
    graphCentr.SetMarkerSize(1.25)
    graphCentr.SetMarkerColor(kRed+4)
    cR = TCanvas("cR", "cR" ,1280, 720)
    cR.cd()
    #SetObjectStyle(graphResolution,color=kAzure+3)
    graphResolution.Draw("AP")
    text =TLatex(0.30, 0.7,"Diamond detector, with ^{241}Am source")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize()*0.7)
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.30, 0.62,"Acquisition time:30s")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    input("press enter to to close")
    cC = TCanvas("cC", "cC" ,1280, 720)
    cC.cd()
    #SetObjectStyle(graphCentr,color=kAzure+3)
    graphCentr.Draw("AP")
    text =TLatex(0.30, 0.7,"Diamond detector, with ^{241}Am source")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize()*0.7)
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.30, 0.62,"Acquisition time:30s")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    input("press enter to to close2")
    gPad.Modified()
    gPad.Update()

    root_file.cd()
    cR.Write()
    cC.Write()

if __name__ == '__main__':
    
    outfilePath = 'data/output/Diamond/WorkingPoint.root'
    root_file = TFile(outfilePath, 'recreate')
    filePaths = 'data/input/HVdiamond.csv'
    diamondsWP(filePaths,root_file)
    
    infilenames= ['data/input/Diamonds/Monday/HV/-50HV.mca','data/input/Diamonds/Monday/HV/-100HV.mca',
                  'data/input/Diamonds/Monday/HV/-150HV.mca','data/input/Diamonds/Monday/HV/-200HV.mca',
                  'data/input/Diamonds/Monday/HV/-250HV.mca','data/input/Diamonds/Monday/HV/-300HV.mca',
                  'data/input/Diamonds/Monday/HV/-400HV.mca']
    #infilenames= ['data/input/Diamonds/Monday/HV/50HV.mca','data/input/Diamonds/Monday/HV/100HV.mca',
                  #'data/input/Diamonds/Monday/HV/150HV.mca','data/input/Diamonds/Monday/HV/200HV.mca',
                  #'data/input/Diamonds/Monday/HV/250HV.mca','data/input/Diamonds/Monday/HV/300HV.mca',
                  #'data/input/Diamonds/Monday/HV/400HV.mca']
    colors = [kBlue+3 , kRed, kGreen, kOrange-3, kBlack, kAzure, kMagenta]
    names=["-50 V","-100 V","-150 V","-200 V","-250 V","-300 V","-400 V"]
    #names=["50 V","100 V","150 V","200 V","250 V","300 V","400 V"]
    histos=[]
    cc = TCanvas('cc','cc',1000,1000)
    leg = TLegend(0.435, 0.71, 0.85, 0.59)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    for idx, (infilename,color) in enumerate(zip(infilenames,colors)):
        hosto=CreateHist(infilename)
        histos.append(hosto)
        SetObjectStyle(histos[idx],color=color, fillalpha=0.5)
        histos[idx].SetFillColorAlpha(color, 0.5);
        histos[idx].Draw("hist,same")
        leg.AddEntry(histos[idx], f"HV={ names[idx]}", 'lf')
        del hosto

    
        cc.Modified()
        cc.Update()
    leg.Draw("same")
    cc.Draw()
    
    input()





