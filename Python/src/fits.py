import pandas as pd
import numpy as np
import sys 
sys.path.append('Python/utils')
from ROOT import TH2D, gStyle, TFile, TH1D, TCanvas, TGraph,TLegend, TF1,TLatex, Math,kAzure, kGreen
import uproot

from StyleFormatter import SetGlobalStyle, SetObjectStyle

SetGlobalStyle(padleftmargin=0.13, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.3, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

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

    fitFunc = TF1('fitFunc', formula, 150, 1600)
    formulas=formula.split('+')
    formulas=[x.strip() for x in formulas]
    formulas=[x[:-3] for x in formulas]
    print(formulas)
    if 'gaus' in formulas[0]:
        fitFunc.SetParameters(334, 320, 37, 13096, 451, 41)
    else:
        fitFunc.SetParameters(300, 300, 30, 2500, 430, 50)
        #fitFunc.SetParLimits(1, 150,350)
        #fitFunc.SetParLimits(2, 5, 30)
    fitFunc.SetLineColor(2)
    if 'gaus' in formulas[0]:
        hist.Fit(fitFunc, 'L')
    else:
        hist.Fit(fitFunc, 'RM')
    print('Chi2 = ', fitFunc.GetChisquare())
    print('NDF = ', fitFunc.GetNDF())
    print('p-value = ', fitFunc.GetProb())
    print('Critical Chi2 = ', Math.chisquared_quantile_c(0.05,fitFunc.GetNDF()))


    landau1 = TF1('landau1', formulas[0], hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
    landau1.SetParameters(fitFunc.GetParameter(0), fitFunc.GetParameter(1), fitFunc.GetParameter(2))
    landau1.SetLineColor(797)
    landau2 = TF1('landau2', formulas[1], hist.GetBinLowEdge(1), hist.GetBinLowEdge(hist.GetNbinsX()))
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

    return hist,fitFunc,landau1,landau2



def CreateImage(hist,functiontot,f1,f2, outname):

    c = TCanvas("c","c",1500,1500)
    hFrame = c.DrawFrame(0,0,2048,2500,"S1 ADC distribution;Channel;Counts")
    SetObjectStyle(hist,linecolor=kAzure+3,fillalpha=0.4,fillcolor=kAzure+4,markersize=0.5, linewidth=1)
    hist.Draw("hist,same")
    functiontot.SetNpx(1000)
    f1.SetNpx(1000)
    f2.SetNpx(1000)
    SetObjectStyle(f2,linecolor=kGreen+3)
    f1.Draw("same")
    f2.Draw("same")
    functiontot.Draw("same")

    text =TLatex(0.45, 0.77,"S1 Scintillator + PMXP2020")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()

    text3 = TLatex(0.45, 0.50,"Acquisition time: 236985 s")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()
    text4 =TLatex(0.45, 0.45,"Discriminator threshold value: (#font[122]{-}39.6 #pm 0.5) mV")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw()
    
    leg = TLegend(0.435, 0.73, 0.735, 0.53)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("S1 Normalised counts")
    leg.AddEntry(hist, 'S1 distribution', 'lf')
    leg.AddEntry(functiontot, 'Total fitting funtcion', 'l')
    leg.AddEntry(f1, 'Gaussian contribution', 'l')
    leg.AddEntry(f2, 'Landau contribution', 'l')
    leg.Draw("same")

    c.SaveAs(outname)


if __name__ == '__main__':

    rootFilePath = 'data/output/fits.root'
    rootFile = TFile(rootFilePath, 'recreate')

    formula = 'gaus(0) + landau(3)'# + [6]+x*[7]+exp([8]*x)'# + gaus(6)'
    #formula = 'landau(0) + gaus(3)'
    inFilePath = 'data/output/S1SG_peakComparison.root'
    histName = 'S1'

    hist,functiontot,f1,f2 = fitHist(inFilePath, histName, formula, rootFile)

    CreateImage(hist,functiontot,f1,f2,'data/output/Figures/S1Fits.pdf')

    formula = 'landau(0) + landau(3)'

    hist,functiontot,f1,f2 = fitHist(inFilePath, histName, formula, rootFile)

    CreateImage(hist,functiontot,f1,f2,'data/output/Figures/S1Fits2Landau.pdf')

    rootFile.Close()


