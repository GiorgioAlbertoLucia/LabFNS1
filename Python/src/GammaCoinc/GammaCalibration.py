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
    berr = 19.49
    cov = -0.34

    E = (Channel - b)/a
    Eerr = berr*berr/((Channel - b)*(Channel - b))
    Eerr += aerr*aerr/a/a
    Eerr -= 2*cov/a/(Channel-b)
    Eerr = E * sqrt(Eerr)
    return E, Eerr

def GetEnergyFromChnB(Channel):
    a = 0.68
    b = 23.01
    aerr = 0.02
    berr = 21.31
    cov = -0.4

    E = (Channel - b)/a
    Eerr = berr*berr/((Channel - b)*(Channel - b))
    Eerr += aerr*aerr/a/a
    Eerr -= 2*cov/a/(Channel-b)
    Eerr = E * sqrt(Eerr)
    return E, Eerr

def GetChnFromEnergyA(E):
    a = 0.61
    b = 25.8

    Channel = a*E + b
    return Channel

def GetChnFromEnergyB(E):
    a = 0.68
    b = 23.01

    Channel = a*E + b
    return Channel

def GetParametersA():
    return 0.61, 25.8

def GetParametersErrorA():
    return 0.02, 19.49

def GetParametersErrorB():
    return 0.02, 21.31

def GetParametersB():
    return 0.68, 23.01

def GetResolutionFromChnA(Channel):
    A = 0.79
    B = -0.0108
    E, _ = GetEnergyFromChnA(Channel)
    return A*sqrt(E) + B*E

def GetResolutionFromChnB(Channel):
    A = 0.95
    B = -0.0142
    E, _ = GetEnergyFromChnB(Channel)
    return A*sqrt(E) + B*E

