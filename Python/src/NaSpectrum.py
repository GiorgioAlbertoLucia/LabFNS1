import pandas as pd
import numpy as np
import sys
#import argparse

sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, TLegend, TPad, TF1, gStyle, TPaveStats, gPad, TGraphErrors, TLatex, TFile 
from ROOT import kSpring, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure,kGray, kMagenta

#________________________
# GLOBAL PARAMETERS

# calibration values
BB = 25.63 # offset
AA = 0.68 # slope, keV^-1


#________________________


def CreateHist(infile, histName):
    '''
    Reads data from a .mca file and fills a histogram with it. Live time of the measurement is also returned.

    Parameters
    ----------
        infile (str): path to the file to read from
        histName (str): name of the histogram created
    
    Returns
    -------
        hist (TH1D): histogram filled with values from the file
        data (list[float]): data read from the file
        live_time (float): time passed during data acquisition (s)
    '''

    data = []
    live_time = 0

    with open(infile, 'r', errors='ignore') as file:#with chiude i automatico il file

        for line in file:
            if line.startswith('LIVE_TIME'):
                live_time = float(line.split('-')[-1].strip())
                break

        lines = file.readlines()[1:-1]
        start_index = lines.index('<<DATA>>\n') + 1
        end_index = lines.index('<<END>>\n')

        for line in lines[start_index:end_index]:
            value = int(line.strip())  # Convert the line to an integer
            data.append(value)  # Append the value to the list

    hist = TH1D(histName,"Hist",len(data),0,len(data))
    for i, x in enumerate(data): 
        hist.Fill(i, x)
        hist.SetBinError(i, np.sqrt(x))
    
    return hist, data, live_time

def ChannelToEnergy(chn):
    '''
    Convert channel to energy using calibration results and takng into account the gain used for that acquisition
    '''
    return (chn-BB)/AA

def HistoFromCtoE(data, histName):
    '''
    Converts data from channels to energies and fills a histogram with it

    Parameters
    ----------
        data (list[float]): data to convert
        aa, bb (float): slope and offset of the calibration line
        gain (int): gain used (calibration was done with gain = 1000)
    
    Returns
    -------
        histE (TH1D): histogram filled with data after conversion in energy
    '''

    nbin = len(data)    
    histE = TH1D(histName,"HistE",nbin,ChannelToEnergy(0),ChannelToEnergy(nbin))
    
    for i, x in enumerate(data): 
        histE.Fill(ChannelToEnergy(i)+1/(2*AA), x)   # fill center of bin to avoid filling the same bin twice (root does strange things with bin edges)
        histE.SetBinError(i, np.sqrt(x))

    return histE 

