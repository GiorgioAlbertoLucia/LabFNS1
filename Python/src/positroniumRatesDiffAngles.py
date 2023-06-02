import numpy as np
import pandas as pd

from ROOT import TGraphErrors, TGraph, TCanvas, TFile, TH1D, gStyle, TLegend, TF1
from ROOT import kOrange, kAzure, kGreen, kRed, kMagenta, kViolet, kBlue, kYellow

colorList = [kOrange-3, kMagenta-4, kAzure-3, kGreen-3, kRed-4, kViolet-6, kBlue-4, kYellow-7]

def readMCAoutput(infile, ROI=[0, -1]):
    '''
    Reads a .mca file and returns the rate and a histogram of data

    Parameters
    ----------
        infile (str): path to the input file
        ROI (list[int]): edges (in chn) between which a region of interest (ROI) is defined. The rate is calculated with counts in the ROI

    Returns
    -------
        rate (float): rate of events
        rate_err (float): error on the rate of events
        hist (TH1D): histogram of data
    '''

    hist = TH1D('hist', 'hist', 1024, 0, 1024)
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
        hist.SetBinError(i, np.sqrt(x))
    for x in data[ROI[0]:ROI[1]]:   tot_counts += x

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
    canvas.DrawFrame(0, 0, 1024, 1200)

    leg = TLegend(0.50, 0.41, 0.85, 0.79)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.9)
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

    return graph

def rateGraphPDF(graph, outFile, canvasPath):
    '''
    Fit the rate TGraph and draw it on canvas. The canvas will be saved on a .root file as well as on a .pdf
    '''

    canvas = TCanvas('Rates-Angle-Canvas', 'Rates of #gamma-#gamma coincidences; Angle (deg); Rate (Hz)')
    canvas.DrawFrame(0, 0, 1024, 600, 'Rates of #gamma-#gamma coincidences; Angle (deg); Rate (Hz)')


    graph.SetMarkerStyle(8)
    graph.SetMarkerSize(.8)
    graph.SetMarkerColor(kOrange-3)

    canvas.cd()
    graph.Draw('ap')
    canvas.SaveAs(canvasPath)

    outFile.cd()
    canvas.Write()

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
    angles = [32, 28, 24, 20, 16, 12, 8, 4, 0, -4, -8, -12, -16, -20, -24, -28, -32]
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
                    'data/input/Gamma/PositroniumDecays/pos560s-29deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos10min-33deg.mca',
                    ]

    rates = []
    rate_errs = []
    hists = []
    ROIs = [[506, 528], [507, 528], [503, 539], [500, 536], [499, 533], [485, 529], [493, 531], [491, 531],
            [491, 526], [491, 525], [493, 529], [493, 533], [491, 530], [493, 530], [500, 527], 
            [501, 531], [501, 524]]
    labels = ['Angle: 32°, Acq. time: 10 min',
              'Angle: 28°, Acq. time: 9 min',
              'Angle: 24°, Acq. time: 8 min',
              'Angle: 20°, Acq. time: 7 min',
              'Angle: 16°, Acq. time: 6 min',
              'Angle: 12°, Acq. time: 5 min',
              'Angle: 8°, Acq. time: 4 min',
              'Angle: 4°, Acq. time: 3 min',
              'Angle: 0°, Acq. time: 2 min',
              'Angle: -4°, Acq. time: 3 min',
              'Angle: -8°, Acq. time: 4 min',
              'Angle: -12°, Acq. time: 5 min',
              'Angle: -16°, Acq. time: 6 min',
              'Angle: -20°, Acq. time: 7 min',
              'Angle: -24°, Acq. time: 8 min',
              'Angle: -28°, Acq. time: 9 min',
              'Angle: -32°, Acq. time: 10 min',
             ]
    
    for angle, infile, ROI in zip(angles, inputFiles, ROIs):
        hist = TH1D()
        rate, rate_err, hist = readMCAoutput(infile, ROI)
        hist.SetName(f'TACcounts_angle_{angle}')
        hist.SetTitle(f'TAC counts, angle = {angle} #circ; Energy (chn); Counts (a. u.)')
        
        rates.append(rate)
        rate_errs.append(rate_err)
        hists.append(hist)
        del hist

    outfile = TFile('data/output/Gamma/positroniumRatesDiffAngles.root', 'recreate')
    for hist in hists:  hist.Write()
    multihist(hists, labels, outfile, 'TAC counts; Time (chn); Counts (a. u.)')   # tac hists
    rate_graph = rateGraph(angles, rates, rate_errs, outfile)
    rateGraphPDF(rate_graph, outfile, 'data/output/Figures/GammaCoincidence/rateGraph.pdf')

    # data from caen scaler
    scalerDf = pd.read_csv(r'data/input/Gamma/positroniumCoincidence.csv')
    scalerRateGraph(scalerDf, outfile)

    outfile.Close()
    


    
