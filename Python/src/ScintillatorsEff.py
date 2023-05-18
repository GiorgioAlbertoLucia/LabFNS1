'''
Script for plotting the counts vs HV to decide the working point of the scintillators
CSV should have 1st column = HV, 2nd column = counts, 3rd column = HV error
Counts distribution is considered to be poissonian -> counts_err = sqrt(counts)
'''

import pandas as pd
import numpy as np
import sys
sys.path.append("Python/utils")

from StyleFormatter import SetGlobalStyle, SetObjectStyle
from math import sqrt
from ROOT import TGraphErrors, TCanvas, TFile, gPad, gStyle, TLatex, kAzure

SetGlobalStyle(padleftmargin=0.1, padbottommargin=0.11, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1, titleoffsetx=1.0, titleoffset= 0.7, opttitle=1)

def scintEff(input_path, root_file, scint_name):

    df = pd.read_csv(input_path)
    df['HV err'] = df['HV[V*1000]']*0.008 + 0.002
    df['Counts err']=np.sqrt(df['Counts'])

    df['HV[V*1000]'] = df['HV[V*1000]'] * 1000
    df['HV err'] = df['HV err'] * 1000

    df['Rate'] = df['Counts'] / 300
    df['Rate err'] = df['Counts err'] / 300

    histo = TGraphErrors(len(df),np.asarray(df['HV[V*1000]'],'d'),np.asarray(df['Counts'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['Counts err'],'d'))
    histo.SetTitle(f"{scint_name} Counts")
    histo.GetXaxis().SetTitle("HV [V]")
    histo.GetYaxis().SetTitle("Counts")

    histo2 = TGraphErrors(len(df),np.asarray(df['HV[V*1000]'],'d'),np.asarray(df['Rate'],'d'),
                     np.asarray(df['HV err'],'d'),np.asarray(df['Rate err'],'d'))
    histo2.SetTitle(f"{scint_name} Rate")
    histo2.GetXaxis().SetTitle("HV [V]")
    histo2.GetYaxis().SetTitle("Rate [Hz]")

    canvas = TCanvas(scint_name, "c" ,1280, 720)
    canvas.cd()
    canvas.SetLogy()
    SetObjectStyle(histo,color=kAzure+3)
    histo.Draw("APZL")

    canvas2 = TCanvas(f'{scint_name}_rate', "c" ,1280, 720)
    canvas2.cd()
    SetObjectStyle(histo2,color=kAzure+3)
    histo2.Draw("APZL")

    gPad.Modified()
    gPad.Update()

    root_file.cd()
    canvas.Write()
    canvas2.Write()


def AdjustFigures(root_file):
    root_file.cd()

    cS1 = root_file.Get('S1')
    gS1=cS1.GetPrimitive("Graph")
    SetObjectStyle(gS1,color=kAzure+3, markersize=1.5)

    cS1new=TCanvas("Canvas","Canvas",1300,1300)
    cS1new.DrawFrame(1800,1.e+2,2700,5.e+6,"S1 Counts; HV [V]; Counts")
    cS1new.Modified()
    cS1new.Update()
    cS1new.SetLogy()
    gS1.Draw("PZ")

    text =TLatex(0.4, 0.42,"S1 Scintillator + PMXP2020")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.4, 0.37,"Acquisition time: 300 s")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.4, 0.32,"Discriminator threshold value: (-39.6 #pm 0.5) mV")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()

    cS1new.SaveAs('data/output/Figures/S1WorkingPoint.pdf')

    cS2 = root_file.Get('S2')
    gS2=cS2.GetPrimitive("Graph")
    SetObjectStyle(gS2,color=kAzure+3, markersize=1.5)

    cS2new=TCanvas("Canvas","Canvas",1300,1300)
    cS2new.DrawFrame(1800,2.,2700,5.e+5,"S2 Counts; HV [V]; Counts")
    cS2new.Modified()
    cS2new.Update()
    cS2new.SetLogy()
    gS2.Draw("PZ")

    text =TLatex(0.4, 0.32,"S2 Scintillator + PMXP2020")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.4, 0.27,"Acquisition time: 300 s")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.4, 0.22,"Discriminator threshold value: (-20.1 #pm 0.4) mV")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()

    cS2new.SaveAs('data/output/Figures/S2WorkingPoint.pdf')

    cS3 = root_file.Get('S3')
    gS3=cS3.GetPrimitive("Graph")
    SetObjectStyle(gS3,color=kAzure+3, markersize=1.5)

    cS3new=TCanvas("Canvas","Canvas",1300,1300)
    cS3new.DrawFrame(1800,.8,2700,3.e+5,"S3 Counts; HV [V]; Counts")
    cS3new.Modified()
    cS3new.Update()
    cS3new.SetLogy()
    gS3.Draw("PZ")

    text =TLatex(0.4, 0.42,"S3 Scintillator + PMXP2020")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.4, 0.37,"Acquisition time: 300 s")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.4, 0.32,"Discriminator threshold value: (-20.1 #pm 0.4) mV")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()

    cS3new.SaveAs('data/output/Figures/S3WorkingPoint.pdf')
    
    cSG = root_file.Get('SG')
    gSG=cSG.GetPrimitive("Graph")
    SetObjectStyle(gSG,color=kAzure+3, markersize=1.5)

    cSGnew=TCanvas("Canvas","Canvas",1300,1300)
    cSGnew.DrawFrame(1100,.8,2100,9.e+7,"SG Counts; HV [V]; Counts")
    cSGnew.Modified()
    cSGnew.Update()
    cSGnew.SetLogy()
    gSG.Draw("PZ")

    text =TLatex(0.4, 0.42,"SG Scintillator + PMXP2020")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.4, 0.37,"Acquisition time: 300 s")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.4, 0.32,"Discriminator threshold value: (-10.2 #pm 0.2) mV")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()

    cSGnew.SaveAs('data/output/Figures/SGWorkingPoint.pdf')



if __name__ == '__main__':
    
    outfilePath = 'data/output/HVwork.root'
    root_file = TFile(outfilePath, 'recreate')

    infilePaths = ['data/input/HVworkS1.csv',
                   'data/input/HVworkSG.csv',
                   'data/input/HVworkS2.csv',
                   'data/input/HVworkS3.csv']
    scintNames = ['S1', 'SG', 'S2', 'S3']

    for input_path, scint_name in zip(infilePaths, scintNames):
        scintEff(input_path, root_file, scint_name)

    AdjustFigures(root_file)


