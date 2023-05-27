import pandas as pd
import numpy as np
import uproot
import math
from ROOT import TF1,TAxis, TH1D,TH2D, TCanvas, kAzure,kBlue, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFitResultPtr, TFile,TGraphErrors,gPad

def diamondsCal():

    cen=[1487.12, 1711.49,1812.38] 
    cenerr=[11.1011,4.3000, 7.7177]
    for x in cenerr:    x = x/2.235
    energy=[4.78783441477, 5.486,5.805]
    energyerr = np.zeros(3)
    
    
    graphCal=TGraphErrors(3,np.asarray(energy,'d'), np.asarray(cen,'d'),
                     energyerr, np.asarray(cenerr,'d'))# il d serve per dire il tipo delle liste per dire che tipo sono
    graphCal.Fit('pol1')

    file = TFile('data/output/Diamond/Diamond_calibration.root', 'recreate')
    graphCal.Write()
    
def ch_to_en_conversion(ch):
    return (ch + 43.35) / 319.8

def en_to_ch_conversion(en):
    return (-43.35 + en * 319.8)

def maxElecEnergyCompton(E0):
    m0 = 0.511  # electron mass in MeV
    return 2*E0**2/(m0)/(1 + 2*E0/m0)

if __name__ == '__main__':

    #diamondsCal()

    ch_label = ['Cs_int-conv_Kpeak', 'Cs_int-conv_Lpeak']
    ch_values = [1010/5, 1061/5]

    for label, value in zip(ch_label, ch_values):
        print(f'{label}: {ch_to_en_conversion(value)} MeV')

    # Compton edge Na22
    photonEn1 = 1.275 # MeV
    photonEn2 = 0.511 # MeV
    print('Compton channel')
    print(f'photon energy: {photonEn1} MeV, electron energy: {maxElecEnergyCompton(photonEn1)} MeV, channel: {en_to_ch_conversion(maxElecEnergyCompton(photonEn1))*5}')
    print(f'photon energy: {photonEn2} MeV, electron energy: {maxElecEnergyCompton(photonEn2)} MeV, channel: {en_to_ch_conversion(maxElecEnergyCompton(photonEn2))*5}')

    