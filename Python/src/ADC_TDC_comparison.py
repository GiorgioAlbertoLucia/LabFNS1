'''
    Run from LABFNS1 with: python3 -m Python.src.ADC_TDC_comparison
'''

import pandas as pd
import numpy as np
import sys 

from ROOT import TH2D, gStyle, TFile
import uproot

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=5., padbottommargin=0.12, padrightmargin=0.5, padtopmargin=0.1, titleoffsety=1.1, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)


#
def AdcTdc2dimHistCompare(df, outputFile, ADCchannel, PUselections=False):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''

    
    extra1 = ''
    extra2 = ''
    if PUselections:    
        extra1 = '_PUsel'
        extra2 = ' PUsel'

    # hist in channels
    histCHN = TH2D(f'tdcCHN_vs_adc_ch{ADCchannel}{extra1}', f'TDC (CHN) data vs ADC data ch{ADCchannel}{extra2}', 256, 0, 2048, 2048, 0, 2048)
    for x, y in zip(df['2228A_-_tdc__ch6'], df[f'2249W_-_adc__ch{ADCchannel}']):   histCHN.Fill(x, y)

    histCHN.GetXaxis().SetTitle('CHN (a.u.)')
    histCHN.GetYaxis().SetTitle('Energy (chn)')

    # hist with time conversion
    hist = TH2D(f'tdc_vs_adc_ch{ADCchannel}{extra1}', f'TDC data vs ADC data ch{ADCchannel}{extra2}', 256, 0, 5120, 2048, 0, 2048)
    for x, y in zip(df['tdc_ns'], df[f'2249W_-_adc__ch{ADCchannel}']):   hist.Fill(x, y)

    hist.GetXaxis().SetTitle('#DeltaT (ns)')
    hist.GetYaxis().SetTitle('Energy (chn)')
    gStyle.SetPalette(53)

    outputFile.cd()
    histCHN.SetDrawOption('colz1')
    histCHN.Write()
    hist.SetDrawOption('colz1')
    hist.Write()

    return hist

def TDCprojection(hist, firstBin, lastBin, outputFile, ADCchannel):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''
    
    proj = hist.ProjectionX(f'TDCproj_{firstBin}_{lastBin}_ch{ADCchannel}', firstBin, lastBin)
    proj.SetTitle(f'TDC projection_ch{ADCchannel} ({firstBin} to {lastBin}); #DeltaT (ns); Counts (a.u.)')

    proj.GetXaxis().SetTitle('#DeltaT (ns)')
    proj.GetYaxis().SetTitle('Counts (a.u.)')

    outputFile.cd()
    proj.Write()

def ADCprojection(hist, firstBin, lastBin, outputFile, ADCchannel):
    '''
    Create a 2-dim histogram with data from adc and tdc.

    Parameters
    ----------
        df (pd.DataFrame): input dataset to get adc and tdc data from
        outputFile (TFile): file to write the output to
    '''

    ADC_hist = hist.ProjectionY(' ')
    proj = hist.ProjectionY(f'ADCproj_{firstBin}_{lastBin}_ch{ADCchannel}', firstBin, lastBin)
    proj.SetTitle(f'ADC projection ch{ADCchannel} ({firstBin} to {lastBin}); #Energy (chn); Counts (a.u.)')

    proj.GetXaxis().SetTitle('Energy (chn)')
    proj.GetYaxis().SetTitle('Counts (a.u.)')

    outputFile.cd()
    proj.Write()

# Data visualization


if __name__ == '__main__':
    
    tree = uproot.open("data/processed/data_tree.root")["fTreeData"]
    df = tree.arrays(library='pd')
    df['tdc_ns'] = df['2228A_-_tdc__ch6'] * 2.5
    dfPU = df.query('`V259N_-_multi-hit_patter_unit__ch0` == 1', inplace=False)

    rootFilePath = 'data/output/ADC_TDC_comparison.root'
    rootFile = TFile(rootFilePath, 'recreate')

    # Produce TH2 and projections along axis
    hist10 = AdcTdc2dimHistCompare(df, rootFile, 10)
    print('Pearson correlation (ch10): ', df['2249W_-_adc__ch10'].corr(df['2228A_-_tdc__ch6'], method='pearson'))
    print('Spearman correlation (ch10): ', df['2249W_-_adc__ch10'].corr(df['2228A_-_tdc__ch6'], method='spearman'))
    hist11 = AdcTdc2dimHistCompare(df, rootFile, 11)
    print('Pearson correlation (ch11): ', df['2249W_-_adc__ch11'].corr(df['2228A_-_tdc__ch6'], method='pearson'))
    print('Spearman correlation (ch11): ', df['2249W_-_adc__ch11'].corr(df['2228A_-_tdc__ch6'], method='spearman'))
    AdcTdc2dimHistCompare(dfPU, rootFile, 10, True)
    AdcTdc2dimHistCompare(dfPU, rootFile, 11, True)

    TDCprojBinList = [[320, 340], [520, 540], [720, 740], [920, 940], [1120, 1140], 
                      [1320, 1340], [1520, 1540], [1720, 1740], [1920, 1940], [2120, 2140],
                      [2320, 2340]]
    for bin_edges in TDCprojBinList:    
        TDCprojection(hist10, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=10)
        TDCprojection(hist11, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=11)
       

    ADCprojBinList = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]]
    for bin_edges in ADCprojBinList:    
        ADCprojection(hist10, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=10)
        ADCprojection(hist11, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=11) 

    rootFile.Close()


