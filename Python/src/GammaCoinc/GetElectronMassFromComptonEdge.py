import sys
sys.path.append('Python/utils')
import numpy as np

from ReadMCA import CreateHist, GetPandas
from GammaCalibration import GetEnergyFromChnA, GetEnergyFromChnB, GetChnFromEnergyA, GetChnFromEnergyB, GetParametersA, GetParametersB, GetParametersErrorA, GetParametersErrorB
from ROOT import TCanvas, TPad, TH1D, TGraphErrors, TFile, TLatex, TLegend, TF1, TArrow, kAzure, kOrange, kRed, kBlue, kGreen, kFullCircle, gStyle, gPad
from StyleFormatter import SetObjectStyle, SetGlobalStyle 
from math import sqrt

def GetErrorMassPlusCalibrationA(edge, err):
    aerr, berr = GetParametersErrorA()
    a, b = GetParametersA()
    chnedge = GetChnFromEnergyA(edge)
    erredgechn = err * a
    cov = -0.34
    Eerr = (berr*berr+ erredgechn*erredgechn)/((chnedge - b)*(chnedge - b))
    Eerr += aerr*aerr/a/a
    Eerr -= 2*cov/a/(chnedge-b)
    Eerr = edge * sqrt(Eerr)
    return Eerr

def GetErrorMassPlusCalibrationB(edge, err):
    aerr, berr = GetParametersErrorB()
    a, b = GetParametersB()
    chnedge = GetChnFromEnergyB(edge)
    erredgechn = err * a
    cov = -0.4
    Eerr = (berr*berr+ erredgechn*erredgechn)/((chnedge - b)*(chnedge - b))
    Eerr += aerr*aerr/a/a
    Eerr -= 2*cov/a/(chnedge-b)
    Eerr = edge * sqrt(Eerr)
    return Eerr

def GetElectronMass(edge, err, Egamma):
    m = 2*Egamma*(Egamma-edge)/edge
    err = 2*Egamma*err*(Egamma/edge/edge)
    return m, err




