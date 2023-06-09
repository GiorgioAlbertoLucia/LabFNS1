import pandas as pd
import numpy as np
import sys
import math
sys.path.append('Python/utils')

from ROOT import TCanvas, TH1D, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TGraphErrors, TMultiGraph, TLegend, gStyle, TF1, TPad 
from ReadMCA import CreateHist, Centroid, FWHM, HistoComparison

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1., titleoffsetx=0.9, titleoffset= 0.6, opttitle=1)

def WriteHisto(infilenames, histofile,rebin=1): 
    # returns (centroids, FWHM) of MCA spectra in infilenames array
    colors = [kBlue, kRed, kGreen, kOrange, kBlack, kViolet, kAzure]
    #print('ciao')
    histofile.cd()
    histos=[]
    for idx, (infilename, color) in enumerate(zip(infilenames,colors)):
        histos.append(CreateHist(infilename,idx))
        #canva = TCanvas('c'+str(idx),'c'+str(idx), 1700, 1200)
        #histos[idx].SetLineStyle(1)
        SetObjectStyle(histos[idx], color=color, fillalpha=1, linewidth=1)
        #histos[idx].Rebin(2)
        #histos[idx].Draw("HIST L")
        histos[idx].Rebin(rebin)
        histos[idx].SetDrawOption("E")
        #histos[idx].Draw("E")
        histos[idx].Write()
        #print(infilename)
    return histos
    histofile.Close()
        #canva.Write()
    #print('Fatto')
    
def HistosFeaturesGaus(histos, fitbound):
    Centroids = []
    errCentroids = []
    Resolutions = []
    errResolutions = []
    FWHMs = []
    errFWHMs = []
    times = []
    for ind in range(len(histos)):
        histos[ind].Fit("gaus","L","",fitbound[ind][0],fitbound[ind][1])
        gaussian = histos[ind].GetFunction("gaus")
        FWHMs.append(2.355*gaussian.GetParameter(2))
        errFWHMs.append(2.355*gaussian.GetParError(2))
        #print(FWHMs[ind])
        Centroids.append(gaussian.GetParameter(1))
        errCentroids.append(gaussian.GetParError(1))
        Resolutions.append(FWHMs[-1]/Centroids[-1])
        errResolutions.append(math.sqrt((FWHMs[-1]*FWHMs[-1]*errCentroids[-1]*errCentroids[-1])/(Centroids[-1]*Centroids[-1]*Centroids[-1]*Centroids[-1]) + 
                                         (errFWHMs[-1]*errFWHMs[-1])/(Centroids[-1]*Centroids[-1])))
        times.append(5+ind*80)
    print(errFWHMs)
    return Centroids,errCentroids,FWHMs,errFWHMs,Resolutions,errResolutions,times


def HistosFeatures(histos, centroidbound):
    Centroids = []
    errCentroids = []
    FWHMs = []
    errFWHMs = []
    times = []
    for ind in range(len(histos)):
        FWHMs.append(FWHM(histos[ind])[0])
        errFWHMs.append(FWHM(histos[ind])[1])
        #print(FWHMs[ind])
        Centroids.append(Centroid(histos[ind],centroidbound[ind][0],centroidbound[ind][1])[0])
        errCentroids.append(Centroid(histos[ind],centroidbound[ind][0],centroidbound[ind][1])[1])
        times.append(5+ind*80)
    return Centroids,errCentroids,FWHMs,errFWHMs,times

def FeaturePlot(feature, errfeatures, times, legend, legcoord, legname, title, savename, titleaxis):
    #print(features)
    colors = [kBlue, kRed, kGreen, kOrange, kBlack, kViolet]
    featureCanva = TCanvas(title, title, 1600, 1600)
    featureGraph = TMultiGraph(title,title)
    for idx in range(len(feature)):
        #if(idx != 0):
            featureCanva.cd()
            print(idx)
            graph = TGraphErrors(len(feature[idx]),np.asarray(times[idx],'d'),np.asarray(feature[idx],'d'),
                         np.asarray([0]*len(feature),'d'),np.asarray(errfeatures[idx],'d'))
            print(legend[idx])
            graph.SetName(legend[idx])
            graph.SetTitle(legend[idx])
            SetObjectStyle(graph,markerstyle=21,color=colors[idx])
            graph.SetDrawOption('P')
            graph.SetMarkerSize(3)
            graph.SetLineWidth(3)
            featureGraph.Add(graph)
    featureCanva.SetLogy()
    featureGraph.SetTitle(titleaxis)
    featureGraph.Draw('ALP')    
    (featureGraph.GetYaxis()).LabelsOption("v")
    featureCanva.Modified()
    featureCanva.Update()
    featureCanva.BuildLegend(legcoord[0],legcoord[1],legcoord[2],legcoord[3],legname)
    featureCanva.SaveAs(savename)
    return featureGraph