def StudyNaSpectrum2(hist, outFile, live_time):
    '''
    Performs a study of the Na spectrum (second data acquisition), creating a histogram, fitting peaks and adding legends to the output. 

    Parameters
    ----------
        hist (TH1D): histogram with Na spectrum
        outFile (TFile): output file
        live_time (float): acquisition time
    '''

    gStyle.SetOptStat(0)

    canvas = TCanvas('Na2canvas', '', 1500, 1500)
    canvas.DrawFrame(50, 0.01, 800, 120, 'Sodium spectrum; Energy [keV]; Counts [a. u.]')

    hist.SetLineColor(kOrange-3)
    hist.SetFillColorAlpha(kOrange-3, 0.4)
    hist.SetTitle('Sodium spectrum (with plastic cover); Energy [keV]; Counts [a. u.]')
    hist.Draw('hist')
    canvas.SetLogy()
    canvas.SaveAs('data/output/Diamond/NaPlastic.pdf')

    # Compton edge 341 keV
    compton1 = TF1('compton1', '[0] + [2]/(  1 + exp( (x-[1])/[3] )  )', 320, 420)
    compton1.SetParNames('y_0', 'x_0', 'a', 'b')
    compton1.SetParameters(50, 341, 150, 4)
    compton1.SetParLimits(0, 30, 70)
    compton1.SetParLimits(1, 330, 370)
    compton1.SetParLimits(2, 120, 180)
    compton1.SetParLimits(3, 0.001, 10)
    compton1.SetLineColor(kBlue-3)
    hist.Fit(compton1, 'rm', '', 300, 450)

    leg1 = TLegend(0.15, 0.5, 0.55, 0.85)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(hist, '^{22}Na Spectrum (with plastic cover)', 'lf')
    leg1.AddEntry(compton1, 'N(E) = [Bkg] + #frac{[a]}{1 + exp#left(#frac{E - [E_{C}]}{[b]}#right)}', 'lf')

    text0 = TLatex(0.55, 0.80, '#bf{Acquisition time:} '+f'{live_time:#.0f} s')
    text1 = TLatex(0.55, 0.75, '#bf{Fit results:}')
    text2 = TLatex(0.55, 0.70, f'[Bkg] = {compton1.GetParameter(0):#.1f} #pm {compton1.GetParError(0):#.1f}')
    text3 = TLatex(0.55, 0.65, '[E_{C}] = '+f'({compton1.GetParameter(1):#.1f} #pm {compton1.GetParError(1):#.1f}) keV')
    text4 = TLatex(0.55, 0.60, f'[a] = ({compton1.GetParameter(2):#.0f} #pm {compton1.GetParError(2):#.0f})')
    text5 = TLatex(0.55, 0.55, f'[b] = ({compton1.GetParameter(3):#.1f} #pm {compton1.GetParError(3):#.1f}) keV')
    text6 = TLatex(0.55, 0.50, f'#chi^2 / NDF = {compton1.GetChisquare():#.0f} / {compton1.GetNDF()}')

    canvasCompton1 = TCanvas('Na2canvasCompton1', '', 1500, 1500)

    hist.GetXaxis().SetRangeUser(200, 600)
    hist.GetYaxis().SetRangeUser(0, 500)
    hist.SetTitle('Sodium spectrum - Compton edge (511 keV); Energy (keV); Counts (a. u.)')
    hist.Draw('hist')
    compton1.Draw('same')
    leg1.Draw('same')

    for text in [text0, text1, text2, text3, text4, text5, text6]:   
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.8)
        text.SetTextFont(42)
        text.Draw()

    # Compton edge 841 keV
    compton2 = TF1('compton2', '[0] + [2]/(  1 + exp( (x-[1])/[3] )  )', 800, 900)
    compton2.SetParNames('y_0', 'x_0', 'a', 'b')
    compton2.SetParameters(1, 864, 9, 4)
    compton2.SetParLimits(0, 0, 3)
    compton2.SetParLimits(1, 800, 900)
    compton2.SetParLimits(2, 5, 15)
    compton2.SetParLimits(3, 0.001, 10)
    compton2.SetLineColor(kBlue-3)
    hist.Fit(compton2, 'lrm', '', 800, 950)

    leg2 = TLegend(0.15, 0.5, 0.55, 0.85)
    leg2.SetTextFont(42)
    leg2.SetTextSize(gStyle.GetTextSize()*0.7)
    leg2.SetFillStyle(0)
    leg2.SetBorderSize(0)
    leg2.AddEntry(hist, '^{22}Na Spectrum (with plastic cover)', 'lf')
    leg2.AddEntry(compton2, 'N(E) = [Bkg] + #frac{[a]}{1 + exp#left(#frac{E - [E_{C}]}{[b]}#right)}', 'lf')

    text0 = TLatex(0.55, 0.80, '#bf{Acquisition time:} '+f'{live_time:#.0f} s')
    text1 = TLatex(0.55, 0.75, '#bf{Fit results:}')
    text2 = TLatex(0.55, 0.70, f'[Bkg] = {compton2.GetParameter(0):#.1f} #pm {compton2.GetParError(0):#.1f}')
    text3 = TLatex(0.55, 0.65, '[E_{C}] = '+f'({compton2.GetParameter(1):#.1f} #pm {compton2.GetParError(1):#.1f}) keV')
    text4 = TLatex(0.55, 0.60, f'[a] = ({compton2.GetParameter(2):#.0f} #pm {compton2.GetParError(2):#.0f})')
    text5 = TLatex(0.55, 0.55, f'[b] = ({compton2.GetParameter(3):#.1f} #pm {compton2.GetParError(3):#.1f}) keV')
    text6 = TLatex(0.55, 0.50, f'#chi^2 / NDF = {compton2.GetChisquare():#.0f} / {compton2.GetNDF()}')

    canvasCompton2 = TCanvas('Na2canvasCompton2', '', 1500, 1500)
    
    hist.GetXaxis().SetRangeUser(700, 1200)
    hist.GetYaxis().SetRangeUser(0, 40)
    hist.SetTitle('Sodium spectrum - Compton edge (1274 keV); Energy (keV); Counts (a. u.)')
    hist.Draw('hist')
    compton2.Draw('same')
    leg2.Draw('same')

    for text in [text0, text1, text2, text3, text4, text5, text6]:   
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.8)
        text.SetTextFont(42)
        text.Draw()

    outFile.cd()
    hist.Write()
    canvas.Write()
    canvasCompton1.Write()
    canvasCompton1.SaveAs('data/output/Diamond/NaCompton1.pdf')
    canvasCompton2.Write()
    canvasCompton2.SaveAs('data/output/Diamond/NaCompton2.pdf')

if __name__ == '__main__':

    # output file initialization    

    # first sodium data acquisition (e- visible)
    infilePath = 'data/input/Gamma/Merc/SodioPiccoSomma.mca'
    histNa, dataNa, live_timeNa = CreateHist(infilePath, 'NaSpectrum')
    histNaE = HistoFromCtoE(dataNa, 'NaSpectrumE')
    histNa.Rebin(8)
    histNaE.Rebin(8)

    canvas = TCanvas('Na2canvas', '', 1500, 1500)

    gStyle.SetOptStat(0)
    histNa.SetLineColor(kAzure-3)
    histNa.SetFillColorAlpha(kAzure-3, 0.4)
    histNa.GetXaxis().SetRangeUser(0, 800)
    histNa.SetTitle('Sodium spectrum; Energy (chn); Counts (a. u.)')
    histNa.Draw('hist')
    canvas.SaveAs('data/output/Figures/GammaCoincidence/NaSpectrum.pdf')
    

    