'''
Script for plotting the coincidence curve for S1 abd SG detectors
'''

import pandas as pd
import numpy as np
import sys
sys.path.append("utils")

from StyleFormatter import SetGlobalStyle, SetObjectStyle
from math import sqrt
from ROOT import TGraphErrors, TCanvas, TFile, gPad, kAzure

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
    histo2.SetTitle("Rate curve S_1S_G")
    histo2.GetXaxis().SetTitle("#DeltaT [ns]")
    histo2.GetYaxis().SetTitle("Rate [Hz]")

    #canvas2 = TCanvas("Rate_coincidence_curve", "c" ,1280, 720)
    #canvas2.cd()
    #SetObjectStyle(histo,color=kAzure+3)
    #histo2.Draw("APZ")

    #gPad.Modified()
    #gPad.Update()

    root_file.cd()
    histo2.Write()
    #canvas2.Write()
    root_file.Close()

    ## Rate acc
    R1 = df['rate s1'].mean()
    R2 = df['rate sg'].mean()
    sigma=1e-07
    Ra=sigma*R1*R2
    print(df.head(26))
    print('rate s1=', R1)
    print('rate sg=', R2)
    print('rate accidentali=', Ra)





#__________________________________________

if __name__ == '__main__':
        
    input_path = 'data/input/coinS1SG.csv'
    coinccurve(input_path)