#def ResolutionPlot(centroids, fwhms, file):

if __name__ == "__main__":

    infilename30 = ['data/input/Diamond/TimeEv/30lun1.mca','data/input/Diamond/TimeEv/30lun2.mca',
                   'data/input/Diamond/TimeEv/30lun3.mca']
    histofile30 = TFile('data/input/Diamond/TimeEvHistos/histo+30.root', 'recreate')
    CentroidBoundaries30 = [(964,1076),(670,1010),(61,984)]
    infilename60 = ['data/input/Diamond/TimeEv/60lun1.mca','data/input/Diamond/TimeEv/60lun2.mca',
                   'data/input/Diamond/TimeEv/60lun3.mca']
    histofile60 = TFile('data/input/Diamond/TimeEvHistos/histo+60.root', 'recreate')
    CentroidBoundaries60 = [(1252, 1346), (1202, 1326), (1120,1326)]
    infilename90 = ['data/input/Diamond/TimeEv/90lun1.mca','data/input/Diamond/TimeEv/90lun2.mca',
                   'data/input/Diamond/TimeEv/90lun3.mca','data/input/Diamond/TimeEv/90lun4.mca',
                   'data/input/Diamond/TimeEv/90lun5.mca']
    histofile90 = TFile('data/input/Diamond/TimeEvHistos/histo+90.root', 'recreate')
    CentroidBoundaries90 = [(1328,1372), (1326, 1376), (1314, 1374), (1290, 1374), (1280, 1378)]
    infilenameMinus30 = ['data/input/Diamond/TimeEv/-30lun1.mca','data/input/Diamond/TimeEv/-30lun2.mca',
                   'data/input/Diamond/TimeEv/-30lun3.mca','data/input/Diamond/TimeEv/-30lun4.mca',
                   'data/input/Diamond/TimeEv/-30lun5.mca','data/input/Diamond/TimeEv/-30lun6.mca',
                   'data/input/Diamond/TimeEv/-30lun7.mca']
    histofileMinus30 = TFile('data/input/Diamond/TimeEvHistos/histo-30.root', 'recreate')
    CentroidBoundariesMinus30 = [(1190,1250), (1184,1246), (1176,1246), (1162,1248), (1140,1242), (1130,1252), (1134,1248)]
    infilenameMinus60 = ['data/input/Diamond/TimeEv/-60lun1.mca','data/input/Diamond/TimeEv/-60lun2.mca',
                   'data/input/Diamond/TimeEv/-60lun3.mca','data/input/Diamond/TimeEv/-60lun4.mca',
                   'data/input/Diamond/TimeEv/-60lun5.mca','data/input/Diamond/TimeEv/-60lun6.mca',
                   'data/input/Diamond/TimeEv/-60lun7.mca']
    histofileMinus60 = TFile('data/input/Diamond/TimeEvHistos/histo-60.root', 'recreate')
    CentroidBoundariesMinus60 = [(1274,1308), (1274,1308), (1270,1310), (1274, 1308), (1268,1312), (1264,1310), (1266, 1310)]
    infilenameMinus90 = ['data/input/Diamond/TimeEv/-90lun1.mca','data/input/Diamond/TimeEv/-90lun2.mca',
                   'data/input/Diamond/TimeEv/-90lun3.mca','data/input/Diamond/TimeEv/-90lun4.mca',
                   'data/input/Diamond/TimeEv/-90lun5.mca']
    histofileMinus90 = TFile('data/input/Diamond/TimeEvHistos/histo-90.root', 'recreate')
    CentroidBoundariesMinus90 = [(1303,1314), (1303,1316), (1302, 1318), (1301, 1318), (1298,1317)]
    
    dict = {'+30': [infilename30, histofile30, CentroidBoundaries30], '+60': [infilename60, histofile60, CentroidBoundaries60], 
            '+90': [infilename90, histofile90, CentroidBoundaries90], '-30': [infilenameMinus30, histofileMinus30, CentroidBoundariesMinus30],
            '-60': [infilenameMinus60, histofileMinus60, CentroidBoundariesMinus60], '-90': [infilenameMinus90, histofileMinus90, CentroidBoundariesMinus90]}

    for key in dict.keys():
        dict[key] = [dict[key],WriteHisto(dict[key][0], dict[key][1],8)]
    #print(dict['+30'][0][2])
    #print(dict['+30'])
    #Features = [HistosFeatures(dict[x][1], dict[x][0][2]) for x in dict.keys()]
    
    Features = []
    for key in dict.keys():
        Features.append(HistosFeaturesGaus(dict[key][1], dict[key][0][2]))

    Legend = list(dict.keys())
    LegendName = 'Applied voltage'
    Centroids = [i[0] for i in Features]
    errCentroids = [i[1] for i in Features]
    FWHMs = [i[2] for i in Features]
    errFWHMs = [i[3] for i in Features]
    Resolutions = [i[4] for i in Features]
    errResolutions = [i[5] for i in Features]
    Times = [i[6] for i in Features]

    #Resolutions = []
    #errResolutions = []
    #for F,eF,C,eC in zip(FWHMs,errFWHMs,Centroids,errCentroids):
    #    ResList = [F[z]/C[z] for z in range(len(F))]
    #    Resolutions.insert(len(Resolutions),ResList)
    #    errResList = [math.sqrt(F[z]*F[z]*eC[z]*eC[z] + (eF[z]*eF[z])/(C[z]*C[z]*C[z]*C[z])) for z in range(len(F))]
    #    errResolutions.insert(len(Resolutions),ResList)
    
    #print(Resolutions, '\n')

    #TimeEvolutionCharacterization = TCanvas("Detector's performance time evolution","Detector's performance time evolution",2200,1200)
    #TimeEvolutionCharacterization.Divide(3,1)
