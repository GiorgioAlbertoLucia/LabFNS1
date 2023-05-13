'''
Script for plotting the counts vs HV to decide the working point of the scintillators
CSV should have 1st column = HV, 2nd column = counts, 3rd column = HV error
Counts distribution is considered to be poissonian -> counts_err = sqrt(counts)
'''

import pandas as pd
import numpy as np
import sys
sys.path.append("utils")

from StyleFormatter import SetGlobalStyle, SetObjectStyle
from math import sqrt
from ROOT import TGraphErrors, TCanvas, TFile, gPad, kAzure

SetGlobalStyle(padleftmargin=0.19, padbottommargin=0.19, padtopmargin=0.1, titleoffsety=1.6, titleoffsetx=1.2, titleoffset= 0.7, opttitle=1)

def scintEff(input_path, root_file, scint_name):

    df = pd.read_csv(input_path)
    df['HV err'] = df['HV[V*1000]']*0.008 + 0.002
    df['Counts err']=np.sqrt(df['Counts'])

    df['HV[V*1000]'] = df['HV[V*1000]'] * 1000
    df['HV err'] = df['HV err'] * 1000

    df['Rate'] = df['Counts'] / 300
    df['Rate err'] = df['Counts err'] / 300

    histo = TGraphErrors(len(df),np.asarray(df['HV[V*1000]'],'d'),np.asarray(df['Counts'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['Counts err'],'d'))
    histo.SetTitle(f"{scint_name} Counts")
    histo.GetXaxis().SetTitle("HV [V]")
    histo.GetYaxis().SetTitle("logN")

    histo2 = TGraphErrors(len(df),np.asarray(df['HV[V*1000]'],'d'),np.asarray(df['Rate'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['Rate err'],'d'))
    histo2.SetTitle(f"{scint_name} Rate")
    histo2.GetXaxis().SetTitle("HV [V]")
    histo2.GetYaxis().SetTitle("Rate [Hz]")

    canvas = TCanvas(scint_name, "c" ,1280, 720)
    canvas.cd()
    canvas.SetLogy()
    SetObjectStyle(histo,color=kAzure+3)
    histo.Draw("APZL")

    canvas2 = TCanvas(f'{scint_name}_rate', "c" ,1280, 720)
    canvas2.cd()
    SetObjectStyle(histo2,color=kAzure+3)
    histo2.Draw("APZL")

    gPad.Modified()
    gPad.Update()

    root_file.cd()
    canvas.Write()
    canvas2.Write()




if __name__ == '__main__':
    
    outfilePath = 'data/output/HVwork.root'
    root_file = TFile(outfilePath, 'recreate')

    infilePaths = ['data/input/HVworkS1.csv',
                   'data/input/HVworkSG.csv',
                   'data/input/HVworkS2.csv',
                   'data/input/HVworkS3.csv']
    scintNames = ['S1', 'SG', 'S2', 'S3']

    for input_path, scint_name in zip(infilePaths, scintNames):
        scintEff(input_path, root_file, scint_name)


