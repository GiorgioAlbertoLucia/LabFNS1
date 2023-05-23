import pandas as pd
import numpy as np
import sys 

from ROOT import TH2D, gStyle, TFile, TH1D, TCanvas, TGraph, TF1, TLegend, TLatex
import uproot

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=0.15, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.5, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)



# Data visualization

def fitHist(inFilePath, histName, formula, outFile):
    '''
    Load an histogram from a root file, fit the distribution with given formula and save fit on canvas to a different root file

    Parameters
    ----------

    '''

    inFile = TFile(inFilePath)
    hist = inFile.Get(histName)
    hist.SetDirectory(0)
    inFile.Close()

    hist.Rebin(2)
    hist.Scale(1./hist.Integral())
    hist.SetLineColor(413)
    hist.SetFillColor(413)
    #for i in range(hist.GetNbinsX()):   hist.SetBinError(i+1, np.sqrt(hist.GetBinContent(i+1)))

    fitFunc = TF1('fitFunc', formula, 266, 1600)
    fitFunc.SetParameters(3170, 477, 65, 6850, 750, 50, 200, 580, 100)
    fitFunc.FixParameter(7, 580)
    fitFunc.SetLineColor(2)
    hist.Fit(fitFunc, 'eb')
    print('Chi2 = ', fitFunc.GetChisquare())
    print('NDF = ', fitFunc.GetNDF())
    print('p-value = ', fitFunc.GetProb())

    landau1 = TF1('landau1', 'landau', hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    landau1.SetParameters(fitFunc.GetParameter(0), fitFunc.GetParameter(1), fitFunc.GetParameter(2))
    landau1.SetLineColor(797)
    landau2 = TF1('landau2', 'landau', hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    landau2.SetParameters(fitFunc.GetParameter(3), fitFunc.GetParameter(4), fitFunc.GetParameter(5))
    landau2.SetLineColor(863)
    #powerLaw = TF1('powerLaw', '[0]+[1]*x*x', hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    #powerLaw.SetParameters(fitFunc.GetParameter(6), fitFunc.GetParameter(7))
    #powerLaw.SetLineColor(413)
    #gaus = TF1('gaus', 'gaus', hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    #gaus.SetParameters(fitFunc.GetParameter(6), fitFunc.GetParameter(7), fitFunc.GetParameter(8))
    #gaus.SetLineColor(413)

    canvas = TCanvas('fit', 'fit')
    canvas.DrawFrame(200, 0, 1700, 0.006, 'SG energy spectrum; Energy (chn); Normalized counts (a.u.)')
    

    lines = ['Deposited energy in SG', 'Acquisition time: 236985 s']
    linePos = [[0.535, 0.64], [0.535, 0.58], [0.535, 0.52]] # xmin, ymin
    latexLines = []
    for line, linePosition in zip(lines, linePos):
        text = TLatex(linePosition[0], linePosition[1], line)
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.6)
        text.SetTextFont(42)
        latexLines.append(text)
    for line in latexLines: line.Draw()

    leg = TLegend(0.53, 0.69, 0.85, 0.8)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    leg.AddEntry(hist, 'ADC SG signal', 'lf')
    leg.AddEntry(fitFunc, 'fit function = landau1 + landau2', 'lf')
    leg.AddEntry(landau1, 'landau1: Landau fit (first peak)', 'lf')
    leg.AddEntry(landau2, 'landau2: Landau fit (second peak)', 'lf')
 

    hist.Draw('hist same')
    landau1.Draw('same')
    landau2.Draw('same')
    #powerLaw.Draw('same')
    #gaus.Draw('same')
    leg.Draw('same')

    outFile.cd()
    canvas.Write()
    canvas.SaveAs('data/output/fit.pdf')

    return hist






if __name__ == '__main__':

    rootFilePath = 'data/output/fits.root'
    rootFile = TFile(rootFilePath, 'recreate')

    formula = 'landau(0) + landau(3)'# + gaus(6)'
    #formula = 'landau(0) + gaus(3)'
    inFilePath = 'data/output/S1SG_peakComparison.root'
    histName = 'SG'

    hist = fitHist(inFilePath, histName, formula, rootFile)

    rootFile.Close()


