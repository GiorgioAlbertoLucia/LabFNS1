'''
    Run from LABFNS1 with: python3 -m Python.src.Comparisons
'''

import pandas as pd
import numpy as np
import sys 

from ROOT import TH1D, TH2D, gStyle, gPad, TFile, TCanvas, TLegend, TLatex, TF1, TLine, TText
from ROOT import kOrange, kGray, kAzure, kRed, kGreen, kBlue, kBlack
import uproot

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
#SetGlobalStyle(padleftmargin=5., padbottommargin=0.12, padrightmargin=0.5, padtopmargin=0.1, titleoffsety=1.1, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)
gStyle.SetOptStat(0)

# Data visualization

def PatternUnitSelection(df, dfPU, outputFile):
    '''
    Create histograms to compare data with and without selections with Pattern Unit
    '''

    # CHANNEL 10 (i.e. S1)
    canvas10 = TCanvas('adc_PU_comp_ch10', '', 1500, 1500)

    ADChist10 = TH1D('ADChist10', '', 235, 0, 2048)
    ADChist10.SetLineColor(kGray+2)
    ADChist10.SetFillColorAlpha(kGray+2, 0.5)
    ADChist10.SetTitle('ADC data with pattern unit selections (S1); Energy (chn); Counts (a.u.)')
    for x in df['2249W_-_adc__ch10']:    ADChist10.Fill(x)

    ADChistPU10 = TH1D('ADChistPU10', '', 235, 0, 2048)
    ADChistPU10.SetLineColor(kOrange-3)
    ADChistPU10.SetFillColorAlpha(kOrange-3, 0.5)
    ADChistPU10.SetTitle('ADC data with pattern unit selections (S1); Energy (chn); Counts (a.u.)')
    for x in dfPU['2249W_-_adc__ch10']:    ADChistPU10.Fill(x)

    leg1 = TLegend(0.55, 0.4, 0.75, 0.7)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(ADChist10, 'All events', 'lf')
    leg1.AddEntry(ADChistPU10, 'Events selected by the pattern unit', 'lf')

    canvas10.cd()
    ADChist10.Draw('hist')
    ADChistPU10.Draw('hist same')
    leg1.Draw('same')
    #canvas.DrawFrame(0, 0, 2048, 1000, 'ADC data with pattern unit selections (S1); Energy (chn); Counts (a.u.)')

    outputFile.cd()
    ADChist10.Write()
    ADChistPU10.Write()
    canvas10.Write()
    canvas10.SaveAs('data/output/ComparisonADCpuS1.pdf')

    # CHANNEL 11 (i.e. SG)
    canvas11 = TCanvas('adc_PU_comp_ch11', '', 1500, 1500)

    ADChist11 = TH1D('ADChist11', '', 235, 0, 2048)
    ADChist11.SetLineColor(kGray+2)
    ADChist11.SetFillColorAlpha(kGray+2, 0.5)
    ADChist11.SetTitle('ADC data with pattern unit selections (SG); Energy (chn); Counts (a.u.)')
    for x in df['2249W_-_adc__ch11']:    ADChist11.Fill(x)

    ADChistPU11 = TH1D('ADChistPU11', '', 235, 0, 2048)
    ADChistPU11.SetLineColor(kOrange-3)
    ADChistPU11.SetFillColorAlpha(kOrange-3, 0.5)
    ADChistPU11.SetTitle('ADC data with pattern unit selections (SG); Energy (chn); Counts (a.u.)')
    for x in dfPU['2249W_-_adc__ch11']:    ADChistPU11.Fill(x)

    leg1 = TLegend(0.55, 0.4, 0.75, 0.7)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(ADChist11, 'All events', 'lf')
    leg1.AddEntry(ADChistPU11, 'Events selected by the pattern unit', 'lf')

    canvas11.cd()
    ADChist11.Draw('hist')
    ADChistPU11.Draw('hist same')
    leg1.Draw('same')
    #canvas.DrawFrame(0, 0, 2048, 1100, 'ADC data with pattern unit selections (S1); Energy (chn); Counts (a.u.)')

    outputFile.cd()
    ADChist11.Write()
    ADChistPU11.Write()
    canvas11.Write()
    canvas11.SaveAs('data/output/ComparisonADCpuSG.pdf')

