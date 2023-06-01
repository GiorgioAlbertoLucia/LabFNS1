import pandas as pd
import numpy as np
import sys
import math
sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta, kViolet

def GetPandas(infile):
    df = pd.read_csv(infile, '\n', header = None, engine='python')
    df = df.iloc[df.index[df[0] == '<<DATA>>'].tolist()[0] + 1: df.index[df[0] == '<<END>>'].tolist()[0] , :]
    df = df.reset_index()
    return df


def CreateHist(infile,number,histtitle="",energyscale="chn"):
    #print(infile)
    df = GetPandas(infile)
    #df = pd.read_csv(infile, '\n', header=None, skiprows=14, nrows=2048)
    #df = pd.read_csv(infile,'\n',skiprows=14,header=None,skipfooter=44, engine='python')
    title = "Hist"+str(number)
    if(histtitle != ""):
        title = histtitle
    hist = TH1D(title,title,len(df),0,len(df))
    if(energyscale == "chn"):
        hist.FillN(len(df),np.asarray(list(range(len(df))),'d'),np.asarray(df[0],'d'))
        #print(hist.Integral())
    if(energyscale == "en200"):
        #print("ciao200")
        return EnergyHisto(hist,df[0],1)
    if(energyscale == "en1000"):
        #print("ciao1000")
        return EnergyHisto(hist,df[0],5)
    return hist

def EnergyHisto(histo, dataarray, gain):
    a = 0.3206
    sa = 0.0014
    b = -47
    sb = 7
    EnHist = TH1D(histo.GetTitle(),histo.GetTitle(),len(dataarray),ChEnConv(0,a,b,gain),ChEnConv(len(dataarray),a,b,gain))
    EnbinEntries = [ChEnConv(bin,a,b,gain) for bin in range(histo.GetNbinsX())]
    EnHist.FillN(len(dataarray),np.asarray(EnbinEntries,'d'),np.asarray(dataarray,'d'))
    CalErr = CalEnergyErr(a,sa,b,sb,gain)
    for binnumber in range(EnHist.GetNbinsX()):
        EnHist.SetBinError(binnumber,np.sqrt(EnHist.GetBinContent(binnumber) + CalErr*CalErr)) 
    #print(EnHist.Integral())
    return EnHist

def ChEnConv(chn,a,b,gain):
    return (chn-b)/(a*gain)

def CalEnergyErr(a,sa,b,sb,gain):
    sEn = np.sqrt( (sb*sb)/(a*a*gain*gain) + (b*b*sa*sa)/(a*a*a*a*gain*gain) + 2*sa*sb*( (b)/(a*a*a*gain) ) )
    return sEn

def HistoComparison(histos, legend, canvatags, boundaries, canvapath, rebins=[], colors = [], alphas = []):
    histoscopy = []
    for histo in histos:
        histoscopy.append(histo)
    canva = TCanvas('c', 'c', 1700,1200)
    hFrame = canva.DrawFrame(boundaries[0], boundaries[1], boundaries[2], boundaries[3], canvatags)
    for idx in range(len(histos)):
        if(rebins != []):
            histoscopy[idx].Rebin(rebins[idx])
        histoscopy[idx].Scale(1/histoscopy[idx].GetMaximum())
        SetObjectStyle(histoscopy[idx],color=colors[idx],fillalpha=alphas[idx],linewidth=1)
        histoscopy[idx].Draw("hist,same")
    legend.Draw("same")
    canva.SaveAs(canvapath)


def DictHistos(dict, histofile, rebin=0):
    colors = [kBlue, kRed, kGreen, kOrange, kBlack, kViolet]
    histofile.cd()
    dictkeys = list(dict.keys()) 
    for idx, (dictkey, color) in enumerate(zip(dictkeys,colors)):
        #if(dictkey == 'Gain 200'): 
        #print(idx)
        dict[dictkey] = [dict[dictkey],CreateHist(dict[dictkey][0],idx,dictkeys[idx],dict[dictkey][1])]
        if(rebin != 0):
            print(rebin)
            dict[dictkey][1].Rebin(rebin)
            #print(0)
            #print(dictkey)
        #if(dictkey != 'Gain 200'):
        #    dict[dictkey] = [dict[dictkey],CreateHist(dict[dictkey],idx,dictkeys[idx],"en1000")]
        #    #print(1)
        #    #print(dictkey)
        #if(dictkey == 'Stronzio'):
        #    dict[dictkey] = [dict[dictkey],CreateHist(dict[dictkey],idx,dictkeys[idx],"en1000")]
        ##print(1)
        ##print(dictkey)
        #canva = TCanvas('c'+str(idx),'c'+str(idx), 1700, 1200)
        #dict[dictkey][1].SetLineStyle(1)
        #print(dict[dictkey])
        print(dict[dictkey][0][1])
        SetObjectStyle(dict[dictkey][1], color=color, fillalpha=1, linewidth=1)
        #dict[dictkey][1].Draw("HIST L")
        dict[dictkey][1].SetDrawOption("E")
        #dict[dictkey][1].Draw("E")
        dict[dictkey][1].Write()

