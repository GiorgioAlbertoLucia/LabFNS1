'''
Script for plotting the coincidence curve for S1 abd SG detectors
'''

import pandas as pd
import numpy as np
import sys
sys.path.append("Python/utils")

from StyleFormatter import SetGlobalStyle, SetObjectStyle
from math import sqrt
from ROOT import TGraphErrors, TCanvas, TFile, gPad, kAzure, TF1, TMath, gStyle, TFitResult, TFitResultPtr

SetGlobalStyle(padleftmargin=0.19, padbottommargin=0.19, padtopmargin=0.1, titleoffsety=1.6, titleoffsetx=1.2, titleoffset= 0.7, opttitle=1)

def def_delay_err(df):
    err = 0
    if df['delay'] < 8:       err = sqrt(2)*0.1
    elif df['delay'] < 71:    err = sqrt(0.1**2 + 0.2**2)
    else:               err = sqrt(2)*0.2     
    return err


def coinccurve(input_path):
    '''
    Function to create a TGraphErrors coincidence S1SG counts vs relative delay.

    Parameters
    ----------
        input_path (str): path to the input data
    '''

    outfilePath = 'data/output/coinS1SG.root'
    root_file = TFile(outfilePath, 'recreate')

    df = pd.read_csv(input_path)
    df.sort_values("delay", axis=0, ascending=True,inplace=True, na_position='first')
    df['delay err'] = df.apply(lambda df: def_delay_err(df), axis=1)
    df['count coin err'] = np.sqrt(df['count coin'])
    df['rate'] = df['count coin'] / df['dT[s]']
    df['rate err'] = df['count coin err'] / df['dT[s]']
    
    df['count s1 err'] = np.sqrt(df['count s1'])
    df['rate s1'] = df['count s1'] / df['dT[s]']
    df['rate s1 err'] = df['count s1 err'] / df['dT[s]']

    df['count sg err'] = np.sqrt(df['count sg'])
    df['rate sg'] = df['count sg'] / (df['dT[s]'])
    df['rate sg err'] = df['count sg err'] / (df['dT[s]'])


    ## Counts graph
    histo = TGraphErrors(len(df),np.asarray(df['delay'],'d'),np.asarray(df['count coin'],'d'),
                     np.asarray(df['delay err'],'d'),np.asarray(df['count coin err'],'d'))
    histo.SetTitle("Coincidence curve S_1S_G")
    histo.GetXaxis().SetTitle("#Delta T")
    histo.GetYaxis().SetTitle("Counts")

    #canvas = TCanvas("coincidence_curve", "c" ,1280, 720)
    #canvas.cd()
    #SetObjectStyle(histo,color=kAzure+3)
    #histo.Draw("APZ")

    #gPad.Modified()
    #gPad.Update()

    root_file.cd()
    #canvas.Write()
    histo.Write()

    ## Rate graph
    histo2 = TGraphErrors(len(df),np.asarray(df['delay'],'d'),np.asarray(df['rate'],'d'),
                     np.asarray(df['delay err'],'d'),np.asarray(df['rate err'],'d'))
    histo2.SetTitle("Rate curve S_{1}S_{G}")
    histo2.GetXaxis().SetTitle("#DeltaT [ns]")
    histo2.GetYaxis().SetTitle("Rate [Hz]")

    root_file.cd()
    histo2.Write()

    # Linear fit on the plateau for fit parameters optimization

    constant = TF1("f1", "[0]", 31, 91)

    FitLowerBoundary = -5
    FitUpperBoundary = 120
    histo2.SetTitle("Fit # p_{0} + p_{1}(1/[1+exp(-#frac{x-p_{2}}{p_{3}})]}) + p_{4}(1/[1+exp(-#frac{x-p_{5}}{p_{6}})]})")
    gStyle.SetTitleSize(3)
    sigmoidsum = TF1("f1","[0] + [1]*((1/(1+TMath::Exp(-(x-[2])/[3])))) + [4]*((1/(1+TMath::Exp(-(x-[5])/[6]))))", FitLowerBoundary, FitUpperBoundary)
    #sigmoidsum.SetParameters(1, constant.GetParameter(0))
    histo2.Fit(sigmoidsum,"RM+","", FitLowerBoundary, FitUpperBoundary)
    Chisquaresum = sigmoidsum.GetChisquare()
    NDegFreedom = sigmoidsum.GetNDF()
    FitProb = sigmoidsum.GetProb()
    FWHMleft = sigmoidsum.GetX(sigmoidsum.GetMaximum()/2, FitLowerBoundary, sigmoidsum.GetMaximumX())
    FWHMright = sigmoidsum.GetX(sigmoidsum.GetMaximum()/2, sigmoidsum.GetMaximumX(), FitUpperBoundary)
    print('Chi Square: ', Chisquaresum, ' Degrees of freedom: ', NDegFreedom, ' Fit Probability: ', FitProb, ' Resolution: ', FWHMright - FWHMleft, 'ns')


    root_file.cd()
    histo2.Write()

    #histo2.SetTitle("Rate curve S_1S_G")
    #singlesigmoid = TF1("f1","[0] + [1]*( (1 / ( 1 + TMath::Exp( - (x - [2]) / [3]) ) ) + (1 / (1 + TMath::Exp(- (x - [4]) / [5]))))", -5, 120)
    #histo2.Fit(singlesigmoid,"RM","", -5, 120)
    #
    #root_file.cd()
    #histo2.Write()
    #
    #histo2.SetTitle("Rate curve S_1S_G")
    #abssigmoid = TF1("f1","[0] + [1]*( (1 / ( 1 + TMath::Exp( TMath::Abs( (x - [2]) / [3]) ) ) ) )", -5, 120)
    #histo2.Fit(abssigmoid,"RM","", -5, 120)
    #
    #root_file.cd()
    #histo2.Write()
    #
    #canvas2 = TCanvas("Rate_coincidence_curve", "c" ,1280, 720)
    #canvas2.cd()
    #SetObjectStyle(histo,color=kAzure+3)
    #histo2.Draw("APZ")

    #gPad.Modified()
    #gPad.Update()

    #root_file.cd()
    #histo2.Write()
    #canvas2.Write()
    root_file.Close()

    ## Rate acc
    R1 = df['rate s1'].mean()
    R2 = df['rate sg'].mean()
    sigma=1e-07
    Ra=sigma*R1*R2
    #print(df.head(26))
    print('rate s1=', R1)
    print('rate sg=', R2)
    print('rate accidentali=', Ra)





#__________________________________________

if __name__ == '__main__':
        
    input_path = 'data/input/coinS1SG.csv'
    coinccurve(input_path)