if __name__ == '__main__':

    inFileSodiumA = 'data/input/Gamma/SodiocalibrazioneA.mca'
    inFileCobaltA = 'data/input/Gamma/CobaltocalibrazioneA.mca'
    inFileSodiumB = 'data/input/Gamma/SodiocalibrazioneB.mca'
    inFileCobaltB = 'data/input/Gamma/CobaltocalibrazioneB.mca'


    canvas = TCanvas("c","c",1920,1080)
    canvas.Divide(3,2)
    hFrame1 = canvas.cd(1).DrawFrame(150,0.1,500,7.e3,"Sodium, Scintillator A;Energy [keV];Counts")
    hFrame1.SetTitleOffset(1.,"Y")
    hFrame1.GetYaxis().SetMaxDigits(2)
    #gPad.SetLogy()
    df511SodiumA = GetPandas(inFileSodiumA)
    df511SodiumA = np.asarray(df511SodiumA[0],'d')
    
    energychannels = []
    for idx, counts in enumerate(df511SodiumA):
        energychannels.append(GetEnergyFromChnA(idx)[0])
    energychannels = np.asarray(energychannels, 'd')
    print(energychannels)
    
    histo511SodiumA = TH1D("histo511SodiumA","histo511SodiumA",len(energychannels),np.amin(energychannels),np.amax(energychannels))
    histo511SodiumA.FillN(len(energychannels),energychannels,df511SodiumA)
    histo511SodiumA.Rebin(4)
    SetObjectStyle(histo511SodiumA, color = kOrange-3, fillalpha = 0.5)
    fit511SodiumA = TF1("fit511SodiumA","[0]+[1]/(1+exp(-(-x+[2])/[3]))+[4]*exp(-x*[5])",275,450)
    fit511SodiumA.SetParNames("bkg","a","x0","b")
    fit511SodiumA.SetParameters(1000,4000,340,10,0.1,0.01)
    histo511SodiumA.Draw('hist,same')
    histo511SodiumA.Fit(fit511SodiumA,'LR')
    fit511SodiumA.Draw("same")
    erroredge = GetErrorMassPlusCalibrationA(fit511SodiumA.GetParameter(2),fit511SodiumA.GetParameter(3))
    print(erroredge)
    print(GetElectronMass(fit511SodiumA.GetParameter(2),erroredge,511))
    text = TLatex(0.2, 0.80,f"Electron mass: ({round(GetElectronMass(fit511SodiumA.GetParameter(2),erroredge,511)[0]/100):1d} #pm {round(GetElectronMass(fit511SodiumA.GetParameter(2),erroredge,511)[1]/100):1d})#upoint"+ " 10^{2} keV/c^{2}")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize()*0.9)
    text.SetTextFont(42)
    text.Draw("same")

    hFrame2 = canvas.cd(2).DrawFrame(800,0,1275,1.6e3,"Sodium, Scintillator A;Energy [keV];Counts")
    hFrame2.SetTitleOffset(1.,"Y")
    hFrame2.GetYaxis().SetMaxDigits(2)
    df1275SodiumA = GetPandas(inFileSodiumA)
    df1275SodiumA = np.asarray(df1275SodiumA[0],'d')
    histo1275SodiumA = TH1D("histo1275SodiumA","histo1275SodiumA",len(energychannels),np.amin(energychannels),np.amax(energychannels))
    histo1275SodiumA.FillN(len(energychannels),energychannels,df1275SodiumA)
    histo1275SodiumA.Rebin(4)
    SetObjectStyle(histo1275SodiumA, color = kOrange-3, fillalpha = 0.5)
    fit1275SodiumA = TF1("fit1275SodiumA","[0]+[1]/(1+exp(-(-x+[2])/[3]))",950,1150)
    fit1275SodiumA.SetParNames("bkg","a","x0","b")
    fit1275SodiumA.SetParameters(400,300,1075,10)
    histo1275SodiumA.Draw('hist,same')
    histo1275SodiumA.Fit(fit1275SodiumA,'LR')
    fit1275SodiumA.Draw("same")
    erroredge = GetErrorMassPlusCalibrationA(fit1275SodiumA.GetParameter(2),fit1275SodiumA.GetParameter(3))
    print(erroredge)
    print(GetElectronMass(fit1275SodiumA.GetParameter(2),erroredge,1275))
    text2 = TLatex(0.2, 0.80,f"Electron mass: ({round(GetElectronMass(fit1275SodiumA.GetParameter(2),erroredge,1275)[0]/100):1d} #pm {round(GetElectronMass(fit1275SodiumA.GetParameter(2),erroredge,1275)[1]/100):1d})#upoint"+ " 10^{2} keV/c^{2}")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.9)
    text2.SetTextFont(42)
    text2.Draw("same")

    hFrame3 = canvas.cd(3).DrawFrame(800,0,1173,1.2e3,"Cobalt, Scintillator A;Energy [keV];Counts")
    hFrame3.SetTitleOffset(1.,"Y")
    hFrame3.GetYaxis().SetMaxDigits(2)
    df1173CobaltA = GetPandas(inFileCobaltA)
    df1173CobaltA = np.asarray(df1173CobaltA[0],'d')
    histo1173CobaltA = TH1D("histo1173CobaltA","histo1173CobaltA",len(energychannels),np.amin(energychannels),np.amax(energychannels))
    histo1173CobaltA.FillN(len(energychannels),energychannels,df1173CobaltA)
    histo1173CobaltA.Rebin(4)
    SetObjectStyle(histo1173CobaltA, color = kAzure+3, fillalpha = 0.5)
    fit1173CobaltA = TF1("fit1173CobaltA","[0]+[1]/(1+exp(-(-x+[2])/[3]))",875,1000)
    SetObjectStyle(fit1173CobaltA, color = kGreen)
    fit1173CobaltA.SetParNames("bkg","a","x0","b")
    fit1173CobaltA.SetParameters(300,100,950,10)
    histo1173CobaltA.Draw('hist,same')
    histo1173CobaltA.Fit(fit1173CobaltA,'LR')
    fit1173CobaltA.Draw("same")
    erroredge = GetErrorMassPlusCalibrationA(fit1173CobaltA.GetParameter(2),fit1173CobaltA.GetParameter(3))
    print(erroredge)
    print(GetElectronMass(fit1173CobaltA.GetParameter(2),erroredge,1173))
    text3 = TLatex(0.2, 0.80,f"Electron mass: ({round(GetElectronMass(fit1173CobaltA.GetParameter(2),erroredge,1173)[0]/100):1d} #pm {round(GetElectronMass(fit1173CobaltA.GetParameter(2),erroredge,1173)[1]/100):1d})#upoint"+ " 10^{2} keV/c^{2}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.9)
    text3.SetTextFont(42)
    text3.Draw("same")

    hFrame4 = canvas.cd(4).DrawFrame(150,0.1,500,7.e3,"Sodium, Scintillator B;Energy [keV];Counts")
    hFrame4.SetTitleOffset(1.,"Y")
    hFrame4.GetYaxis().SetMaxDigits(2)
    #gPad.SetLogy()
    df511SodiumB = GetPandas(inFileSodiumB)
    df511SodiumB = np.asarray(df511SodiumB[0],'d')

    energychannels = []
    for idx, counts in enumerate(df511SodiumB):
        energychannels.append(GetEnergyFromChnB(idx)[0])
    energychannels = np.asarray(energychannels, 'd')
    print(energychannels)
    
    histo511SodiumB = TH1D("histo511SodiumB","histo511SodiumB",len(energychannels),np.amin(energychannels),np.amax(energychannels))
    histo511SodiumB.FillN(len(energychannels),energychannels,df511SodiumB)
    histo511SodiumB.Rebin(4)
    SetObjectStyle(histo511SodiumB, color = kOrange-3, fillalpha = 0.5)
    fit511SodiumB = TF1("fit511SodiumB","[0]+[1]/(1+exp(-(-x+[2])/[3]))",275,450)
    fit511SodiumB.SetParNames("bkg","a","x0","b")
    fit511SodiumB.SetParameters(1000,4000,340,10)
    histo511SodiumB.Draw('hist,same')
    histo511SodiumB.Fit(fit511SodiumB,'LR')
    fit511SodiumB.Draw("same")
    erroredge = GetErrorMassPlusCalibrationB(fit511SodiumB.GetParameter(2),fit511SodiumB.GetParameter(3))
    print(erroredge)
    print(GetElectronMass(fit511SodiumB.GetParameter(2),erroredge,511))
    text4 = TLatex(0.2, 0.80,f"Electron mass: ({round(GetElectronMass(fit511SodiumB.GetParameter(2),erroredge,511)[0]/100):1d} #pm {round(GetElectronMass(fit511SodiumB.GetParameter(2),erroredge,511)[1]/100):1d})#upoint"+ " 10^{2} keV/c^{2}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.9)
    text4.SetTextFont(42)
    text4.Draw("same")

    hFrame5 = canvas.cd(5).DrawFrame(800,0,1275,1.6e3,"Sodium, Scintillator B;Energy [keV];Counts")
    hFrame5.SetTitleOffset(1.,"Y")
    hFrame5.GetYaxis().SetMaxDigits(2)
    df1275SodiumB = GetPandas(inFileSodiumB)
    df1275SodiumB = np.asarray(df1275SodiumB[0],'d')
    histo1275SodiumB = TH1D("histo1275SodiumB","histo1275SodiumB",len(energychannels),np.amin(energychannels),np.amax(energychannels))
    histo1275SodiumB.FillN(len(energychannels),energychannels,df1275SodiumB)
    histo1275SodiumB.Rebin(4)
    SetObjectStyle(histo1275SodiumB, color = kOrange-3, fillalpha = 0.5)
    fit1275SodiumB = TF1("fit1275SodiumB","[0]+[1]/(1+exp(-(-x+[2])/[3]))",950,1150)
    fit1275SodiumB.SetParNames("bkg","a","x0","b")
    fit1275SodiumB.SetParameters(400,300,1075,10)
    histo1275SodiumB.Draw('hist,same')
    histo1275SodiumB.Fit(fit1275SodiumB,'LR')
    fit1275SodiumB.Draw("same")
    erroredge = GetErrorMassPlusCalibrationB(fit1275SodiumB.GetParameter(2),fit1275SodiumB.GetParameter(3))
    print(erroredge)
    print(GetElectronMass(fit1275SodiumB.GetParameter(2),erroredge,1275))
    text5 = TLatex(0.2, 0.80,f"Electron mass: ({round(GetElectronMass(fit1275SodiumB.GetParameter(2),erroredge,1275)[0]/100):1d} #pm {round(GetElectronMass(fit1275SodiumB.GetParameter(2),erroredge,1275)[1]/100):1d})#upoint"+ " 10^{2} keV/c^{2}")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize()*0.9)
    text5.SetTextFont(42)
    text5.Draw("same")

    hFrame6 = canvas.cd(6).DrawFrame(800,0,1173,1.2e3,"Cobalt, Scintillator B;Energy [keV];Counts")
    hFrame6.SetTitleOffset(1.,"Y")
    hFrame6.GetYaxis().SetMaxDigits(2)
    df1173CobaltB = GetPandas(inFileCobaltB)
    df1173CobaltB = np.asarray(df1173CobaltB[0],'d')
    histo1173CobaltB = TH1D("histo1173CobaltB","histo1173CobaltB",len(energychannels),np.amin(energychannels),np.amax(energychannels))
    histo1173CobaltB.FillN(len(energychannels),energychannels,df1173CobaltB)
    histo1173CobaltB.Rebin(4)
    SetObjectStyle(histo1173CobaltB, color = kAzure+3, fillalpha = 0.5)
    fit1173CobaltB = TF1("fit1173CobaltB","[0]+[1]/(1+exp(-(-x+[2])/[3]))",875,1000)
    SetObjectStyle(fit1173CobaltB, color = kGreen)
    fit1173CobaltB.SetParNames("bkg","a","x0","b")
    fit1173CobaltB.SetParameters(300,100,950,10)
    histo1173CobaltB.Draw('hist,same')
    histo1173CobaltB.Fit(fit1173CobaltB,'LR')
    fit1173CobaltB.Draw("same")
    erroredge = GetErrorMassPlusCalibrationB(fit1173CobaltB.GetParameter(2),fit1173CobaltB.GetParameter(3))
    print(erroredge)
    print(GetElectronMass(fit1173CobaltB.GetParameter(2),erroredge,1173))
    text6 = TLatex(0.2, 0.80,f"Electron mass: ({round(GetElectronMass(fit1173CobaltB.GetParameter(2),erroredge,1173)[0]/100):1d} #pm {round(GetElectronMass(fit1173CobaltB.GetParameter(2),erroredge,1173)[1]/100):1d})#upoint"+ " 10^{2} keV/c^{2}")
    text6.SetNDC()
    text6.SetTextSize(gStyle.GetTextSize()*0.9)
    text6.SetTextFont(42)
    text6.Draw("same")

    electronMass = GetElectronMass(fit511SodiumA.GetParameter(2),erroredge,511)[0] + GetElectronMass(fit1275SodiumA.GetParameter(2),erroredge,1275)[0]
    electronMass += GetElectronMass(fit1173CobaltA.GetParameter(2),erroredge,1173)[0] 
    electronMass += GetElectronMass(fit511SodiumB.GetParameter(2),erroredge,511)[0]
    electronMass += GetElectronMass(fit1275SodiumB.GetParameter(2),erroredge,1275)[0]
    electronMass += GetElectronMass(fit1173CobaltB.GetParameter(2),erroredge,1173)[0] 

    electronMass/=6

    error = GetElectronMass(fit511SodiumA.GetParameter(2),erroredge,511)[1] + GetElectronMass(fit1275SodiumA.GetParameter(2),erroredge,1275)[1]
    error += GetElectronMass(fit1173CobaltA.GetParameter(2),erroredge,1173)[1] 
    error += GetElectronMass(fit511SodiumB.GetParameter(2),erroredge,511)[1]
    error += GetElectronMass(fit1275SodiumB.GetParameter(2),erroredge,1275)[1]
    error += GetElectronMass(fit1173CobaltB.GetParameter(2),erroredge,1173)[1] 

    error/=36

    print(electronMass, error)

    canvas.SaveAs('/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/data/output/Figures/GammaCoincidence/ElectronMass.pdf')