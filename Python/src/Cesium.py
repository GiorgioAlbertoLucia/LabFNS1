import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TLegend, gStyle, TF1, Math, TPad, kYellow, TLine, kGray, gPad 
from ReadMCA import DictHistos, HistoComparison, CalEnergyErr, FitStats

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.14, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.11, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

def InternalConversionPeakFit(histoPeak,calerr,color):
    
    # FIT PICCO CONVERSIONE INTERNA GUADAGNO 1000 - NO BETA ELECTRONS
    InternalConversionPeakFit = TCanvas('Internal conversion peak fit', 'Internal conversion peak fit',1280,760)
    FitLowBound = 630
    FitUppBound = 675
    IntConvPeak = TF1("Internal conversion peak", "gaus(0)", FitLowBound, FitUppBound)
    #IntConvPeak.SetParameter(0,0.9)
    IntConvPeak.SetParameter(1,660)
    histoPeak.Fit(IntConvPeak,"RM+","",FitLowBound,FitUppBound) 
    FitStats(IntConvPeak)
    fitResults = histoPeak.Fit(IntConvPeak, 'S')
    covMatrix = fitResults.GetCovarianceMatrix()
    cov = covMatrix[0][1]
    print('COVARIANZAAAAAAAAAAAAAAAAAAAA')
    print(cov)
    print('\n\n\n\n\n')
    hFrame = InternalConversionPeakFit.DrawFrame(570,0.,770,1500,"Internal conversion peak fit; E[keV]; Counts")
    histoPeak.SetLineColor(color)
    histoPeak.SetMarkerColor(color)
    histoPeak.Draw("hist,p,e,same")
    leg = TLegend(0.71, 0.6, 0.85, 0.8)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    leg.AddEntry(histoPeak, 'Data', 'lep')
    leg.AddEntry(IntConvPeak, 'Fit curve', 'lf')
    leg.Draw("same")
    IntConvPeak.Draw("same")
    InternalConversionPeakFit.Modified()
    InternalConversionPeakFit.Update()
    InternalConversionPeakFit.SaveAs('data/output/Diamond/Cesio/InternalConversionPeakFit.pdf')
    Calerr = CalEnergyErr(0.318,0.008,-30,40,5,cov,IntConvPeak.GetParameter(1),IntConvPeak.GetParError(1))
    print(Calerr)
    print('\n\n\n\n\n\n') 
    TotalError = np.sqrt(IntConvPeak.GetParError(1)*IntConvPeak.GetParError(1) + Calerr*Calerr)
    Polymide = PolymideThickness(IntConvPeak.GetParameter(1),TotalError)
    result = str(IntConvPeak.GetParameter(1)) + ' ' + u"\u00B1" + ' ' + str(TotalError) + ' keV ' + "\n\n" + "Polymide Thickness: " + Polymide
    return result
    #return (IntConvPeak.GetParameter(1),IntConvPeak.GetParError(1))

def PolymideThickness(IntConvPeak, IntConvPeakErr):
    # StopPowerPolyElectronsNIST = 1.769 (MeV*cm2)/(g)
    StopPowerPolyElectronsNIST = 0.1769 # (keV*m2)/(g)
    # SpecificRhoPoly = 1.420 (g/cm3)
    SpecificRhoPoly = 1420000 # g/m3
    # AmbTempRhoWater = 1000 kg/m3
    AmbTempRhoWater = 1000000 # g/m3
    RhoPoly = AmbTempRhoWater*SpecificRhoPoly
    PolyThickness = (662-IntConvPeak)/(RhoPoly*StopPowerPolyElectronsNIST)
    PolyThicknessErr = IntConvPeakErr/(RhoPoly*StopPowerPolyElectronsNIST)
    result = str(PolyThickness) + ' ' + u"\u00B1" + ' ' + str(PolyThicknessErr) + ' m'
    return result

