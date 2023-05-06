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

infilePath = "data/input/TestWorkingPointEff.csv"

SetGlobalStyle(padleftmargin=0.09, padbottommargin=0.11, padtopmargin=0.1, titleoffsety=0.8, titleoffsetx=0.8, titleoffset= 0.7, opttitle=1)

df=pd.read_csv(infilePath)
df['Counts err']=np.sqrt(df[[df.columns[0]]])
canvas = TCanvas("c","c",1280,720)
canvas.cd()
canvas.SetLogy()

histo = TGraphErrors(len(df),np.asarray(df[df.columns[0]],'d'),np.asarray(df[df.columns[1]],'d'),
                     np.asarray(df[df.columns[2]],'d'),np.asarray(df[df.columns[3]],'d'))
histo.SetTitle("S1 Counts")
histo.GetXaxis().SetTitle("HV")
histo.GetYaxis().SetTitle("Counts")

SetObjectStyle(histo,color=kAzure+3)
histo.Draw("APZ")

gPad.Modified()
gPad.Update()
input('Press enter to continue')