def GetCalibrationFitA(mus,sigmas):
    #mu = [channel(Soudium 511keV), channel(Sodium 1275keV), channel(Cobalt 1173keV), channel(Cobalt 1333keV)]    
    decayenergies=[510.998950,1275,1173.2,1332.5]
    graph = TGraphErrors(len(decayenergies),np.asarray(decayenergies,'d'),np.asarray(mus,'d'),np.asarray([1.e-6,1,0.1,0,1],'d'),np.asarray(sigmas,'d'))
    calibrationfit = TF1("calibrationfitA",'pol1',0,2000)
    fitResults = graph.Fit(calibrationfit, 'S')
    covMatrix = fitResults.GetCovarianceMatrix()
    covMatrix.Print()
    canvas = TCanvas("CalibrationFitA","CalibrationFitA",1300,1500)
    canvas.SetLeftMargin(0.13)
    hFrame = canvas.DrawFrame(400,250,1500,1000,"Calibration fit scintillator A;E [keV];Channel")
    hFrame.GetYaxis().SetTitleOffset(1.2)
    SetObjectStyle(graph,color=kAzure+3,markerstyle=kFullCircle)
    graph.Draw("P,same")
    calibrationfit.Draw("same")


    text2 =TLatex(0.2, 0.8,"Channel = E (keV) #times a + b")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize())
    text2.SetTextFont(42)
    text2.Draw("same")
    text3 =TLatex(0.2, 0.72,"a = ({0:.2f} #pm {1:.2f}) keV".format(calibrationfit.GetParameter(1),calibrationfit.GetParError(1))+"^{#font[122]{-}1}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize())
    text3.SetTextFont(42)
    text3.Draw("same")
    text4 =TLatex(0.2, 0.64,f"b = ({round(calibrationfit.GetParameter(0)/10):1d} #pm {round(calibrationfit.GetParError(0)/10):d})"+" #upoint 10^{1}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize())
    text4.SetTextFont(42)
    text4.Draw("same")
    text5 =TLatex(0.2, 0.56,f"cov(a,b) = {covMatrix[0][1]:.2f}")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize())
    text5.SetTextFont(42)
    text5.Draw("same")

    canvas.SaveAs("data/output/Figures/GammaCoincidence/CalibrationFitA.pdf")

def GetCalibrationFitB(mus,sigmas):
    #mu = [channel(Soudium 511keV), channel(Sodium 1275keV), channel(Cobalt 1173keV), channel(Cobalt 1333keV)]    
    decayenergies=[510.998950,1275,1173.2,1332.5]
    graph = TGraphErrors(len(decayenergies),np.asarray(decayenergies,'d'),np.asarray(mus,'d'),np.asarray([1.e-6,1,0.1,0.1],'d'),np.asarray(sigmas,'d'))
    calibrationfit = TF1("calibrationfitB",'pol1',0,2000)
    fitResults = graph.Fit(calibrationfit, 'S')
    covMatrix = fitResults.GetCovarianceMatrix()
    covMatrix.Print()
    canvas = TCanvas("CalibrationFitB","CalibrationFitB",1300,1500)
    canvas.SetLeftMargin(0.13)
    hFrame = canvas.DrawFrame(400,250,1500,1000,"Calibration fit scintillator B;E [keV];Channel")
    hFrame.GetYaxis().SetTitleOffset(1.2)
    SetObjectStyle(graph,color=kAzure+3,markerstyle=kFullCircle)
    graph.Draw("P,same")
    calibrationfit.Draw("same")

    text2 =TLatex(0.2, 0.8,"Channel = E (keV) #times a + b")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize())
    text2.SetTextFont(42)
    text2.Draw("same")
    text3 =TLatex(0.2, 0.72,"a = ({0:.2f} #pm {1:.2f}) keV".format(calibrationfit.GetParameter(1),calibrationfit.GetParError(1))+"^{#font[122]{-}1}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize())
    text3.SetTextFont(42)
    text3.Draw("same")
    text4 =TLatex(0.2, 0.64,f"b = ({round(calibrationfit.GetParameter(0)/10):1d} #pm {round(calibrationfit.GetParError(0)/10):d})"+" #upoint 10^{1}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize())
    text4.SetTextFont(42)
    text4.Draw("same")
    text5 =TLatex(0.2, 0.56,f"cov(a,b) = {covMatrix[0][1]:.2f}")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize())
    text5.SetTextFont(42)
    text5.Draw("same")

    canvas.SaveAs("data/output/Figures/GammaCoincidence/CalibrationFitB.pdf")

def GetResolutionFitA(decayenergies, errdecays, sigmas, errsigmas):
    #sigmas = [width(Soudium 511keV), width(Sodium 1275keV), width(Cobalt 1173keV), width(Cobalt 1333keV)]    
    #decayenergies=[510.998950,1275,1173.2,1332.5]
    #errdecays = np.asarray([1.e-6,1,0.1,0.1],'d')
    sigmas = np.asarray(sigmas,'d')
    decayenergies = np.asarray(decayenergies,'d')
    errdecays = np.asarray(errdecays,'d')
    Res = sigmas/decayenergies 
    errsigmas = np.asarray(errsigmas,'d')
    print(errdecays)
    errRes = Res * np.sqrt(np.square(errdecays/decayenergies) + np.square(errsigmas/sigmas))
    graph = TGraphErrors(len(decayenergies),decayenergies,Res,errdecays,errRes)
    resolutionfit = TF1("resolutionfitA",'[0]+[1]/sqrt(x)',0,2000)
    resolutionfit.SetParameters(1,0.1)
    graph.Fit(resolutionfit)
    canvas = TCanvas("ResolutionFitA","ResolutionFitA",1200,1500)
    canvas.SetLeftMargin(0.12)
    hFrame = canvas.DrawFrame(450,0,1500,0.05,"Resolution Fit;E [keV];Resolution")
    hFrame.GetYaxis().SetTitleOffset(1.1)
    hFrame.GetYaxis().SetMaxDigits(2)
    SetObjectStyle(graph,color=kAzure+3,markerstyle=kFullCircle,markersize = 2)
    resolutionfit.Draw("same")
    graph.Draw("PZ,same")

    text = TLatex(0.35, 0.80,"Resolution fit scintillator A")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw("same")
    text2 =TLatex(0.35, 0.72,"#frac{#sigma_{E}}{E} = #frac{A}{#sqrt{E (keV)}} + B")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.8)
    text2.SetTextFont(42)
    text2.Draw("same")
    text3 =TLatex(0.35, 0.64,"A = ({0:.2f} #pm {1:.2f}) keV".format(resolutionfit.GetParameter(1),resolutionfit.GetParError(1))+"^{1/2}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw("same")
    text4 =TLatex(0.35, 0.58,f"B = {resolutionfit.GetParameter(0):.4f} #pm {resolutionfit.GetParError(0):.4f}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw("same")

    canvas.SaveAs("data/output/Figures/GammaCoincidence/ResolutionFitA.pdf")

def GetResolutionFitB(decayenergies, errdecays, sigmas, errsigmas):
    #sigmas = [width(Soudium 511keV), width(Sodium 1275keV), width(Cobalt 1173keV), width(Cobalt 1333keV)]    
    #decayenergies=[510.998950,1275,1173.2,1332.5]
    #errdecays = np.asarray([1.e-6,1,0.1,0.1],'d')
    sigmas = np.asarray(sigmas,'d')
    decayenergies = np.asarray(decayenergies,'d')
    errdecays = np.asarray(errdecays,'d')
    Res = sigmas/decayenergies 
    errsigmas = np.asarray(errsigmas,'d')
    print(errdecays)
    errRes = Res * np.sqrt(np.square(errdecays/decayenergies) + np.square(errsigmas/sigmas))
    graph = TGraphErrors(len(decayenergies),decayenergies,Res,errdecays,errRes)
    resolutionfit = TF1("resolutionfitB",'[0]+[1]/sqrt(x)',0,2000)
    resolutionfit.SetParameters(1,0.1)
    graph.Fit(resolutionfit)
    canvas = TCanvas("ResolutionFitB","ResolutionFitB",1200,1500)
    canvas.SetLeftMargin(0.12)
    hFrame = canvas.DrawFrame(450,0,1500,0.05,"Resolution Fit;E [keV];Resolution")
    hFrame.GetYaxis().SetTitleOffset(1.1)
    hFrame.GetYaxis().SetMaxDigits(2)
    SetObjectStyle(graph,color=kAzure+3,markerstyle=kFullCircle,markersize = 2)
    resolutionfit.Draw("same")
    graph.Draw("PZ,same")

    text = TLatex(0.35, 0.80,"Resolution fit scintillator B")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw("same")
    text2 =TLatex(0.35, 0.72,"#frac{#sigma_{E}}{E} = #frac{A}{#sqrt{E (keV)}} + B")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.8)
    text2.SetTextFont(42)
    text2.Draw("same")
    text3 =TLatex(0.35, 0.64,"A = ({0:.2f} #pm {1:.2f}) keV".format(resolutionfit.GetParameter(1),resolutionfit.GetParError(1))+"^{1/2}")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw("same")
    text4 =TLatex(0.35, 0.58,f"B = {resolutionfit.GetParameter(0):.4f} #pm {resolutionfit.GetParError(0):.4f}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw("same")

    canvas.SaveAs("data/output/Figures/GammaCoincidence/ResolutionFitB.pdf")

def CalibrateA(inFileCobaltA, inFileSodiumA):
    histoCobaltA = CreateHist(inFileCobaltA,0)
    histoCobaltA.SetName("histoCobaltA")
    histoSodiumA = CreateHist(inFileSodiumA,1)
    histoSodiumA.SetName("histoSodiumA")
    fSodiumA1 = TF1("fSodiumA","[0]+gaus(1)",300,370)
    fSodiumA2 = TF1("fSodiumA","[0]+gaus(1)",700,900)
    fCobaltA1 = TF1("fCobaltA","[0]+gaus(1)",700,780)
    fCobaltA2 = TF1("fCobaltA","[0]+gaus(1)",780,910)
    fSodiumA1.SetNpx(1000)
    fSodiumA2.SetNpx(1000)
    fCobaltA1.SetNpx(1000)
    fCobaltA2.SetNpx(1000)
    fSodiumA1.SetParameters(1.e-4,0.009,350,20)
    fSodiumA2.SetParameters(1.e-4,0.0009,800,15)
    fCobaltA1.SetParameters(1.e-4,0.002,750,10)
    fCobaltA2.SetParameters(1.e-4,0.002,850,10)
    SetObjectStyle(histoSodiumA, color = kOrange-3, fillalpha = 0.5)
    SetObjectStyle(fSodiumA1, color = kRed, linewidth=3)
    SetObjectStyle(fSodiumA2, color = kRed, linewidth=3)
    SetObjectStyle(histoCobaltA, color = kAzure+3, fillalpha = 0.5)
    SetObjectStyle(fCobaltA1, color = kGreen, linewidth=3)
    SetObjectStyle(fCobaltA2, color = kGreen, linewidth=3)
    canvasA = TCanvas("canvasA","canvasA",1000,1000)
    canvasA.SetLeftMargin(0.11)
    hFrameA = canvasA.DrawFrame(0,0,1024,0.01,"Calibration scintillator A;Channel;Counts [a.u.]")
    hFrameA.SetTitleOffset(1.,"Y")
    hFrameA.GetYaxis().SetMaxDigits(2)
    histoSodiumA = histoSodiumA.DrawNormalized('hist,same')
    histoCobaltA = histoCobaltA.DrawNormalized('hist,same')
    histoSodiumA.Fit(fSodiumA1,'R')
    histoSodiumA.Fit(fSodiumA2,'R')
    histoCobaltA.Fit(fCobaltA1,'R')
    histoCobaltA.Fit(fCobaltA2,'R')
    fSodiumA1.Draw('same')
    fSodiumA2.Draw('same')
    fCobaltA1.Draw('same')
    fCobaltA2.Draw('same')
    leg = TLegend(0.565, 0.80, 0.85, 0.68)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("SG Normalised counts")
    leg.AddEntry(histoSodiumA, 'Sodium spectrum', 'f')
    leg.AddEntry(histoCobaltA, 'Cobalt spectrum', 'f')
    leg.Draw("same")
    canvasA.SaveAs("data/output/Figures/GammaCoincidence/CalibrationA.pdf")
    GetCalibrationFitA([fSodiumA1.GetParameter(2),fSodiumA2.GetParameter(2),fCobaltA1.GetParameter(2),fCobaltA2.GetParameter(2)],
                       [fSodiumA1.GetParameter(3),fSodiumA2.GetParameter(3),fCobaltA1.GetParameter(3),fCobaltA2.GetParameter(3)])
    E511, sigma511 = GetEnergyFromChnA(fSodiumA1.GetParameter(2))
    E1275, sigma1275 = GetEnergyFromChnA(fSodiumA2.GetParameter(2))
    E1173, sigma1173 = GetEnergyFromChnA(fCobaltA1.GetParameter(2))
    E1332, sigma1332 = GetEnergyFromChnA(fCobaltA2.GetParameter(2))
    GetResolutionFitA([E511, E1275, E1173, E1332],
                      [sigma511,sigma1275,sigma1173,sigma1332],
                      [fSodiumA1.GetParameter(3),fSodiumA2.GetParameter(3),fCobaltA1.GetParameter(3),fCobaltA2.GetParameter(3)],
                      [fSodiumA1.GetParError(3),fSodiumA2.GetParError(3),fCobaltA1.GetParError(3),fCobaltA2.GetParError(3)])
    
def CalibrateB(inFileCobaltB, inFileSodiumB):
    histoCobaltB = CreateHist(inFileCobaltB,0)
    histoCobaltB.SetName("histoCobaltB")
    histoSodiumB = CreateHist(inFileSodiumB,1)
    histoSodiumB.SetName("histoSodiumB")
    fSodiumB1 = TF1("fSodiumB","[0]+gaus(1)",340,420)
    fSodiumB2 = TF1("fSodiumB","[0]+gaus(1)",830,950)
    fCobaltB1 = TF1("fCobaltB","[0]+gaus(1)",780,880)
    fCobaltB2 = TF1("fCobaltB","[0]+gaus(1)",880,1000)
    fSodiumB1.SetParameters(5.e-4,0.009,380,15)
    fSodiumB2.SetParameters(5.e-4,0.0009,900,15)
    fCobaltB1.SetParameters(5.e-4,0.002,825,15)
    fCobaltB2.SetParameters(5.e-4,0.002,950,15)
    #fSodiumB.SetParameters(500,3000,400,15,500,900,15)
    #fCobaltB.SetParameters(20,200,825,15,200,900,15)
    fSodiumB1.SetNpx(1000)
    fSodiumB2.SetNpx(1000)
    fCobaltB1.SetNpx(1000)
    fCobaltB2.SetNpx(1000)
    SetObjectStyle(histoSodiumB, color = kOrange-3, fillalpha = 0.5)
    SetObjectStyle(fSodiumB1, color = kRed, linewidth=3)
    SetObjectStyle(fSodiumB2, color = kRed, linewidth=3)
    SetObjectStyle(histoCobaltB, color = kAzure+3, fillalpha = 0.5)
    SetObjectStyle(fCobaltB1, color = kGreen, linewidth=3)
    SetObjectStyle(fCobaltB2, color = kGreen, linewidth=3)
    canvasB = TCanvas("canvasB","canvasB",1000,1000)
    canvasB.SetLeftMargin(0.11)
    hFrameB = canvasB.DrawFrame(0,0,1024,0.01,"Calibration scintillator B;Channel;Counts [a.u.]")
    hFrameB.SetTitleOffset(1.,"Y")
    hFrameB.GetYaxis().SetMaxDigits(2)
    histoSodiumB = histoSodiumB.DrawNormalized('hist,same')
    histoCobaltB = histoCobaltB.DrawNormalized('hist,same')
    histoSodiumB.Fit(fSodiumB1,'R')
    histoSodiumB.Fit(fSodiumB2,'R')
    histoCobaltB.Fit(fCobaltB1,'R')
    histoCobaltB.Fit(fCobaltB2,'R')
    fSodiumB1.Draw('same')
    fSodiumB2.Draw('same')
    fCobaltB1.Draw('same')
    fCobaltB2.Draw('same')
    leg = TLegend(0.565, 0.80, 0.85, 0.68)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("SG Normalised counts")
    leg.AddEntry(histoSodiumB, 'Sodium spectrum', 'f')
    leg.AddEntry(histoCobaltB, 'Cobalt spectrum', 'f')
    leg.Draw("same")
    canvasB.SaveAs("data/output/Figures/GammaCoincidence/CalibrationB.pdf")
    GetCalibrationFitB([fSodiumB1.GetParameter(2),fSodiumB2.GetParameter(2),fCobaltB1.GetParameter(2),fCobaltB2.GetParameter(2)],
                       [fSodiumB1.GetParameter(3),fSodiumB2.GetParameter(3),fCobaltB1.GetParameter(3),fCobaltB2.GetParameter(3)])
    E511, sigma511 = GetEnergyFromChnB(fSodiumB1.GetParameter(2))
    E1275, sigma1275 = GetEnergyFromChnB(fSodiumB2.GetParameter(2))
    E1173, sigma1173 = GetEnergyFromChnB(fCobaltB1.GetParameter(2))
    E1332, sigma1332 = GetEnergyFromChnB(fCobaltB2.GetParameter(2))
    GetResolutionFitB([E511, E1275, E1173, E1332],
                      [sigma511,sigma1275,sigma1173,sigma1332],
                      [fSodiumB1.GetParameter(3),fSodiumB2.GetParameter(3),fCobaltB1.GetParameter(3),fCobaltB2.GetParameter(3)],
                      [fSodiumB1.GetParError(3),fSodiumB2.GetParError(3),fCobaltB1.GetParError(3),fCobaltB2.GetParError(3)])
    
if __name__ == '__main__':

    inFileCobaltA = 'data/input/Gamma/CobaltocalibrazioneA.mca'
    inFileSodiumA = 'data/input/Gamma/SodiocalibrazioneA.mca'
    inFileCobaltB = 'data/input/Gamma/CobaltocalibrazioneB.mca'
    inFileSodiumB = 'data/input/Gamma/SodiocalibrazioneB.mca'

    CalibrateA(inFileCobaltA,inFileSodiumA)
    CalibrateB(inFileCobaltB,inFileSodiumB)