def ComptonEdgeFit(histoCompton,calerr,color):
    #CHI2 SUPERATO
    #FitLowBound = 475
    #FitUppBound = 530
    #ComptonEdgeFunction = TF1("Compton Edge", " [0] / (1+TMath::Exp( - ( x-[1] )/[2] ) ) + TMath::Exp(-[3]*x)", FitLowBound, FitUppBound)   

    #(465, 515)
    # ComptonEdgeFunction.SetParameter(0,2.)
    # ComptonEdgeFunction.SetParameter(1,490)
    # ComptonEdgeFunction.SetParameter(2,6.)
    # ComptonEdgeFunction = TF1("Compton Edge", " [0] / (1+TMath::Exp( - ( x-[1] )/[2] ) )", FitLowBound, FitUppBound)

    #FitLowBound = 455
    #FitUppBound = 540
    #ComptonEdgeFunction = TF1("Compton Edge", " [0] / (1+TMath::Exp( ( x-[1] )/[2] ) ) + [3]", FitLowBound, FitUppBound)
    #ComptonEdgeFunction.SetParameter(0,117)
    #ComptonEdgeFunction.SetParameter(1,495)
    #ComptonEdgeFunction.SetParameter(2,3.)
    #ComptonEdgeFunction.SetParameter(3,3.) Rebin=8

    # FIT COMPTON EDGE ACQUISITION WITH PLASTIC - NO BETA ELECTRONS
    #FileFitEdge = TFile('data/output/Diamond/Cesio/ComptonEdge.root', 'recreate')
    ComptonEdgeFit = TCanvas('Compton Edge Fit', 'Compton Edge Fit',1280,760)
    FitLowBound = 455
    FitUppBound = 540
    ComptonEdgeFunction = TF1("Compton Edge", " [0] / (1+TMath::Exp( ( x-[1] )/[2] ) ) + [3]", FitLowBound, FitUppBound)
    ComptonEdgeFunction.SetParameter(0,60)
    ComptonEdgeFunction.SetParameter(1,495)
    ComptonEdgeFunction.SetParameter(2,3.)
    ComptonEdgeFunction.SetParameter(3,2.)
    histoCompton.Fit(ComptonEdgeFunction,"L","",FitLowBound,FitUppBound) # provare 3° opzione func
    FitStats(ComptonEdgeFunction)
    fitResults = histoCompton.Fit(ComptonEdgeFunction, 'SL')
    covMatrix = fitResults.GetCovarianceMatrix()
    cov = covMatrix[0][1]
    print('COVARIANZAAAAAAAAAAAAAAAAAAAA')
    print(cov)
    print('\n\n\n\n\n')
    hFrame = ComptonEdgeFit.DrawFrame(400,0.,600,220,"Compton Edge Fit; E[keV]; Counts")
    histoCompton.SetLineColor(color)
    histoCompton.SetMarkerColor(color)
    histoCompton.Draw("hist,p,e,same")
    #histoCompton.Write()
    leg = TLegend(0.65, 0.40, 0.85, 0.60)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("TDC Normalised counts")
    leg.AddEntry(histoCompton, 'Data', 'lep')
    leg.AddEntry(ComptonEdgeFunction, 'Fit curve', 'lf')
    leg.Draw("same")
    ComptonEdgeFunction.Draw("same")
    ComptonEdgeFit.Modified()
    ComptonEdgeFit.Update()
    ComptonEdgeFit.SaveAs('data/output/Diamond/Cesio/ComptonEdgeFit.pdf')
    Calerr = CalEnergyErr(0.318,0.008,-30,40,5,cov,ComptonEdgeFunction.GetParameter(1),ComptonEdgeFunction.GetParError(1))
    print(Calerr)
    print('\n\n\n\n\n\n') 
    TotalError = np.sqrt(ComptonEdgeFunction.GetParError(1)*ComptonEdgeFunction.GetParError(1) + Calerr*Calerr)
    result = str(ComptonEdgeFunction.GetParameter(1)) + ' ' + u"\u00B1" + ' ' + str(TotalError) + ' keV'
    return result
    #return (ComptonEdgeFunction.GetParameter(1),ComptonEdgeFunction.GetParError(1),0,0)
    #FileFitEdge.Close()

def BetaQValueFit(histoBeta, outfilename, calerr, color):

    BetaQValueFitFile = TFile('data/output/Diamond/Cesio/BetaEdgeFit.root','recreate')
    BetaQValueFit = TCanvas("Beta Q Value Fit", "Beta Q Value Fit", 1280, 760)

    # FIT AND DRAWING BOUNDARIES REBIN 4
    #FitLowBound1 = 405
    #FitUppBound1 = 490
    #FitLowBound2 = 540
    #FitUppBound2 = 633
    #BoundDrawBetaCurve = 600
    #BoundDrawConstCurve = 490
    #CanvaYAxisBottomBound = 0.
    #CanvaYAxisTopBound = 550.
