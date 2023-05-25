import pandas as pd
import numpy as np
import sys 

from ROOT import TH2D, gStyle, TFile, TH1D, TCanvas, TGraph
import uproot

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=5., padbottommargin=0.12, padrightmargin=0.5, padtopmargin=0.1, titleoffsety=1.1, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)


def addHist(df, outputFile, column, plotSpec, histName=''):
    '''
    Directly write to a file a histogram of a given column

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
        column (str): column to plot
        plotSpec (list): [xTitle, nBinsX, Xmin, Xmax]
        histName (str): histogram name
    '''
    [xTitle, nBinsX, Xmin, Xmax] = plotSpec
    
    hist = TH1D(histName, histName, nBinsX, Xmin, Xmax)
    for x in df[column]:    hist.Fill(x)

    hist.GetXaxis().SetTitle(xTitle)
    hist.GetYaxis().SetTitle('Counts (a.u)')

    outputFile.cd()
    hist.Write()

def performHistTest(series1, series2, histSpec, rootFile):
    '''
        Perform Chi2 and Kolmogorov-Smirnov test on histograms from two pandas.Series
    '''

    [nBinsX, Xmin, Xmax] = histSpec
    hist1 = TH1D('hist1', 'hist1', nBinsX, Xmin, Xmax)
    for x in series1:   hist1.Fill(x)
    hist1.Scale(1./hist1.Integral())
    
    hist2 = TH1D('hist2', 'hist2', nBinsX, Xmin, Xmax)
    for x in series2:   hist2.Fill(x)
    hist2.Scale(1./hist2.Integral())

    residual = np.zeros(nBinsX)
    chi2 = hist1.Chi2Test(hist2, 'p', residual)
    #print('Kolmogorov test: ', hist1.Chi2Test(hist2, 'n'))

    
    x = np.arange(Xmin, Xmax)
    resGraph = TGraph(nBinsX, np.asarray(x, dtype='f'), np.asarray(residual, dtype='f'))
    resGraph.SetName('residual_graph')
    resGraph.SetTitle('Residual; Energy (chn); Residual')
    
    rootFile.cd()
    resGraph.Write()

    return resGraph
    


def addTH2(df, outputFile, columnX, columnY, scatSpec, histName=''):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''

    # hist with time conversion
    [xTitle, nBinsX, Xmin, Xmax, yTitle, nBinsY, Ymin, Ymax] = scatSpec
    hist = TH2D(histName, histName, nBinsX, Xmin, Xmax, nBinsY, Ymin, Ymax)
    for x, y in zip(df[columnX], df[columnY]):   hist.Fill(x, y)

    hist.GetXaxis().SetTitle(xTitle)
    hist.GetYaxis().SetTitle(yTitle)

    outputFile.cd()
    hist.SetDrawOption('colz1')
    hist.Write()

    return hist

# Data visualization


if __name__ == '__main__':
    
    tree = uproot.open("data/processed/data_tree.root")["fTreeData"]
    df = tree.arrays(library='pd')
    df['tdc_ns'] = df['2228A_-_tdc__ch6'] * 2.5

    rootFilePath = 'data/output/S1SG_peakComparison.root'
    rootFile = TFile(rootFilePath, 'recreate')

    plotSpec = ['CHN (a.u.)', 2048, 0, 2048]
    addHist(df, rootFile, '2249W_-_adc__ch10', plotSpec, 'S1')
    addHist(df, rootFile, '2249W_-_adc__ch11', plotSpec, 'SG')
    

    # select events in the first peak
    dfSgPeak = df.query('0 < `2249W_-_adc__ch11` < 574', inplace=False)
    plotSpec = ['CHN (a.u.)', 2048, 0, 2048]
    addHist(dfSgPeak, rootFile, '2249W_-_adc__ch10', plotSpec, 'S1_with_peakSelection_on_SG')
    addHist(dfSgPeak, rootFile, '2249W_-_adc__ch11', plotSpec, 'SG_with_peakSelection_on_SG')

    dfS1Peak = df.query('0 < `2249W_-_adc__ch10` < 333', inplace=False)
    plotSpec = ['CHN (a.u.)', 2048, 0, 2048]
    addHist(dfS1Peak, rootFile, '2249W_-_adc__ch10', plotSpec, 'S1_with_peakSelection_on_S1')
    addHist(dfS1Peak, rootFile, '2249W_-_adc__ch11', plotSpec, 'SG_with_peakSelection_on_S1')

    # th2 with and without pattern unit selections
    dfPU = df.query('`V259N_-_multi-hit_patter_unit__ch0` == 1', inplace=False)
    addHist(dfPU, rootFile, '2249W_-_adc__ch10', plotSpec, 'S1_PUselections')
    addHist(dfPU, rootFile, '2249W_-_adc__ch11', plotSpec, 'SG_PUselections')
    scatSpec = ['S1 CHN (a.u.)', 2048, 0, 2048, 'SG CHN (a.u.)', 2048, 0, 2048]
    addTH2(df, rootFile, '2249W_-_adc__ch10', '2249W_-_adc__ch11', scatSpec, 'S1_and_SG')
    addTH2(dfPU, rootFile, '2249W_-_adc__ch10', '2249W_-_adc__ch11', scatSpec, 'S1_and_SG_PUselections')

    dfNotPU = df.query('`V259N_-_multi-hit_patter_unit__ch0` == 0', inplace=False)
    addHist(dfNotPU, rootFile, '2249W_-_adc__ch10', plotSpec, 'S1_NotPUselections')
    addHist(dfNotPU, rootFile, '2249W_-_adc__ch11', plotSpec, 'SG_NotPUselections')

    # KS test
    histSpec = [732, 254, 986]
    performHistTest(df['2249W_-_adc__ch10'], dfSgPeak['2249W_-_adc__ch10'], histSpec, rootFile)

    rootFile.Close()


