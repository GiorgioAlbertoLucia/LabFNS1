import numpy as np
import pandas as pd

from ROOT import TGraphErrors, TGraph, TCanvas, TFile, TH1D, gStyle, TLegend
from ROOT import kOrange, kAzure, kGreen, kRed, kMagenta, kViolet, kBlue, kYellow

colorList = [kOrange-3, kMagenta-4, kAzure-3, kGreen-3, kRed-4, kViolet-6, kBlue-4, kYellow-7]

def readMCAoutput(infile):
    '''
    Reads a .mca file and returns the rate and a histogram of data

    Parameters
    ----------
        infile (str): path to the input file

    Returns
    -------
        rate (float): rate of events
        rate_err (float): error on the rate of events
        hist (TH1D): histogram of data
    '''

    hist = TH1D('hist', 'hist', 2048, 0, 2048)
    data = []
    live_time = 0

    with open(infile, 'r', errors='ignore') as file:

        for line in file:
            if line.startswith('LIVE_TIME'):
                #live_time = line
                live_time = float(line.split('-')[-1].strip())
                break

        lines = file.readlines()[1:-1]
        start_index = lines.index('<<DATA>>\n') + 1
        end_index = lines.index('<<END>>\n')

        for line in lines[start_index:end_index]:
                value = int(line.strip()) 
                data.append(value) 

    tot_counts = 0
    for i, x in enumerate(data):  
        hist.Fill(i, x)
        tot_counts += x

    rate = tot_counts/live_time
    rate_err = np.sqrt(tot_counts)/live_time
    return rate, rate_err, hist

def multihist(hists, labels, outFile, canvasTitle=''):
    '''
    Draw multiple histograms on canvas and save them to a root file

    Parameters
    ----------
        hists (list[TH1D]): list of histograms to draw
        labels (list[str]): list of histogram labels
        outFile (TFile): file to draw the histograms to
        canvasTitle (str, optional): title of the canvas 

    '''

    canvas = TCanvas('c', canvasTitle, 1500, 1500)

    leg = TLegend(0.50, 0.71, 0.85, 0.59)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)

    for i, hist in enumerate(hists):
        #hist.SetFillColor(colorList[i])
        hist.SetLineColor(colorList[i%len(colorList)])
        hist.Draw('hist same')
        leg.AddEntry(hist, labels[i], 'lf')

    leg.Draw()
    outFile.cd()
    canvas.Write()

def rateGraph(x, y, ey, outFile):

    entries = len(x)
    ex = np.ones((entries,))

    graph = TGraphErrors(entries, np.asarray(x, 'd'), np.asarray(y, 'd'), ex, np.asarray(ey, 'd'))
    graph.SetDrawOption('ap')
    graph.SetName('Rates-Angle')
    graph.SetTitle('Rates of #gamma-#gamma coincidences; Angle (deg); Rate (Hz)')
    graph.SetMarkerColor(kAzure-4)

    outFile.cd()
    graph.Write()