#
    #BetaCurveFunction = TF1("Beta Curve", "[0] + TMath::Exp(-[1]*(x-[2]) )", FitLowBound1, BoundDrawBetaCurve)
    #BetaCurveFunction.SetParameter(0,40)
    #BetaCurveFunction.SetParameter(1,0.0109)
    #BetaCurveFunction.SetParameter(2,910)
#
    #ConstFunction = TF1("Compton Plateau", "[0]", BoundDrawConstCurve, FitUppBound2)
    #ConstFunction.SetParameter(1,50)
#
    #histoBeta.Fit(BetaCurveFunction,"L","",FitLowBound1,FitUppBound1)
    #histoBeta.Fit(ConstFunction,"L","",FitLowBound2,FitUppBound2)

    # FIT AND DRAWING BOUNDARIES REBIN 8

    FitLowBound1 = 400
    FitUppBound1 = 485
    FitLowBound2 = 525
    FitUppBound2 = 630
    BoundDrawBetaCurve = 580
    BoundDrawConstCurve = 500
    CanvaYAxisBottomBound = 0.
    CanvaYAxisTopBound = 1500.

    BetaCurveFunction = TF1("Beta Curve", "[0] + TMath::Exp(-[1]*(x-[2]) )", 380, BoundDrawBetaCurve)
    BetaCurveFunction.SetParameter(0,40)
    BetaCurveFunction.SetParameter(1,0.0109)
    BetaCurveFunction.SetParameter(2,910)

    ConstFunction = TF1("Compton Plateau", "[0]", BoundDrawConstCurve, 640)
    ConstFunction.SetParameter(1,50)

    histoBeta.Fit(BetaCurveFunction,"L","",FitLowBound1,FitUppBound1)
    print('\n\n\n\n\n\n\n')
    histoBeta.Fit(ConstFunction,"L","",FitLowBound2,FitUppBound2)

    FitStats(ConstFunction)
    FitStats(BetaCurveFunction)

    # DRAW THE GRAPH
    hFrame = BetaQValueFit.DrawFrame(300,CanvaYAxisBottomBound,700,CanvaYAxisTopBound,"Q value Beta Decay Fit; E[keV]; Counts")
    #histoBeta.SetMarkerColor(4)
    histoBeta.SetLineColor(color)
    histoBeta.SetMarkerColor(color)
    histoBeta.Draw("hist,p,e,same")
    BetaCurveFunction.Draw("same")
    BetaCurveFunction.SetLineColor(kGreen) 
    BetaCurveFunction.SetLineWidth(2) 
    ConstFunction.Draw("same")
    ConstFunction.SetLineColor(kViolet)
    ConstFunction.SetLineWidth(2)
    BetaCurveFitLowBound = TLine(FitLowBound1,0.7*gPad.GetUymax(),FitLowBound1,0.17*gPad.GetUymax())
    BetaCurveFitUppBound = TLine(FitUppBound1,0.4*gPad.GetUymax(),FitUppBound1,0.05*gPad.GetUymax())
    BetaCurveFitLowBound.SetLineColor(kRed)
    BetaCurveFitLowBound.SetLineWidth(2)
    BetaCurveFitUppBound.SetLineColor(kRed)
    BetaCurveFitUppBound.SetLineWidth(2)
    ConstCurveFitLowBound = TLine(FitLowBound2,0.25*gPad.GetUymax(),FitLowBound2,gPad.GetUymin())
    ConstCurveFitUppBound = TLine(FitUppBound2,0.25*gPad.GetUymax(),FitUppBound2,gPad.GetUymin())
    ConstCurveFitLowBound.SetLineColor(kRed)
    ConstCurveFitLowBound.SetLineWidth(2)
    ConstCurveFitUppBound.SetLineColor(kRed)
    ConstCurveFitUppBound.SetLineWidth(2)
    BetaCurveFitLowBound.Draw("same")
    BetaCurveFitUppBound.Draw("same")
    ConstCurveFitLowBound.Draw("same")
    ConstCurveFitUppBound.Draw("same")
    legend = TLegend(0.58,0.53,0.83,0.73)
    legend.SetTextFont(42)
    legend.SetTextSize(gStyle.GetTextSize()*0.7)
    legend.SetFillStyle(0)
    legend.AddEntry(histoBeta, 'Data', 'lep')
    legend.AddEntry(BetaCurveFunction, 'Beta Curve Fit', 'lf')
    legend.AddEntry(ConstFunction, 'Plateau Fit', 'lf')
    legend.AddEntry(BetaCurveFitLowBound,'Fit ranges', 'lf')
    legend.Draw("same")
    BetaQValueFit.Modified()
    BetaQValueFit.Update()
    BetaQValueFit.SaveAs('data/output/Diamond/Cesio/'+outfilename+'.pdf')
    BetaQValueFit.Write()
    BetaQValueFitFile.Close()

    # Q-VALUE ESTIMATE
    a0 = BetaCurveFunction.GetParameter(0)
    a1 = BetaCurveFunction.GetParameter(1)
    a2 = BetaCurveFunction.GetParameter(2)
    a3 = ConstFunction.GetParameter(0)
    sa0 = BetaCurveFunction.GetParError(0)
    sa1 = BetaCurveFunction.GetParError(1)
    sa2 = BetaCurveFunction.GetParError(2)
    sa3 = ConstFunction.GetParError(0)
    QValueEstimate = a2-(np.log(a3-a0)/a1)
    print(sa2*sa2)
    print(((np.log(a3-a0)*np.log(a3-a0))/(a1*a1*a1*a1))*sa1*sa1)
    print((sa3*sa3)*(1/(a1*a1*(a3-a0)*(a3-a0))))
    print((sa0*sa0)*(1/(a1*a1*(a3-a0)*(a3-a0))))
    QValueEstimateError = np.sqrt(sa2*sa2 + ((np.log(a3-a0)*np.log(a3-a0))/(a1*a1*a1*a1))*sa1*sa1 + (sa0*sa0+sa3*sa3)*(1/(a1*a1*(a3-a0)*(a3-a0))) )
    TotalError = np.sqrt(QValueEstimateError + calerr*calerr)
    result = str(QValueEstimate) + ' ' + u"\u00B1" + ' ' + str(TotalError) + ' keV'
    return result
    #return (QValueEstimate,QValueEstimateError)