#
    TitleCanvaFWHMs = 'FWHM comparison'
    PathCanvaFWHMs = 'data/output/Diamond/TimeFWHMs.pdf'
    LegendCoordinates = [0.65,0.65,0.85,0.85]
    TitleAxisLabelsFWHMs = "FWHM comparison;t[s];FWHM"
    #TimeEvolutionCharacterization.cd(0)
    FeaturePlot(FWHMs, errFWHMs, Times, Legend, LegendCoordinates, LegendName, TitleCanvaFWHMs, PathCanvaFWHMs, TitleAxisLabelsFWHMs)
    #TimeEvolutionCharacterization.Modified()
    #TimeEvolutionCharacterization.Update()
###
    TitleCanvaCentroids = 'Centroids comparison'
    PathCanvaCentroids = 'data/output/Diamond/TimeCentroids.pdf'
    LegendCoordinates = [0.6,0.5,0.8,0.3]
    TitleAxisLabelsCentroids = "Centroid comparison;t[s];Centroid"
    #TimeEvolutionCharacterization.cd(1)
    FeaturePlot(Centroids, errCentroids, Times, Legend, LegendCoordinates, LegendName, TitleCanvaCentroids, PathCanvaCentroids, TitleAxisLabelsCentroids)
    #TimeEvolutionCharacterization.Modified()
    #TimeEvolutionCharacterization.Update()
###
    #TitleCanvaResolution = 'Resolution comparison'
    #PathCanvaResolution = 'data/output/Diamond/TimeResolutions.pdf'
    #TitleAxisLabelsResolution = "Resolution comparison;t[s];Resolution"
    #LegendCoordinates = [0.65,0.65,0.85,0.85]
    #TimeEvolutionCharacterization.cd(1)
    #(FeaturePlot(Resolutions, errResolutions, Times, Legend, LegendCoordinates, LegendName, TitleCanvaResolution, PathCanvaResolution, TitleAxisLabelsResolution)).Draw('ALP')
    #TimeEvolutionCharacterization.Modified()
    #TimeEvolutionCharacterization.Update()
#
    #TimeEvolutionCharacterization.SaveAs('data/output/Diamond/TimeEvolutionCharacterization.pdf')

    ResCompLegend = TLegend(0.77,0.67,0.92,0.82)
    ResCompLegend.SetHeader('Start Time')
    dict['+60'][1][0].Scale(1/dict['+60'][1][0].GetMaximum())
    dict['+60'][1][1].Scale(1/dict['+60'][1][1].GetMaximum())
    dict['+60'][1][2].Scale(1/dict['+60'][1][2].GetMaximum())
    ResCompLegend.AddEntry(dict['+60'][1][0],'5s','lf')
    ResCompLegend.AddEntry(dict['+60'][1][1],'85s','lf')
    ResCompLegend.AddEntry(dict['+60'][1][2],'165s','lf')
    ResCompLegend.SetTextFont(42)
    ResCompLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    ResCompLegend.SetFillStyle(0)
    ResCompboundaries = [1000,0.,1500.,1.1]
    ResCompCanva = 'MCA normalised count distributions HV=+60V;Channel;Counts [a.u]'
    HistoComparison([dict['+60'][1][0],dict['+60'][1][1],dict['+60'][1][2]], ResCompLegend, ResCompCanva,
                    ResCompboundaries, 'data/output/Diamond/ResComp.pdf',[1,1,1],[kRed,kAzure+3,kOrange-3],[0.9,0.7,0.6])