def scalerRateGraph(scalerDf, outFile):

    scalerDf['rateA'] = scalerDf['countsA'] / scalerDf['acquisitionTime (s)']
    scalerDf['rateB'] = scalerDf['countsB'] / scalerDf['acquisitionTime (s)']
    scalerDf['rateA_err'] = np.sqrt(scalerDf['countsA']) / scalerDf['acquisitionTime (s)']
    scalerDf['rateB_err'] = np.sqrt(scalerDf['countsB']) / scalerDf['acquisitionTime (s)']

    canvas = TCanvas('scalerRate-Angle', 'Rates for scintillators A and B; Angle (deg); Rate (Hz)')
    canvas.DrawFrame(0, 0, 1024, 1000)

    entries = len(scalerDf)
    ex = np.ones((entries,))

    graphA = TGraphErrors(entries, np.asarray(scalerDf['angle (deg)'], 'd'), np.asarray(scalerDf['rateA'], 'd'), 
                          ex, np.asarray(scalerDf['rateA_err'], 'd'))
    graphA.SetDrawOption('ap')
    graphA.SetName('Rates-Angle-scalerA')
    graphA.SetTitle('Rates of #gamma-#gamma coincidences, scint. A; Angle (deg); Rate (Hz)')
    graphA.SetMarkerColor(kAzure-4)

    graphB = TGraphErrors(entries, np.asarray(scalerDf['angle (deg)'], 'd'), np.asarray(scalerDf['rateB'], 'd'), 
                          ex, np.asarray(scalerDf['rateB_err'], 'd'))
    graphB.SetDrawOption('ap')
    graphB.SetName('Rates-Angle-scalerB')
    graphB.SetTitle('Rates of #gamma-#gamma coincidences, scint. B; Angle (deg); Rate (Hz)')
    graphB.SetMarkerColor(kOrange-3)

    leg = TLegend(0.50, 0.73, 0.85, 0.81)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    leg.AddEntry(graphA, 'Rates of coincidence for scintillator A', 'lf')
    leg.AddEntry(graphB, 'Rates of coincidence for scintillator B', 'lf')

    canvas.cd()
    canvas.SetTitle('Rates for scintillators A and B; Angle (deg); Rate (Hz)')
    graphA.Draw('ap')
    graphB.Draw('ap')
    leg.Draw('same')


    outFile.cd()
    canvas.Write()
    canvas.SaveSource('Python/src/RatesPositroniumABcanvas.C')
    graphA.Write()
    graphB.Write()

if __name__ == '__main__':

    ### data from mca
    angles = [31, 27, 23, 19, 15, 11, 7, 3, -1, -5, -9, -13, -17, -21, -25]
    inputFiles =   ['data/input/Gamma/PositroniumDecays/pos10min31deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos9min27deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos8min23deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos7min19deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos6min15deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos5min11deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos4min7deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos3min3deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos2min-1deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos3min-5deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos4min-9deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos5min-13deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos6min-17deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos7min-21deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos8min-25deg.mca',
                    #'data/input/Gamma/PositroniumDecays/pos9min-29deg.mca',
                    #'data/input/Gamma/PositroniumDecays/pos10min-33deg.mca',
                    ]

    rates = []
    rate_errs = []
    hists = []
    labels = ['Angle: 31#circ, Acq. time: 10 min',
              'Angle: 27#circ, Acq. time: 9 min',
              'Angle: 23#circ, Acq. time: 8 min',
              'Angle: 19#circ, Acq. time: 7 min',
              'Angle: 15#circ, Acq. time: 6 min',
              'Angle: 11#circ, Acq. time: 5 min',
              'Angle: 7#circ, Acq. time: 4 min',
              'Angle: 3#circ, Acq. time: 3 min',
              'Angle: -1#circ, Acq. time: 2 min',
              'Angle: -5#circ, Acq. time: 3 min',
              'Angle: -9#circ, Acq. time: 4 min',
              'Angle: -13#circ, Acq. time: 5 min',
              'Angle: -17#circ, Acq. time: 6 min',
              'Angle: -21#circ, Acq. time: 7 min',
              'Angle: -25#circ, Acq. time: 8 min',
              #'Angle: -29#circ, Acq. time: 9 min',
              #'Angle: -33#circ, Acq. time: 10 min',
             ]
    
    for angle, infile in zip(angles, inputFiles):
        hist = TH1D()
        rate, rate_err, hist = readMCAoutput(infile)
        
        rates.append(rate)
        rate_errs.append(rate_err)
        hists.append(hist)
        del hist

    outfile = TFile('data/output/Gamma/positroniumRatesDiffAngles.root', 'recreate')
    multihist(hists, labels, outfile, 'TAC counts; Energy (chn); Counts (a. u.)')   # tac hists
    rateGraph(angles, rates, rate_errs, outfile)

    # data from caen scaler
    scalerDf = pd.read_csv(r'data/input/Gamma/positroniumCoincidence.csv')
    scalerRateGraph(scalerDf, outfile)

    outfile.Close()
    


    