def FitStats(fitfunct):
    Chisquare = fitfunct.GetChisquare()
    Chicrit = Math.chisquared_quantile_c(0.05,fitfunct.GetNDF())
    NDegFreedom = fitfunct.GetNDF()
    Pvalue = fitfunct.GetProb()
    print('Chi Square:', Chisquare, ', Degrees of freedom:', NDegFreedom, ', Critical Chi Square:', Chicrit,', P-value: ', Pvalue)

def HistoSubtraction(DFbound,diffYbound,histo1,histo2,legend,outfilename):
    histo1copy = histo1
    histo2copy = histo2
    SizeLittlePad = 0.3   # size in %
    canvas = TCanvas("Canvas", "Canvas",1000,1000)
    pad = TPad("pad","pad",0.,SizeLittlePad,1.,1.)
    #pad.SetTopMargin(0.)
    pad.SetBottomMargin(0.)
    pad.Draw()
    padDiff = TPad("padDiff","padDiff",0.,0.,1.,SizeLittlePad)
    padDiff.SetTopMargin(0.)
    padDiff.SetBottomMargin(0.3)
    padDiff.Draw()
#
    pad.cd()
    hFrame = pad.DrawFrame(DFbound[0],DFbound[1],DFbound[2],DFbound[3],"MCA normalised counts distribution;Energy [keV];Counts [a.u.]")
    histo1copy.Scale(1/histo1copy.GetMaximum())
    SetObjectStyle(histo1copy, color = kAzure+3, fillalpha=0.5)
    histo1copy.Draw("hist,same")
    histo2copy.Scale(1/histo2copy.GetMaximum())
    SetObjectStyle(histo2copy, color = kOrange-3, fillalpha=0.7)
    histo2copy.Draw("hist,same")
    legend.Draw("same")

    padDiff.cd()
    # DA FARE: SOTTRARRE ISTOGRAMMI NORMALIZZATI ALL'AREA TOTALE
    hFrameDiff = pad.DrawFrame(DFbound[0],DFbound[1],DFbound[2],diffYbound,";Energy [keV];|Difference|")
    histo = histo1copy.Clone()
    histo.Add(histo2copy,-1.)      # Performs subtraction
    SetObjectStyle(histo, color = kRed, fillalpha=0.5)

    hFrameDiff.GetYaxis().SetTitleSize(0.12)
    hFrameDiff.GetXaxis().SetTitleSize(0.12)
    hFrameDiff.GetYaxis().SetLabelSize(0.1)
    hFrameDiff.GetXaxis().SetLabelSize(0.1)
    hFrameDiff.GetYaxis().SetTitleOffset(0.41)
    hFrameDiff.GetXaxis().SetTitleOffset(0.8)
    hFrameDiff.SetTickLength(0.06,'X')
    hFrameDiff.SetTickLength(0.04,'Y')
    hFrameDiff.GetYaxis().SetNdivisions(3,5,0,True)

    histo.Draw("hist,same")

    canvas.cd()
    canvas.Modified()
    canvas.Update()

    canvas.SaveAs('data/output/Diamond/Cesio/'+outfilename+'.pdf')

