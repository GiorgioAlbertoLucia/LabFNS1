import numpy as np
import pandas as pd

from ROOT import TGraphErrors, TGraph, TCanvas, TFile, TH1D, gStyle, TLegend, TLatex, TPaveStats, TF1, Form
from ROOT import kOrange, kAzure, kGreen, kRed, kMagenta, kViolet, kBlue, kYellow

colorList = [kOrange-3, kMagenta-4, kAzure-3, kGreen-3, kRed-4, kViolet-6, kBlue-4, kYellow-7]

def readMCAoutput(infile):
    '''
    Reads a .mca file and returns a histogram of data

    Parameters
    ----------
        infile (str): path to the input file

    Returns
    -------
        hist (TH1D): histogram of data
    '''

    hist = TH1D('hist', 'hist', 1024, 0, 1024)
    data = []

    with open(infile, 'r', errors='ignore') as file:

        lines = file.readlines()[1:-1]
        start_index = lines.index('<<DATA>>\n') + 1
        end_index = lines.index('<<END>>\n')

        for line in lines[start_index:end_index]:
                value = int(line.strip()) 
                data.append(value) 

    for i, x in enumerate(data):    
        hist.Fill(i, x)
        hist.SetBinError(i, np.sqrt(x))

    return hist

def multihist(hists, labels, outFile, canvasTitle='', canvasPath=''):
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
    canvas.DrawFrame(0, 0, 1200, 450, canvasTitle)

    leg = TLegend(0.65, 0.51, 0.88, 0.79)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.9)
    leg.SetFillStyle(0)

    text = TLatex() #acquisition time

    for i, hist in enumerate(hists):
        hist.SetLineColor(colorList[i%len(colorList)])
        hist.Draw('hist same')
        leg.AddEntry(hist, labels[i], 'lf')

    leg.Draw()
    outFile.cd()
    canvas.Write()
    canvas.SaveAs(canvasPath)

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

def calibration(x, y, ey, outFile, name='graph', title='', canvasPath=''):
    '''
    Creates a TGraphError and performs a linear fit on data. Fit parameters will be returned

    Parameters
    ----------

    Returns
    -------
        q, m (float): parameters of the fit (y = mx + q)
        eq, em (float): errors to the parameters of the fit
    '''

    entries = len(x)
    ex = np.zeros((entries,))

    graph = TGraphErrors(entries, np.asarray(x, 'd'), np.asarray(y, 'd'), ex, np.asarray(ey, 'd'))
    graph.SetDrawOption('ap')
    graph.SetName(name)
    graph.SetTitle(title)
    graph.SetMarkerStyle(8)
    graph.SetMarkerSize(.8)
    graph.SetMarkerColor(kOrange-3)

    fitFunc = TF1('fitFunc', 'pol1')
    fitFunc.SetParNames('q', 'm')
    fitFunc.SetLineColor(kAzure-3)
    graph.Fit(fitFunc)   
    
    q = fitFunc.GetParameter(0)
    eq = fitFunc.GetParError(0)
    m = fitFunc.GetParameter(1)
    em = fitFunc.GetParError(1)

    canvas = TCanvas(f'{name}_canvas', title)
    graph.Draw('ap')
    fitFunc.Draw('same')

    gStyle.SetOptStat(0)
    text1 = TLatex(0.185, 0.70, 'Fit results (Time = m * Delay + q):')
    text2 = TLatex(0.185, 0.66, f'q = {q:#.0f} #pm {eq:#.0f}')
    text3 = TLatex(0.185, 0.62, f'm = ({m:#.3f} #pm {em:#.3f}) ns^{-1}')
    text4 = TLatex(0.185, 0.58, f'#chi^2 / NDF = {fitFunc.GetChisquare():#.2f} / {fitFunc.GetNDF()}')
    for text in [text1, text2, text3, text4]:   
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.8)
        text.SetTextFont(42)
        text.Draw()

    leg = TLegend(0.185, 0.74, 0.5, 0.85)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.9)
    leg.SetFillStyle(0)
    leg.AddEntry(graph, 'TCA peak position')
    leg.AddEntry(fitFunc, 'Fit line')
    leg.Draw()

    outFile.cd()
    graph.Write()
    canvas.Write()
    canvas.SaveAs(canvasPath)

    return q, m, eq, em

def resolution(time, timeSigma):
    pass

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
    delays = [0, 200, 400, 600, 800, 1000]
    labels = ['Delay: 0 ns', 'Delay: 200 ns', 'Delay: 400 ns', 'Delay: 600 ns', 'Delay: 800 ns', 'Delay: 1000 ns',]
    inputFiles =   ['data/input/Gamma/delay_ven/1000ns.mca',
                    'data/input/Gamma/delay_ven/800ns.mca',
                    'data/input/Gamma/delay_ven/600ns.mca',
                    'data/input/Gamma/delay_ven/400ns.mca',
                    'data/input/Gamma/delay_ven/200ns.mca',
                    'data/input/Gamma/delay_ven/0ns.mca'
                    ]

    hists = []
    peakCenter = []
    peakCenterErr = []
    peakSigma = []
    peakSigmaErr = []
    
    for delay, infile in zip(delays, inputFiles):
        hist = TH1D()
        hist = readMCAoutput(infile)
        hist.SetName(f'TACcounts_delay_{delay}')
        hist.SetTitle(f'TAC counts, delay = {delay} ns; Time (chn); Counts (a. u.)')

        hists.append(hist)
        del hist

    outfile = TFile('data/output/Gamma/timeCalibrationMCA.root', 'recreate')
    
    multihist(hists, labels, outfile, 'TAC counts; Time (chn); Counts (a. u.)', 'data/output/Figures/GammaCoincidence/timeDistribution.pdf')     # tac hists

    fitRanges = [[269, 307], [373, 411], [470, 508], [573, 605], [675, 712], [772, 805]]
    for hist, fitRange in zip(hists, fitRanges):                                                              # fit single hist
        hist.Fit('gaus', '', '', fitRange[0], fitRange[1]) 
        fitFunc = hist.GetFunction('gaus')   
        peakCenter.append(fitFunc.GetParameter(1))
        peakCenterErr.append(fitFunc.GetParError(1))
        peakSigma.append(fitFunc.GetParameter(2))
        peakSigmaErr.append(fitFunc.GetParError(2))
        hist.Write()


    print('\n##########Time calibration#########\n')
    q, m, eq, em = calibration(delays, peakCenter, peakSigma, outfile, 'timeCalibrationMCA', 'Time Calibration for the MCA; Delay (ns); Time (chn)', 'data/output/Figures/GammaCoincidence/timeCalibrationMCA.pdf')
    print('\nFit params (y = mx + q):\nq = ', q, ' +- ', eq, '\nm = ', m, ' +- ', em)

    outfile.Close()
    


    
