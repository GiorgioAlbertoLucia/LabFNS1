import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TLegend, gStyle 
from ReadMCA import DictHistos

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.14, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.11, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

if __name__ == "__main__":

    infilename = 'data/input/Diamond/Stronzio/stronzio.mca'
    histofile = TFile('data/input/Diamond/Stronzio/StrontiumHisto.root', 'recreate')

    dict = {'Stronzio': infilename}
    DictHistos(dict, histofile, 4)


    #comparison between data taken with different gain
    #GainLegend = TLegend(0.6,0.6,0.8,0.8)
    #GainLegend.SetHeader('Amplifier gain','C')
    #GainLegend.AddEntry(dict['Cesium gain 200'][1],'200','lf')
    #GainLegend.AddEntry(dict['Cesium gain 1000'][1],'1000','lf')
    #GainLegend.SetTextFont(42)
    #GainLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    #GainLegend.SetFillStyle(0)
    #Gainboundaries = [300.,0.,3700.,1.1]
    #GainCanva = 'Gain Comparison;Energy [KeV];Counts'
    #HistoComparison(dict['Cesium gain 1000'][1], dict['Cesium gain 200'][1], GainLegend, GainCanva, Gainboundaries, 'data/output/Diamond/GainComp.pdf')
