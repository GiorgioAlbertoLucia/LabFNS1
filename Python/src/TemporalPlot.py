import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, TH1D, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kMagenta, TFile, TGraphErrors 
from ReadMCA import CreateHist, Centroid, FWHM

def HistoFeatures(infilenames): 
    # returns (centroids, FWHM) of MCA spectra in infilenames array
    colors = [kBlue , kRed, kGreen, kOrange, kBlack, kAzure, kMagenta]
    
    histos=[]
    for idx, (infilename, color) in enumerate(zip(infilenames,colors)):
        histos.append(CreateHist(infilename,idx))
        #SetObjectStyle(histos[idx],color=color, fillalpha=0.5)
        #histos[idx].Draw("hist,same")
    
    centroids = []
    FWHMs = []
    times = []

    for ind in histos:
        FWHMs.append(FWHM(histos[ind]))
        centroids.append(Centroid(histos[ind]))
        times.append(5+ind*80)

    return zip(centroids,FWHMs,times)

def FeaturePlot(feature, times, file):
    #print(features)
    graph = TGraphErrors(len(feature),np.asarray(times),np.asarray(feature),
                     0.,0.)
    graph.Write()


if __name__ == "__main__":

    infilename30 = ['data/input/Diamonds/Monday/30lun1.mca','data/input/Diamonds/Monday/30lun2.mca',
                   'data/input/Diamonds/Monday/30lun3.mca']
    infilename60 = ['data/input/Diamonds/Monday/60lun1.mca','data/input/Monday60lun2.mca',
                   'data/input/Diamonds/Monday/60lun3.mca']
    #infilename90 = ['data/input/Diamonds/Monday/90lun1.mca','data/input/Diamonds/Monday/90lun2.mca',
    #               'data/input/Diamonds/Monday/90lun3.mca','data/input/Diamonds/Monday/90lun4.mca',
    #               'data/input/Diamonds/Monday/90lun5.mca','data/input/Diamonds/Monday/90lun6.mca',
    #               'data/input/Diamonds/Monday/90lun7.mca']
    infilenameMinus30 = ['data/input/Diamonds/Monday/-30lun1.mca','data/input/Diamonds/Monday/-30lun2.mca',
                   'data/input/Diamonds/Monday/-30lun3.mca','data/input/Diamonds/Monday/-30lun4.mca',
                   'data/input/Diamonds/Monday/-30lun5.mca','data/input/Diamonds/Monday/-30lun6.mca',
                   'data/input/Diamonds/Monday/-30lun7.mca']
    #infilenameMinus60 = ['data/input/Diamonds/Monday/-60lun1.mca','data/input/Diamonds/Monday/-60lun2.mca',
    #               'data/input/Diamonds/Monday/-60lun6.mca','data/input/Diamonds/Monday/-60lun4.mca',
    #               'data/input/Diamonds/Monday/-60lun5.mca','data/input/Diamonds/Monday/-60lun6.mca',
    #               'data/input/Diamonds/Monday/-60lun7.mca']
    #infilenameMinus90 = ['data/input/Diamonds/Monday/90lun1.mca','data/input/Diamonds/Monday/90lun2.mca',
    #               'data/input/Diamonds/Monday/-90lun9.mca','data/input/Diamonds/Monday/-90lun4.mca',
    #               'data/input/Diamonds/Monday/-90lun5.mca','data/input/Diamonds/Monday/-90lun6.mca',
    #               'data/input/Diamonds/Monday/-90lun7.mca']
    dict = {'+30': infilename30, '+60': infilename60, '-30': infilenameMinus30}

    Features = [HistoFeatures(dict[x]) for x in dict]
    #Features.append(HistoFeatures(infilename30))
    #Features.append(HistoFeatures(infilename60))
    #Features.append(HistoFeatures(infilename90))
    #Features.append(HistoFeatures(infilenameMinus30))
    #Features.append(HistoFeatures(infilenameMinus60))
    #Features.append(HistoFeatures(infilenameMinus90))

    outfilepathFWHM = ('data/output/DiamondFWHM.root')
    outfilepathCentroids = ('data/output/DiamondCentroids.root')

    fileFWHM = TFile(outfilepathFWHM,'recreate')
    for dataset in Features:
        FeaturePlot(Features[dataset][1],Features[dataset][3],fileFWHM)
    fileFWHM.Close()

    fileCentroid = TFile(outfilepathCentroids,'recreate')
    for dataset in Features:
        FeaturePlot(Features[dataset][0],Features[dataset][3],fileCentroid)
    fileCentroid.Close()
    



