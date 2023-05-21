import pandas as pd
import numpy as np
import uproot
import sys
sys.path.append('Python/utils')

from ROOT import TH1D, TCanvas, kAzure, kOrange

from StyleFormatter import SetGlobalStyle, SetObjectStyle

#gROOT.SetBatch()

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

Tree=uproot.open("data/input/DataFullRun.root")["fTreeData"]

##########
#   S1   #
##########

Df=Tree.arrays(library='pd')

Df=Df[["Module1_0","Module2_0"]]

c = TCanvas("NotInhibited","NotInhibited",1000,1000)
c.DrawFrame(0,0,7.e+4,700,"")

hNotInhibited = TH1D("NotInhibited","NotInhibited",1000,0,7.e+4)

hNotInhibited.FillN(len(Df["Module1_0"]),np.asarray(Df["Module1_0"],'d'),np.asarray([1]*len(Df["Module1_0"]),'d'))
SetObjectStyle(hNotInhibited,color=kAzure+3,fillalpha=0.5,linewidth=1)
hNotInhibited.Draw("same")

hInhibited = TH1D("Inhibited","Inhibited",1000,0,7.e+4)

hInhibited.FillN(len(Df["Module2_0"]),np.asarray(Df["Module2_0"],'d'),np.asarray([1]*len(Df["Module2_0"]),'d'))
SetObjectStyle(hInhibited,color=kOrange-3,fillalpha=0.5,linewidth=1)
hInhibited.Draw("same")


c.SaveAs("/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/Python/src/DeadTime.pdf")