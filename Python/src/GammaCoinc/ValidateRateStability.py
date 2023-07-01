from ROOT import TH1D, TCanvas
import pandas as pd
import numpy as np

df = pd.read_csv('data/input/Gamma/positroniumCoincidence.csv')

histoA = TH1D("histoA","histoA",100,-32,32)
histoB = TH1D("histoB","histoB",100,-32,32)

rateA = np.asarray(df['countsA'],'d')
rateB = np.asarray(df['countsB'],'d')
time = np.asarray(df['acquisitionTime (s)'],'d')
angle = np.asarray(df['angle (deg)'],'d')
rateA/=time
rateB/=time

canvas = TCanvas("c","c",1080,720)

histoA.FillN(len(rateA),angle,rateA)
histoB.FillN(len(rateB),angle,rateB)

histoA.Draw()
histoB.Draw('same')

canvas.SaveAs('data/output/Figures/GammaCoincidence.png')