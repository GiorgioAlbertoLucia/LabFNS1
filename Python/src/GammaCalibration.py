import sys
sys.path.append('Python/utils')
import numpy as np

from ReadMCA import CreateHist
from ROOT import TCanvas, TPad, TGraphErrors, TFile, TLatex, TLegend, TF1, TArrow, kAzure, kOrange, kRed, kBlue, kGreen, kFullCircle, gStyle
from StyleFormatter import SetObjectStyle, SetGlobalStyle 
from math import sqrt

SetGlobalStyle(padleftmargin=0.1, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1., titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

def GetEnergyFromChnA(Channel):
    a = 0.61
    b = 25.8
    aerr = 0.02
    berr = 19.87
    cov = -0.35

    E = (Channel - b)/a
    Eerr = berr*berr/(Channel*Channel)
    Eerr += aerr*aerr/a/a
    Eerr += 2*cov/a/(Channel-b)
    Eerr = E * sqrt(Eerr)
    return E, Eerr

def GetEnergyFromChnB(Channel):
    a = 0.68
    b = 23.01
    aerr = 0.02
    berr = 21.31
    cov = -0.4

    E = (Channel - b)/a
    Eerr = berr*berr/(Channel*Channel)
    Eerr += aerr*aerr/a/a
    Eerr += 2*cov/a/(Channel-b)
    Eerr = E * sqrt(Eerr)
    return E, Eerr

def GetCalibrationFitA(mus,sigmas):
    #mu = [channel(Soudium 511keV), channel(Sodium 1275keV), channel(Cobalt 1173keV), channel(Cobalt 1333keV)]    
    decayenergies=[510.998950,1275,1173.2,1332.5]
    graph = TGraphErrors(len(decayenergies),np.asarray(decayenergies,'d'),np.asarray(mus,'d'),np.asarray([1.e-6,1,0.1,0,1],'d'),np.asarray(sigmas,'d'))
    calibrationfit = TF1("calibrationfitA",'pol1',0,2000)
    fitResults = graph.Fit(calibrationfit, 'S')
    covMatrix = fitResults.GetCovarianceMatrix()
    covMatrix.Print()
    canvas = TCanvas("CalibrationFitA","CalibrationFitA",1500,1500)
    hFrame = canvas.DrawFrame(400,250,1500,1000,"Calibration Fit;E [keV];Channel")
    SetObjectStyle(graph,color=kAzure+3,markerstyle=kFullCircle)
    graph.Draw("P,same")
    calibrationfit.Draw("same")

    text = TLatex(0.15, 0.80,"Calibration fit scintillator A")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw("same")
    text2 =TLatex(0.15, 0.74,"Channel = E (keV) #times a + b")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.8)
    text2.SetTextFont(42)
    text2.Draw("same")
    text3 =TLatex(0.15, 0.68,"a = ({0:.2f} #pm {1:.2f}) keV".format(calibrationfit.GetParameter(1),calibrationfit.GetParError(1))+"^{#font[122]{-}1}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw("same")
    text4 =TLatex(0.15, 0.62,f"b = {calibrationfit.GetParameter(0):.2f} #pm {calibrationfit.GetParError(0):.2f}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw("same")
    text5 =TLatex(0.15, 0.56,f"cov(a,b) = {covMatrix[0][1]:.2f}")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize()*0.7)
    text5.SetTextFont(42)
    text5.Draw("same")

    canvas.SaveAs("data/output/Figures/GammaCoincidence/CalibrationFitA.pdf")

def GetCalibrationFitB(mus,sigmas):
    #mu = [channel(Soudium 511keV), channel(Sodium 1275keV), channel(Cobalt 1173keV), channel(Cobalt 1333keV)]    
    decayenergies=[510.998950,1275,1173.2,1332.5]
    graph = TGraphErrors(len(decayenergies),np.asarray(decayenergies,'d'),np.asarray(mus,'d'),np.asarray([1.e-6,1,0.1,0,1],'d'),np.asarray(sigmas,'d'))
    calibrationfit = TF1("calibrationfitB",'pol1',0,2000)
    fitResults = graph.Fit(calibrationfit, 'S')
    covMatrix = fitResults.GetCovarianceMatrix()
    covMatrix.Print()
    canvas = TCanvas("CalibrationFitB","CalibrationFitB",1500,1500)
    hFrame = canvas.DrawFrame(400,250,1500,1000,"Calibration Fit;E [keV];Channel")
    SetObjectStyle(graph,color=kAzure+3,markerstyle=kFullCircle)
    graph.Draw("P,same")
    calibrationfit.Draw("same")

    text = TLatex(0.15, 0.80,"Calibration fit scintillator B")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw("same")
    text2 =TLatex(0.15, 0.74,"Channel = E (keV) #times a + b")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.8)
    text2.SetTextFont(42)
    text2.Draw("same")
    text3 =TLatex(0.15, 0.68,"a = ({0:.2f} #pm {1:.2f}) keV".format(calibrationfit.GetParameter(1),calibrationfit.GetParError(1))+"^{#font[122]{-}1}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw("same")
    text4 =TLatex(0.15, 0.62,f"b = {calibrationfit.GetParameter(0):.2f} #pm {calibrationfit.GetParError(0):.2f}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw("same")
    text5 =TLatex(0.15, 0.56,f"cov(a,b) = {covMatrix[0][1]:.2f}")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize()*0.7)
    text5.SetTextFont(42)
    text5.Draw("same")

    canvas.SaveAs("data/output/Figures/GammaCoincidence/CalibrationFitB.pdf")

def CalibrateA(inFileCobaltA, inFileSodiumA):
    histoCobaltA = CreateHist(inFileCobaltA,0)
    histoCobaltA.SetName("histoCobaltA")
    histoSodiumA = CreateHist(inFileSodiumA,1)
    histoSodiumA.SetName("histoSodiumA")
    fSodiumA = TF1("fSodiumA","[0]+gaus(1)+gaus(4)",250,1024)
    fCobaltA = TF1("fCobaltA","[0]+gaus(1)+gaus(4)",650,950)
    fSodiumA.SetNpx(1000)
    fCobaltA.SetNpx(1000)
    fSodiumA.SetParameters(100,3000,400,20,500,800,20)
    fCobaltA.SetParameters(20,200,750,20,200,850,20)
    SetObjectStyle(histoSodiumA, color = kOrange-3, fillalpha = 0.5)
    SetObjectStyle(fSodiumA, color = kRed, linewidth=3)
    SetObjectStyle(histoCobaltA, color = kAzure+3, fillalpha = 0.5)
    SetObjectStyle(fCobaltA, color = kGreen, linewidth=3)
    histoSodiumA.Fit(fSodiumA,'LR')
    histoCobaltA.Fit(fCobaltA,'LR')
    canvasA = TCanvas("canvasA","canvasA",1000,1000)
    canvasA.SetLeftMargin(0.14)
    hFrameA = canvasA.DrawFrame(0,0,1024,3.5e3,"Calibration scintillator A;Channel;Counts")
    hFrameA.SetTitleOffset(1.45,"Y")
    histoSodiumA.Draw('hist,same')
    histoCobaltA.Draw('hist,same')
    fSodiumA.Draw('same')
    fCobaltA.Draw('same')
    leg = TLegend(0.565, 0.80, 0.85, 0.68)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("SG Normalised counts")
    leg.AddEntry(histoSodiumA, 'Sodium spectrum', 'f')
    leg.AddEntry(histoCobaltA, 'Cobalt spectrum', 'f')
    leg.Draw("same")
    canvasA.SaveAs("data/output/Figures/GammaCoincidence/CalibrationA.pdf")
    GetCalibrationFitA([fSodiumA.GetParameter(2),fSodiumA.GetParameter(5),fCobaltA.GetParameter(2),fCobaltA.GetParameter(5)],
                       [fSodiumA.GetParameter(3),fSodiumA.GetParameter(6),fCobaltA.GetParameter(3),fCobaltA.GetParameter(6)])
    
def CalibrateB(inFileCobaltB, inFileSodiumB):
    histoCobaltB = CreateHist(inFileCobaltB,0)
    histoCobaltB.SetName("histoCobaltB")
    histoSodiumB = CreateHist(inFileSodiumB,1)
    histoSodiumB.SetName("histoSodiumB")
    fSodiumB = TF1("fSodiumB","[0]+gaus(1)+gaus(4)",250,1024)
    fCobaltB = TF1("fCobaltB","[0]+gaus(1)+gaus(4)",750,1024)
    fSodiumB.SetParameters(500,3000,400,15,500,900,15)
    fCobaltB.SetParameters(20,200,825,15,200,900,15)
    fSodiumB.SetNpx(1000)
    fCobaltB.SetNpx(1000)
    SetObjectStyle(histoSodiumB, color = kOrange-3, fillalpha = 0.5)
    SetObjectStyle(fSodiumB, color = kRed, linewidth=3)
    SetObjectStyle(histoCobaltB, color = kAzure+3, fillalpha = 0.5)
    SetObjectStyle(fCobaltB, color = kGreen, linewidth=3)
    histoSodiumB.Fit(fSodiumB,'LR')
    histoCobaltB.Fit(fCobaltB,'LR')
    canvasB = TCanvas("canvasB","canvasB",1000,1000)
    canvasB.SetLeftMargin(0.14)
    hFrameB = canvasB.DrawFrame(0,0,1024,3.5e3,"Calibration scintillator B;Channel;Counts")
    hFrameB.SetTitleOffset(1.45,"Y")
    histoSodiumB.Draw('hist,same')
    histoCobaltB.Draw('hist,same')
    fSodiumB.Draw('same')
    fCobaltB.Draw('same')
    leg = TLegend(0.565, 0.80, 0.85, 0.68)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("SG Normalised counts")
    leg.AddEntry(histoSodiumB, 'Sodium spectrum', 'f')
    leg.AddEntry(histoCobaltB, 'Cobalt spectrum', 'f')
    leg.Draw("same")
    canvasB.SaveAs("data/output/Figures/GammaCoincidence/CalibrationB.pdf")
    GetCalibrationFitB([fSodiumB.GetParameter(2),fSodiumB.GetParameter(5),fCobaltB.GetParameter(2),fCobaltB.GetParameter(5)],
                       [fSodiumB.GetParameter(3),fSodiumB.GetParameter(6),fCobaltB.GetParameter(3),fCobaltB.GetParameter(6)])



if __name__ == '__main__':

    inFileCobaltA = 'data/input/Gamma/CobaltocalibrazioneA.mca'
    inFileSodiumA = 'data/input/Gamma/SodiocalibrazioneA.mca'
    inFileCobaltB = 'data/input/Gamma/CobaltocalibrazioneB.mca'
    inFileSodiumB = 'data/input/Gamma/SodiocalibrazioneB.mca'

    CalibrateA(inFileCobaltA,inFileSodiumA)
    CalibrateB(inFileCobaltB,inFileSodiumB)




