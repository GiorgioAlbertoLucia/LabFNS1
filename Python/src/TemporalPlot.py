import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, TH1D, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TGraphErrors, kFullCircle, TAttLine, TMultiGraph 
from ReadMCA import CreateHist, Centroid, FWHM

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

def WriteHisto(infilenames, histofile, centroidbound): 
    # returns (centroids, FWHM) of MCA spectra in infilenames array
    colors = [kBlue, kRed, kGreen, kOrange, kBlack, kViolet]
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
        histos[idx].SetDrawOption("E")
        #histos[idx].Draw("E")
        histos[idx].Write()
        #canva.Write()
    #print('Fatto')
    
    centroids = []
    FWHMs = []
    times = []


    for ind in range(len(histos)):

        FWHMs.append(FWHM(histos[ind]))
        #print(FWHMs[ind])
        centroids.append(Centroid(histos[ind],centroidbound[ind][0],centroidbound[ind][1]))
        times.append(5+ind*80)

    histofile.Close()
    return centroids,FWHMs,times

def FeaturePlot(feature, times, legend, legcoord, legname, title, savename):
    #print(features)
    colors = [kBlue, kRed, kGreen, kOrange, kBlack, kViolet]
    featureCanva = TCanvas(title, title, 1600, 1600)
    featureGraph = TMultiGraph(title,title)
    for idx in range(len(feature)):
        featureCanva.cd()
        print(idx)
        graph = TGraphErrors(len(feature[idx]),np.asarray(times[idx],'d'),np.asarray(feature[idx],'d'),
                     np.asarray([0.]*len(feature[idx]),'d'),np.asarray([0.2]*len(feature[idx]),'d'))
        print(legend[idx])
        graph.SetName(legend[idx])
        graph.SetTitle(legend[idx])
        SetObjectStyle(graph,markerstyle=21,color=colors[idx])
        graph.SetDrawOption('P')
        graph.SetMarkerSize(3)
        graph.SetLineWidth(3)
        featureGraph.Add(graph)

    featureGraph.Draw('ALP')    
    featureCanva.Modified()
    featureCanva.Update()
    featureCanva.BuildLegend(legcoord[0],legcoord[1],legcoord[2],legcoord[3],legname)
    featureCanva.SaveAs(savename)

#def ResolutionPlot(centroids, fwhms, file):

