import pandas as pd
import numpy as np
import sys
import math
sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta, kViolet, Math

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
    a = 0.318
    sa = 0.008
    b = -30
    sb = 40
    EnHist = TH1D(histo.GetTitle(),histo.GetTitle(),len(dataarray),ChEnConv(0,a,b,gain),ChEnConv(len(dataarray),a,b,gain))
    EnbinEntries = [ChEnConv(bin,a,b,gain) for bin in range(histo.GetNbinsX())]
    EnHist.FillN(len(dataarray),np.asarray(EnbinEntries,'d'),np.asarray(dataarray,'d'))
    #CalErr = CalEnergyErr(a,sa,b,sb,gain)
    #for binnumber in range(EnHist.GetNbinsX()):
    #    EnHist.SetBinError(binnumber,np.sqrt(EnHist.GetBinContent(binnumber) + CalErr*CalErr)) 
    #print(EnHist.Integral())
    return EnHist

def ChEnConv(chn,a,b,gain):
    return (chn-b)/(a*gain)

def CalEnergyErr(a,sa,b,sb,gain,cov,en,sen):
    #+ 2*sa*sb*( (b)/(a*a*a*gain) )
    ch = (0.3176)*gain*en - 33.26
    print('CANALEEEEEEEEEEEEEEEEE')
    print(ch)
    print('\n\n\n\n\n')
    sch = np.sqrt( (0.3176*0.3176*gain*gain*sen*sen) + (en*en*gain*gain*sa*sa) + sb*sb)
    sEn = np.sqrt( (sb*sb)/(a*a*gain*gain) + ((ch-b)*(ch-b)*sa*sa)/(a*a*a*a*gain*gain) + 2*cov*( (ch-b)/(a*a*a*gain*gain) ) + ((sch*sch)/(a*a*gain*gain)) )
    return sEn

def FitStats(fitfunct):
    Chisquare = fitfunct.GetChisquare()
    Chicrit = Math.chisquared_quantile_c(0.05,fitfunct.GetNDF())
    NDegFreedom = fitfunct.GetNDF()
    Pvalue = fitfunct.GetProb()
    print('Chi Square:', Chisquare, ', Degrees of freedom:', NDegFreedom, ', Critical Chi Square:', Chicrit,', P-value: ', Pvalue)

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


def DictHistos(dict, histofile, color,rebin=0):
    #colors = [kBlue, kRed, kGreen, kOrange, kBlack, kViolet]
    colors = [color, color, color, color, color, color]
    histofile.cd()
    dictkeys = list(dict.keys()) 
    for idx, (dictkey, color) in enumerate(zip(dictkeys,colors)):
        dict[dictkey] = [dict[dictkey],CreateHist(dict[dictkey][0],idx,dictkeys[idx],dict[dictkey][1])]
        if(rebin != 0):
            dict[dictkey][1].Rebin(rebin)
        dict[dictkey][1].SetLineColor(4)
        SetObjectStyle(dict[dictkey][1], color=color, fillalpha=1, linewidth=1)
        dict[dictkey][1].SetDrawOption("E")
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