def secondPeakSelection(df, outputFile):

    # CHANNEL 10 (i.e. S1)
    dfSel = df.query('`2249W_-_adc__ch10` > 340', inplace=False)
    canvas10 = TCanvas('adc_PeakSel_ch10', '', 1500, 1500)

    ADChist10 = TH1D('ADChist10', '', 235, 0, 2048)
    ADChist10.SetLineColor(kGray+2)
    ADChist10.SetFillColorAlpha(kGray+2, 0.5)
    ADChist10.SetTitle('ADC data with peak selections (S1); Energy (chn); Counts (a.u.)')
    for x in df['2249W_-_adc__ch10']:    ADChist10.Fill(x)

    ADChistSel10 = TH1D('ADChistSel10', '', 235, 0, 2048)
    ADChistSel10.SetLineColor(kGreen-3)
    ADChistSel10.SetFillColorAlpha(kGreen-3, 0.3)
    ADChistSel10.SetTitle('ADC data with peak selections (S1); Energy (chn); Counts (a.u.)')
    for x in dfSel['2249W_-_adc__ch10']:    ADChistSel10.Fill(x)

    leg1 = TLegend(0.55, 0.4, 0.75, 0.7)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(ADChist10, 'All events', 'lf')
    leg1.AddEntry(ADChistSel10, 'Events with energy > 340 chn', 'lf')

    lineAtPedestal = TLine(320, gPad.GetUymax(), 320, gPad.GetUymin())
    lineAtPedestal.SetLineColor(kBlack)
    lineAtPedestal.SetLineWidth(2)
    lineAtPedestal.SetLineStyle(7)

    pedestal= TText(0.24,0.7,"Pedestal")
    pedestal.SetNDC()
    pedestal.SetTextSize(gStyle.GetTextSize()*0.7)
    pedestal.SetTextAngle(90)
    pedestal.SetTextFont(42)

    canvas10.cd()
    ADChist10.Draw('hist')
    ADChistSel10.Draw('hist same')
    leg1.Draw('same')
    lineAtPedestal.Draw('same')
    pedestal.Draw('same')

    outputFile.cd()
    canvas10.Write()
    canvas10.SaveAs('data/output/ComparisonADCpeakS1.pdf')

    # TH2

    canvas20 = TCanvas('th2_PeakSel_ch10', '', 1500, 1500)

    hist10 = TH2D('hist10', '', 125, 0, 5000, 235, 0, 2048)
    for x, y in zip(df['tdc_ns'], df['2249W_-_adc__ch10']): hist10.Fill(x, y)
    hist10.SetTitle('ADC and TDC data with peak selections (S1); Time (ns); Energy (chn)')
    hist10.SetMarkerStyle(3)
    hist10.SetMarkerColor(kGray+2)

    hist10Sel = TH2D('hist10Sel', '', 125, 0, 5000, 235, 0, 2048)
    for x, y in zip(dfSel['tdc_ns'], dfSel['2249W_-_adc__ch10']): hist10Sel.Fill(x, y)
    hist10Sel.SetTitle('ADC and TDC data with peak selections (S1); Time (ns); Energy (chn)')
    hist10Sel.SetMarkerStyle(3)
    hist10Sel.SetMarkerColor(kGreen-3)

    leg1 = TLegend(0.55, 0.7, 0.75, 0.8)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(hist10, 'All events', 'pf')
    leg1.AddEntry(hist10Sel, 'Events with energy > 340 chn', 'pf')

    lineAtPedestal = TLine(canvas20.GetUxmax(), 320, canvas20.GetUxmin(), 320)
    lineAtPedestal.SetLineColor(kBlack)
    lineAtPedestal.SetLineWidth(1)
    lineAtPedestal.SetLineStyle(7)

    pedestal= TText(0.7,0.21,"Pedestal")
    pedestal.SetNDC()
    pedestal.SetTextSize(gStyle.GetTextSize()*0.7)
    pedestal.SetTextFont(42)

    canvas20.cd()
    hist10.Draw('scat')
    hist10Sel.Draw('scat same')
    leg1.Draw('same')

    outputFile.cd()
    canvas20.Write()
    canvas20.SaveAs('data/output/ComparisonTH2peakS1.pdf')




    # CHANNEL 11 (i.e. S1)
    dfSel = df.query('`2249W_-_adc__ch11` > 584', inplace=False)
    canvas11 = TCanvas('adc_PeakSel_ch11', '', 1500, 1500)

    ADChist11 = TH1D('ADChist11', '', 235, 0, 2048)
    ADChist11.SetLineColor(kGray+2)
    ADChist11.SetFillColorAlpha(kGray+2, 0.5)
    ADChist11.SetTitle('ADC data with peak selections (SG); Energy (chn); Counts (a.u.)')
    for x in df['2249W_-_adc__ch11']:    ADChist11.Fill(x)

    ADChistSel11 = TH1D('ADChistSel11', '', 235, 0, 2048)
    ADChistSel11.SetLineColor(kGreen-3)
    ADChistSel11.SetFillColorAlpha(kGreen-3, 0.3)
    ADChistSel11.SetTitle('ADC data with peak selections (SG); Energy (chn); Counts (a.u.)')
    for x in dfSel['2249W_-_adc__ch11']:    ADChistSel11.Fill(x)

    leg1 = TLegend(0.55, 0.4, 0.75, 0.7)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(ADChist11, 'All events', 'lf')
    leg1.AddEntry(ADChistSel11, 'Events with energy > 584 chn', 'lf')

    lineAtPedestal = TLine(320, gPad.GetUymax(), 320, gPad.GetUymin())
    lineAtPedestal.SetLineColor(kBlack)
    lineAtPedestal.SetLineWidth(1)
    lineAtPedestal.SetLineStyle(7)

    pedestal= TText(0.24,0.7,"Pedestal")
    pedestal.SetNDC()
    pedestal.SetTextSize(gStyle.GetTextSize()*0.7)
    pedestal.SetTextAngle(90)
    pedestal.SetTextFont(42)

    canvas11.cd()
    ADChist11.Draw('hist')
    ADChistSel11.Draw('hist same')
    leg1.Draw('same')
    lineAtPedestal.Draw()
    pedestal.Draw('same')

    outputFile.cd()
    canvas11.Write()
    canvas11.SaveAs('data/output/ComparisonADCpeakSG.pdf')

    # TH2

    canvas21 = TCanvas('th2_PeakSel_ch11', '', 1500, 1500)

    hist11 = TH2D('hist11', '', 125, 0, 5000, 235, 0, 2048)
    for x, y in zip(df['tdc_ns'], df['2249W_-_adc__ch11']): hist11.Fill(x, y)
    hist11.SetTitle('ADC and TDC data with peak selections (SG); Time (ns); Energy (chn)')
    hist11.SetMarkerStyle(3)
    hist11.SetMarkerColor(kGray+2)

    hist11Sel = TH2D('hist11Sel', '', 125, 0, 5000, 235, 0, 2048)
    for x, y in zip(dfSel['tdc_ns'], dfSel['2249W_-_adc__ch11']): hist11Sel.Fill(x, y)
    hist11Sel.SetTitle('ADC and TDC data with peak selections (SG); Time (ns); Energy (chn)')
    hist11Sel.SetMarkerStyle(3)
    hist11Sel.SetMarkerColor(kGreen-3)

    leg1 = TLegend(0.55, 0.7, 0.75, 0.8)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(hist11, 'All events', 'pf')
    leg1.AddEntry(hist11Sel, 'Events with energy > 584 chn', 'pf')

    lineAtPedestal = TLine(gPad.GetUxmax(), 320, gPad.GetUxmin(), 320)
    lineAtPedestal.SetLineColor(kBlack)
    lineAtPedestal.SetLineWidth(1)
    lineAtPedestal.SetLineStyle(7)

    pedestal = TText(0.7,0.21,"Pedestal")
    pedestal.SetNDC()
    pedestal.SetTextSize(gStyle.GetTextSize()*0.7)
    pedestal.SetTextFont(42)

    canvas21.cd()
    hist11.Draw('scat')
    hist11Sel.Draw('scat same')
    leg1.Draw('same')
    lineAtPedestal.Draw()
    pedestal.Draw('same')

    outputFile.cd()
    canvas21.Write()
    canvas21.SaveAs('data/output/ComparisonTH2peakSG.pdf')