if __name__ == "__main__":

    infilename30 = ['data/input/Diamond/TimeEv/30lun1.mca','data/input/Diamond/TimeEv/30lun2.mca',
                   'data/input/Diamond/TimeEv/30lun3.mca']
    histofile30 = TFile('data/input/Diamond/TimeEvHistos/histo+30.root', 'recreate')
    CentroidBoundaries30 = [(964,1076),(670,1010),(61,984)]
    infilename60 = ['data/input/Diamond/TimeEv/60lun1.mca','data/input/Diamond/TimeEv/60lun2.mca',
                   'data/input/Diamond/TimeEv/60lun3.mca']
    histofile60 = TFile('data/input/Diamond/TimeEvHistos/histo+60.root', 'recreate')
    CentroidBoundaries60 = [(1256, 1332), (1216, 1314), (1144,1294)]
    infilename90 = ['data/input/Diamond/TimeEv/90lun1.mca','data/input/Diamond/TimeEv/90lun2.mca',
                   'data/input/Diamond/TimeEv/90lun3.mca','data/input/Diamond/TimeEv/90lun4.mca',
                   'data/input/Diamond/TimeEv/90lun5.mca']
    histofile90 = TFile('data/input/Diamond/TimeEvHistos/histo+90.root', 'recreate')
    CentroidBoundaries90 = [(1334,1372), (1328, 1372), (1326, 1370), (1306, 1368), (1288, 1368)]
    infilenameMinus30 = ['data/input/Diamond/TimeEv/-30lun1.mca','data/input/Diamond/TimeEv/-30lun2.mca',
                   'data/input/Diamond/TimeEv/-30lun3.mca','data/input/Diamond/TimeEv/-30lun4.mca',
                   'data/input/Diamond/TimeEv/-30lun5.mca','data/input/Diamond/TimeEv/-30lun6.mca',
                   'data/input/Diamond/TimeEv/-30lun7.mca']
    histofileMinus30 = TFile('data/input/Diamond/TimeEvHistos/histo-30.root', 'recreate')
    CentroidBoundariesMinus30 = [(1176,1250), (1172,1246), (1176,1246), (1170,1248), (1150,1242), (1148,1242), (1150,1240)]
    infilenameMinus60 = ['data/input/Diamond/TimeEv/-60lun1.mca','data/input/Diamond/TimeEv/-60lun2.mca',
                   'data/input/Diamond/TimeEv/-60lun6.mca','data/input/Diamond/TimeEv/-60lun4.mca',
                   'data/input/Diamond/TimeEv/-60lun5.mca','data/input/Diamond/TimeEv/-60lun6.mca',
                   'data/input/Diamond/TimeEv/-60lun7.mca']
    histofileMinus60 = TFile('data/input/Diamond/TimeEvHistos/histo-60.root', 'recreate')
    CentroidBoundariesMinus60 = [(1274,1308), (1274,1310), (1274,1308), (1274, 1308), (1274,1308), (1274,1308), (1278, 1308)]
    infilenameMinus90 = ['data/input/Diamond/TimeEv/90lun1.mca','data/input/Diamond/TimeEv/90lun2.mca',
                   'data/input/Diamond/TimeEv/-90lun3.mca','data/input/Diamond/TimeEv/-90lun4.mca',
                   'data/input/Diamond/TimeEv/-90lun5.mca']
    histofileMinus90 = TFile('data/input/Diamond/TimeEvHistos/histo-90.root', 'recreate')
    CentroidBoundariesMinus90 = [(1334,1372), (1328,1372), (1298, 1318), (1296, 1318), (1296,1318)]
    print('ciao')
    dict = {'+30': [infilename30, histofile30,CentroidBoundaries30], '+60': [infilename60, histofile60, CentroidBoundaries60], 
            '+90': [infilename90, histofile90, CentroidBoundaries90], '-30': [infilenameMinus30, histofileMinus30, CentroidBoundariesMinus30],
            '-60': [infilenameMinus60, histofileMinus60, CentroidBoundariesMinus60], '-90': [infilenameMinus90, histofileMinus90, CentroidBoundariesMinus90]}

    Features = [WriteHisto(dict[x][0], dict[x][1], dict[x][2]) for x in dict]
    #print(Features)
    Legend = list(dict.keys())
    #print(Legend)
    LegendName = 'Applied voltage'
    Centroids = [i[0] for i in Features]
    FWHMs = [i[1] for i in Features]
    Times = [i[2] for i in Features]
    print(FWHMs, '\n')
    print(Centroids, '\n')
    Resolutions = []
    for i,j in zip(FWHMs,Centroids):
        ResList = [i[z]/j[z] for z in range(len(i))]
        Resolutions.insert(len(Resolutions),ResList)
    
    print(Resolutions, '\n')

    #Try = [[2,2,2],[3,3,3],[4,4,4,4,4],[5,5,5,5,5,5,5],[6,6,6,6,6,6,6],[7,7,7,7,7]]
    #TitleCanvaTry = 'Try comparison'
    #PathCanvaTry = 'data/output/Diamond/TimeTry.pdf'
    #FeaturePlot(Try,Times,TitleCanvaTry, PathCanvaTry)

    TitleCanvaFWHMs = 'FWHM comparison'
    PathCanvaFWHMs = 'data/output/Diamond/TimeFWHMs.png'
    LegendCoordinates = [0.6,0.5,0.8,0.7]
    FeaturePlot(FWHMs, Times, Legend, LegendCoordinates, LegendName, TitleCanvaFWHMs, PathCanvaFWHMs)
#
    TitleCanvaCentroids = 'Centroids comparison'
    PathCanvaCentroids = 'data/output/Diamond/TimeCentroids.png'
    LegendCoordinates = [0.6,0.5,0.8,0.3]
    FeaturePlot(Centroids, Times, Legend, LegendCoordinates, LegendName, TitleCanvaCentroids, PathCanvaCentroids)
#
    TitleCanvaResolution = 'Resolution comparison'
    PathCanvaResolution = 'data/output/Diamond/TimeResolutions.png'
    FeaturePlot(Resolutions, Times, Legend, LegendCoordinates, LegendName, TitleCanvaResolution, PathCanvaResolution)