if __name__ == "__main__":

    infilenames = ['data/input/Diamond/Cesio/cesio1.mca','data/input/Diamond/Cesio/cesio2.mca',
                   'data/input/Diamond/Cesio/cesio3.mca', 'data/input/Diamond/Cesio/cesio4.mca',
                   'data/input/Diamond/Cesio/CesioNight.mca']
    histofile = TFile('data/input/Diamond/Cesio/CesiumHistosNoErr.root', 'recreate')


    dict = {'Gain 200': [infilenames[0],"en200"], 'Gain 1000': [infilenames[1],"en1000"], 'Plastica prova': [infilenames[2],"en1000"],
            'Sorgente non scatterless': [infilenames[3],"en1000"], 'Misura notturna con plastica': [infilenames[4],"en1000"]}
    
    color = kAzure-7
    DictHistos(dict, histofile, color, 8)

    # CalibrationErr = CalEnergyErr(0.318,0.008,-30,40,5)
    CalibrationErr = 0
    #print(CalibrationErr)
    ComptonEdge = ComptonEdgeFit(dict['Misura notturna con plastica'][1],CalibrationErr,color)
    InternalConversionPeak = InternalConversionPeakFit(dict['Gain 1000'][1],CalibrationErr,color)
    BetaQValue = BetaQValueFit(dict['Gain 1000'][1],'BetaQValue',CalibrationErr,color)

    with open('data/output/Diamond/Cesio/CesiumAnalysis.txt', 'w') as f:
        Compton = 'Compton edge estimate: ' + ComptonEdge + '\n\n'
        f.write(Compton)
        InternalConversion = 'Internal conversion peak estimate: ' + InternalConversionPeak + '\n\n'
        f.write(InternalConversion)
        QValue = 'Beta Q value estimate: ' + BetaQValue + '\n\n'
        f.write(QValue)

    #comparison between data taken with different gain
    histofileCh = TFile('data/input/Diamond/Cesio/CesiumHistosCh.root','recreate')
    dictCh = {'GainCh 200': [infilenames[0],"chn"], 'GainCh 1000': [infilenames[1],"chn"]}
    DictHistos(dictCh, histofileCh, 4)
    GainChLegend = TLegend(0.6,0.6,0.8,0.8)
    GainChLegend.SetHeader('Amplifier gain')
    GainChLegend.AddEntry(dictCh['GainCh 200'][1],'Coarse 200','lf')
    GainChLegend.AddEntry(dictCh['GainCh 1000'][1],'Coarse 1000','lf')
    GainChLegend.SetTextFont(42)
    GainChLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    GainChLegend.SetFillStyle(0)
    GainChboundaries = [71.74,0.,1200.,1.1]
    GainChCanva = 'MCA normalised counts distribution;Channel;Counts [a.u.]'
    HistoComparison([dictCh['GainCh 1000'][1], dictCh['GainCh 200'][1]], GainChLegend, GainChCanva, GainChboundaries, 'data/output/Diamond/Cesio/GainChComp.pdf',
                    [1,1],[kAzure+3,kOrange-3],[0.5,0.9])
