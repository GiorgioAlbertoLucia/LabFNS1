import pandas as pd
import numpy as np
import sys 

from ROOT import TH2D, gStyle, TFile, TH1D, TCanvas, TGraph, TF1
import uproot


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

    #hist.Rebin()
    for i in range(hist.GetNbinsX()):   hist.SetBinError(i+1, np.sqrt(hist.GetBinContent(i+1)))

    fitFunc = TF1('fitFunc', formula, 266, 1600)
    fitFunc.SetParameters(0, 300, 90, 0, 450, 120)
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
    #powerLaw = TF1('powerLaw', '[0]+x*[1]+exp([2]*x)', hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    #powerLaw.SetParameters(fitFunc.GetParameter(6), fitFunc.GetParameter(7), fitFunc.GetParameter(8))
    #powerLaw.SetLineColor(413)
    #gaus = TF1('gaus', 'gaus', hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    #gaus.SetParameters(fitFunc.GetParameter(6), fitFunc.GetParameter(7), fitFunc.GetParameter(8))
    #gaus.SetLineColor(413)

    canvas = TCanvas('fit', 'fit')
    hist.Draw('hist e0 same')
    landau1.Draw('same')
    landau2.Draw('same')
    #powerLaw.Draw('same')
    #gaus.Draw('same')


    outFile.cd()
    canvas.Write()

    return hist






if __name__ == '__main__':

    rootFilePath = 'data/output/fits.root'
    rootFile = TFile(rootFilePath, 'recreate')

    formula = 'landau(0) + landau(3)'# + [6]+x*[7]+exp([8]*x)'# + gaus(6)'
    #formula = 'landau(0) + gaus(3)'
    inFilePath = 'data/output/S1SG_peakComparison.root'
    histName = 'SG'

    hist = fitHist(inFilePath, histName, formula, rootFile)

    rootFile.Close()


