import pandas as pd
import numpy as np
import sys 

from ROOT import TH2D, gStyle, TFile
import uproot

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=5., padbottommargin=0.12, padrightmargin=0.5, padtopmargin=0.1, titleoffsety=1.1, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)


#
def AdcTdc2dimHistCompare(df, outputFile):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''

    # hist in channels
    histCHN = TH2D('tdcCHN_vs_adc', 'TDC (CHN) data vs ADC data', 256, 0, 2048, 2048, 0, 2048)
    for x, y in zip(df['2228A_-_tdc__ch6'], df['2249W_-_adc__ch11']):   histCHN.Fill(x, y)

    histCHN.GetXaxis().SetTitle('CHN (a.u.)')
    histCHN.GetYaxis().SetTitle('Energy ()')

    # hist with time conversion
    hist = TH2D('tdc_vs_adc', 'TDC data vs ADC data', 256, 0, 5120, 2048, 0, 2048)
    for x, y in zip(df['tdc_ns'], df['2249W_-_adc__ch11']):   hist.Fill(x, y)

    hist.GetXaxis().SetTitle('#DeltaT (ns)')
    hist.GetYaxis().SetTitle('Energy ()')
    gStyle.SetPalette(53)

    outputFile.cd()
    histCHN.SetDrawOption('colz1')
    histCHN.Write()
    hist.SetDrawOption('colz1')
    hist.Write()

    return hist

def TDCprojection(hist, firstBin, lastBin, outputFile):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''
    
    proj = hist.ProjectionX(f'TDCproj_{firstBin}_{lastBin}', firstBin, lastBin)
    proj.SetTitle(f'TDC projection ({firstBin} to {lastBin}); #DeltaT (ns); Counts (a.u.)')

    outputFile.cd()
    proj.Write()

def ADCprojection(hist, firstBin, lastBin, outputFile):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''

    ADC_hist = hist.ProjectionY(' ')
    proj = hist.ProjectionY(f'ADCproj_{firstBin}_{lastBin}', firstBin, lastBin)
    proj.SetTitle(f'ADC projection ({firstBin} to {lastBin}); #Energy (); Counts (a.u.)')

    outputFile.cd()
    proj.Write()

# Data visualization


if __name__ == '__main__':
    
    tree = uproot.open("data/processed/data_tree.root")["fTreeData"]
    df = tree.arrays(library='pd')
    df['tdc_ns'] = df['2228A_-_tdc__ch6'] * 2.5

    rootFilePath = 'data/output/ADC_TDC_comparison.root'
    rootFile = TFile(rootFilePath, 'recreate')

    # Produce TH2 and projections along axis
    hist = AdcTdc2dimHistCompare(df, rootFile)

    TDCprojBinList = [[320, 340], [520, 540], [720, 740], [920, 940], [1120, 1140], 
                      [1320, 1340], [1520, 1540], [1720, 1740], [1920, 1940], [2120, 2140],
                      [2320, 2340]]
    for bin_edges in TDCprojBinList:    TDCprojection(hist, bin_edges[0]+1, bin_edges[1], rootFile)   

    ADCprojBinList = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]]
    for bin_edges in ADCprojBinList:    ADCprojection(hist, bin_edges[0]+1, bin_edges[1], rootFile) 



    rootFile.Close()