def TDCwithSelection(df, outputFile):
    
    dfSel = df.query('`2249W_-_adc__ch10` > 340 and `2249W_-_adc__ch11` > 584', inplace=False)
    dfDisc = df.query('`2249W_-_adc__ch10` < 340 or `2249W_-_adc__ch11` < 584', inplace=False)

    # Discarded events
    canvas = TCanvas('adc_PeakSel_ch11', '', 1500, 1500)
    canvas.SetLogy()

    TDChist = TH1D('TDChist', '', 125, 0, 5000)
    TDChist.SetLineColor(kGray+2)
    TDChist.SetFillColorAlpha(kGray+2, 0.5)
    TDChist.SetTitle('TDC data with discarded events; Time (ns); Counts (a.u.)')
    for x in df['tdc_ns']:    TDChist.Fill(x)

    TDChistDisc = TH1D('TDChistDisc', '', 125, 0, 5000)
    TDChistDisc.SetLineColor(kRed-3)
    TDChistDisc.SetFillColorAlpha(kRed-3, 0.3)
    TDChistDisc.SetTitle('TDC data with discarded events; Time (ns); Counts (a.u.)')
    for x in dfDisc['tdc_ns']:    TDChistDisc.Fill(x)

    leg1 = TLegend(0.55, 0.4, 0.75, 0.7)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(TDChist, 'All events', 'lf')
    leg1.AddEntry(TDChistDisc, 'Discarded events', 'lf')

    canvas.cd()
    TDChist.Draw('hist')
    TDChistDisc.Draw('hist same')
    leg1.Draw('same')

    outputFile.cd()
    canvas.Write()
    canvas.SaveAs('data/output/ComparisonTDCdiscards.pdf')


    # FIT

    cS1 = TCanvas("cS1","cS1",1500,1500)
    cS1.cd()
    cS1.SetLogy()

    hTDC = TH1D("hTDC","hTDC",125,0,5000)
    for x in dfSel["tdc_ns"]: hTDC.Fill(x)
    hTDC.SetFillColorAlpha(kOrange-3, 0.5)

    funz = TF1("funz","[0]+[1]*exp(x*[2])",20,800)
    funz1 = TF1("funz1","[0]+[1]*exp(x*[2])",2000,5000)
    funz2 = TF1("funz2","[0]+[1]*exp(x*[2])+[3]*exp(x*[4])",300, 800)

    funz1.SetParameter(0,0)
    funz1.SetParLimits(0, 0, 1e6)
    funz1.SetParameter(1, 68)
    funz1.SetParameter(2, -0.00045)
    hTDC.Fit(funz1,"RM+")
    print('Chi square fit 1 / DoF = ', funz1.GetChisquare(), '/', funz1.GetNDF())

    funz2.SetParameter(0, funz1.GetParameter(0))
    funz2.SetParLimits(0, 0, 1e6)
    funz2.SetParameter(1, funz1.GetParameter(1))
    funz2.SetParLimits(1, 0, 1e6)
    funz2.SetParameter(2, funz1.GetParameter(2))
    funz2.SetParLimits(2, -0.0007, -0.0003)
    funz2.SetParameter(3, 1.7e4)
    funz2.SetParLimits(3, 0, 1e6)
    funz2.SetParameter(4, -0.009)
    funz2.SetParLimits(4, -0.011, -0.007)
    hTDC.Fit(funz2,"RM+")
    print('Chi square fit 2 / DoF = ', funz2.GetChisquare(), '/', funz2.GetNDF())

    funz.SetLineColor(kBlue)
    funz1.SetLineColor(kRed)
    funz2.SetLineColor(kGreen)

    hTDC.Draw("hist e0")
    funz1.Draw('same')
    funz2.Draw('same')

    hTDC.SetTitle("TDC intervals with ADC selections; Time (ns); Counts (a.u)")

    text =TLatex(0.30, 0.7,"TDC LeCroy 2228A")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.30, 0.62,"ADC selections")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.30, 0.56,"Acquisition time: 236985 s")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()
    text4 =TLatex(0.30, 0.48,"Fake stop time: 6 #mus")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw()

    leg = TLegend(0.55, 0.51, 0.85, 0.72)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)

    leg.AddEntry(hTDC, 'TDC_data', 'lf')
    leg.AddEntry(funz1, 'N_{0} + c_{1} e^{-#lambda_{dec} t}', 'lf')
    leg.AddEntry(funz2, 'N_{0} + c_{1} e^{-#lambda_{dec} t} + c_{2} e^{-#lambda_{cat} t}', 'lf')
    leg.Draw('same')

    outputFile.cd()
    cS1.Write()
    cS1.SaveAs('data/output/ComparisonsTDC.pdf')