def Centroid(histo, lowerbound, upperbound):
    ROIinterval = upperbound-lowerbound
    centroid = []
    weight = []
    errcentroid = []
    for bin in range(ROIinterval):
        centroid.append(histo.GetBinContent(lowerbound + bin)*histo.GetBinCenter(lowerbound + bin))
        weight.append(histo.GetBinContent(lowerbound + bin))
    for bin in range(ROIinterval):
        numerator = sum(weight)*histo.GetBinCenter(lowerbound + bin) - histo.GetBinContent(lowerbound + bin)*histo.GetBinCenter(lowerbound + bin)
        errcentroid.append(((numerator*numerator)/(sum(weight)*sum(weight)*sum(weight)*sum(weight)))*histo.GetBinContent(lowerbound + bin)) 
    #print(sum(centroid))
    #print(sum(weight))
    #print('Centroid: ', sum(tuple(centroid))/sum(tuple(weight)))
    return sum(centroid)/sum(weight),math.sqrt(sum(errcentroid))

def FWHM(histo):
    errFWHM = 0
    maximum = histo.GetBinContent(histo.GetMaximumBin())
    leftbound = histo.GetBinCenter(histo.GetBin(histo.FindFirstBinAbove(maximum/2,1,1,histo.GetMaximumBin())-1))
    sigmabinleft = math.sqrt(maximum + histo.GetBinContent(histo.FindFirstBinAbove(maximum/2,1,1,histo.GetMaximumBin())-1))
    rightbound = histo.GetBinCenter(histo.GetBin(histo.FindLastBinAbove(maximum/2,1,histo.GetMaximumBin(),-1)-1))
    sigmabinright = math.sqrt(maximum + histo.GetBinContent(histo.FindLastBinAbove(maximum/2,1,histo.GetMaximumBin(),-1)-1))
    errFWHM = math.sqrt(sigmabinleft*sigmabinleft + sigmabinright*sigmabinright)
    #errFWHM = math.sqrt(2*maximum + histo.GetBinContent(histo.FindFirstBinAbove(maximum/2,1,1,histo.GetMaximumBin())-1) + histo.GetBinContent(histo.FindLastBinAbove(maximum/2,1,histo.GetMaximumBin(),-1)-1))
    return rightbound-leftbound,errFWHM

#def HistoComparison(histo1, histo2, legend, canvatags, boundaries, canvapath, rebin1=0, rebin2=0):
#    #histo1.SetNormFactor(1./histo1.Integral())
#    #histo2.SetNormFactor(1./histo2.Integral())
#    #histo1.Scale(histo1.GetNormFactor())
#    #histo2.Scale(histo2.GetNormFactor())
#    if(rebin1 != 0):
#        histo1.Rebin(rebin1)
#    if(rebin2 != 0):
#        histo1.Rebin(rebin2)
#    histo1.Scale(1/histo1.GetMaximum())
#    histo2.Scale(1/histo2.GetMaximum())
#    #histo1.Scale(1./histo1.Integral("width"))
#    #histo2.Scale(1./histo2.Integral("width"))
#    canva = TCanvas('c', 'c', 1700,1200)
#    hFrame = canva.DrawFrame(boundaries[0], boundaries[1], boundaries[2], boundaries[3], canvatags)
#    SetObjectStyle(histo1,color=kAzure+3,fillalpha=0.5,linewidth=1)
#    histo1.Draw("hist,same")
#    SetObjectStyle(histo2,color=kOrange-3,fillalpha=0.9,linewidth=1)
#    histo2.Draw("hist,same")
#    legend.Draw("same")

if __name__ == '__main__':
    infilenames= ['data/input/Diamond/TimeEv/30lun1.mca','data/input/Diamond/TimeEv/30lun2.mca',
                   'data/input/Diamond/TimeEv/30lun3.mca']
    colors = [kBlue, kRed, kGreen, kOrange, kBlack, kAzure, kMagenta]

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