#
    #comparison between data taken with plastic source and scatterless source
    ScatterLegend = TLegend(0.6,0.6,0.8,0.8)
    ScatterLegend.SetHeader('Source feature')
    ScatterLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non scatterless','lf')
    ScatterLegend.AddEntry(dict['Misura notturna con plastica'][1],'Plastica','lf')
    ScatterLegend.SetTextFont(42)
    ScatterLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    ScatterLegend.SetFillStyle(0)
    Scatterboundaries = [71.74,0.,800.,1.1]
    ScatterCanva = 'Sources Comparison;Energy [keV];Counts'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Misura notturna con plastica'][1]], ScatterLegend, ScatterCanva,
                    Scatterboundaries, 'data/output/Diamond/Cesio/SourceComp.pdf',[1,1],[kBlue-4,kYellow-4],[0.5,0.9])
##
    ##comparison between data taken with plastic source and scatterless source
    ScatNonScatLegend = TLegend(0.6,0.6,0.8,0.8)
    ScatNonScatLegend.SetHeader('Source feature')
    ScatNonScatLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non scatterless','lf')
    ScatNonScatLegend.AddEntry(dict['Gain 1000'][1],'Scatterless','lf')
    ScatNonScatLegend.SetTextFont(42)
    ScatNonScatLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    ScatNonScatLegend.SetFillStyle(0)
    ScatNonScatboundaries = [71.74,0.,1000.,1.1]
    ScatNonScatCanva = 'Sources Comparison;Energy [keV];Counts'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Gain 1000'][1]], ScatNonScatLegend, ScatNonScatCanva,
                    ScatNonScatboundaries, 'data/output/Diamond/Cesio/ScatNonScatComp.pdf',[1,1],[kBlue-4,kYellow-4],[0.5,0.9])
##
    ##comparison between all data
    AllSourcesLegend = TLegend(0.5,0.6,0.85,0.8)
    AllSourcesLegend.SetHeader('Source feature')
    AllSourcesLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non-scatterless','lf')
    AllSourcesLegend.AddEntry(dict['Gain 1000'][1],'Scatterless','lf')
    AllSourcesLegend.AddEntry(dict['Misura notturna con plastica'][1],'Scatterless with plastic','lf')
    AllSourcesLegend.SetTextFont(42)
    AllSourcesLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    AllSourcesLegend.SetFillStyle(0)
    AllSourcesboundaries = [71.74,0.,800.,1.1]
    AllSourcesCanva = 'Sources Comparison;Energy [keV];Counts [a.u.]'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Gain 1000'][1],dict['Misura notturna con plastica'][1]], AllSourcesLegend, AllSourcesCanva,
                     AllSourcesboundaries, 'data/output/Diamond/Cesio/AllSourcesComp.pdf',[1,1,1],[kRed,kAzure+3,kOrange-3],[0.9,0.7,0.6])
##
    # HISTOGRAMS COMPARISONS AND SUBTRACTIONS
    legend = TLegend(0.5,0.6,0.85,0.8)
    legend.SetHeader('Source feature')
    legend.AddEntry(dict['Sorgente non scatterless'][1],'Non-scatterless','lf')
    legend.AddEntry(dict['Gain 1000'][1],'Scatterless','lf')
    HistoSubtraction([71.74,0,800,1.1],0.3,dict['Sorgente non scatterless'][1],dict['Gain 1000'][1],legend,'Gain1000VsNonScat')
    legend = TLegend(0.5,0.6,0.85,0.8)
    legend.SetHeader('Source feature')
    legend.AddEntry(dict['Sorgente non scatterless'][1],'Non-scatterless','lf')
    legend.AddEntry(dict['Misura notturna con plastica'][1],'Scatterless with plastic','lf')
    HistoSubtraction([71.74,0,700,1.1],0.95,dict['Sorgente non scatterless'][1],dict['Misura notturna con plastica'][1],legend,'NonScatVsPlasticaNotte')
    legend = TLegend(0.5,0.6,0.85,0.8)
    legend.SetHeader('Source feature')
    legend.AddEntry(dict['Misura notturna con plastica'][1],'Scatterless with plastic','lf')
    legend.AddEntry(dict['Gain 1000'][1],'Scatterless','lf')
    HistoSubtraction([71.74,0,800,1.1],0.9,dict['Gain 1000'][1],dict['Misura notturna con plastica'][1],legend,'Gain1000VsPlasticaNotte')

    #################################