if __name__ == '__main__':
    
    tree = uproot.open("data/processed/data_tree.root")["fTreeData"]
    df = tree.arrays(library='pd')
    df['tdc_ns'] = df['2228A_-_tdc__ch6'] * 2.5
    dfPU = df.query('`V259N_-_multi-hit_patter_unit__ch0` == 0', inplace=False)

    rootFilePath = 'data/output/Comparison.root'
    rootFile = TFile(rootFilePath, 'recreate')

    PatternUnitSelection(df, dfPU, rootFile)
    secondPeakSelection(df, rootFile)
    TDCwithSelection(df, rootFile)

    ## Produce TH2 and projections along axis
    #hist10 = AdcTdc2dimHistCompare(df, rootFile, 10)
    #print('Pearson correlation (ch10): ', df['2249W_-_adc__ch10'].corr(df['2228A_-_tdc__ch6'], method='pearson'))
    #print('Spearman correlation (ch10): ', df['2249W_-_adc__ch10'].corr(df['2228A_-_tdc__ch6'], method='spearman'))
    #hist11 = AdcTdc2dimHistCompare(df, rootFile, 11)
    #print('Pearson correlation (ch11): ', df['2249W_-_adc__ch11'].corr(df['2228A_-_tdc__ch6'], method='pearson'))
    #print('Spearman correlation (ch11): ', df['2249W_-_adc__ch11'].corr(df['2228A_-_tdc__ch6'], method='spearman'))
    #AdcTdc2dimHistCompare(dfPU, rootFile, 10, True)
    #AdcTdc2dimHistCompare(dfPU, rootFile, 11, True)

    #TDCprojBinList = [[320, 340], [520, 540], [720, 740], [920, 940], [1120, 1140], 
    #                  [1320, 1340], [1520, 1540], [1720, 1740], [1920, 1940], [2120, 2140],
    #                  [2320, 2340]]
    #for bin_edges in TDCprojBinList:    
    #    TDCprojection(hist10, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=10)
    #    TDCprojection(hist11, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=11)
    #   

    #ADCprojBinList = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]]
    #for bin_edges in ADCprojBinList:    
    #    ADCprojection(hist10, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=10)
    #    ADCprojection(hist11, bin_edges[0]+1, bin_edges[1], rootFile, ADCchannel=11) 

    rootFile.Close()


