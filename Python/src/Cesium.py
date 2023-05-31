import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TLegend, gStyle, TF1, Math, TPad, kYellow, TLine, kGray, gPad 
from ReadMCA import DictHistos, HistoComparison

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.14, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.11, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

def InternalConversionPeakFit(histoPeak):
    
    # FIT PICCO CONVERSIONE INTERNA GUADAGNO 1000 - NO BETA ELECTRONS
    FileFitIntConvPeak = TFile('data/output/Diamond/Cesio/InternalConvPeak.root', 'recreate')
    FitLowBound = 640
    FitUppBound = 680
    ComptonEdgeFit = TCanvas('Compton Edge Fit', 'Compton Edge Fit',1280,760)
    hFrame = ComptonEdgeFit.DrawFrame(FitLowBound-FitLowBound*0.05,0.,FitUppBound + FitUppBound*0.05,450,"Internal conversion peak; E[KeV]; Counts")
    IntConvPeak = TF1("Internal conversion peak", "gaus(0)", FitLowBound, FitUppBound)
    #IntConvPeak.SetParameter(0,0.9)
    IntConvPeak.SetParameter(1,660)
    histoPeak.Fit(IntConvPeak,"RM+","",FitLowBound,FitUppBound) # provare 3° opzione func
    histoPeak.SetMarkerColor(4)
    histoPeak.Draw("hist,p")
    histoPeak.Write()
    FitStats(IntConvPeak)
    FileFitIntConvPeak.Close()

def ComptonEdgeFit(histoCompton):
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
    hFrame = ComptonEdgeFit.DrawFrame(450,0.,545,140,"Compton Edge scatterless source with plastic; E[KeV]; Counts")
    histoCompton.SetMarkerColor(4)
    histoCompton.Draw("hist,p,same")
    #histoCompton.Write()
    leg = TLegend(0.62, 0.65, 0.82, 0.85)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    #leg.SetHeader("TDC Normalised counts")
    leg.AddEntry(histoCompton, 'Data', 'lf')
    leg.AddEntry(ComptonEdgeFunction, 'Fit curve', 'lf')
    leg.Draw("same")
    ComptonEdgeFunction.Draw("same")
    ComptonEdgeFit.Modified()
    ComptonEdgeFit.Update()
    ComptonEdgeFit.SaveAs('data/output/Diamond/Cesio/ComptonEdgeFit.pdf')
    #FileFitEdge.Close()

def BetaQValueFit(histoBeta, outfilename):

    BetaQValueFitFile = TFile('data/output/Diamond/Cesio/BetaEdgeFit.root','recreate')
    BetaQValueFit = TCanvas("Beta Q Value Fit", "Beta Q Value Fit", 1280, 760)

    # FIT AND DRAWING BOUNDARIES
    #FitLowBound1 = 385
    FitLowBound1 = 405
    FitUppBound1 = 490
    FitLowBound2 = 540
    FitUppBound2 = 633
    BoundDrawBetaCurve = 600
    BoundDrawConstCurve = 490
    CanvaYAxisBottomBound = 0.
    CanvaYAxisTopBound = 0.

    BetaCurveFunction = TF1("Beta Curve", "[0] + TMath::Exp(-[1]*(x-[2]) )", FitLowBound1, BoundDrawBetaCurve)
    BetaCurveFunction.SetParameter(0,40)
    BetaCurveFunction.SetParameter(1,0.0109)
    BetaCurveFunction.SetParameter(2,910)

    ConstFunction = TF1("Compton Plateau", "[0]", BoundDrawConstCurve, FitUppBound2)
    ConstFunction.SetParameter(1,50)

    histoBeta.Fit(BetaCurveFunction,"L","",FitLowBound1,FitUppBound1)
    histoBeta.Fit(ConstFunction,"L","",FitLowBound2,FitUppBound2)

    FitStats(ConstFunction)
    FitStats(BetaCurveFunction)

    # DRAW THE GRAPH
    hFrame = BetaQValueFit.DrawFrame(FitLowBound1-FitLowBound1*0.1,CanvaYAxisBottomBound,FitUppBound2+FitUppBound2*0.13,CanvaYAxisTopBound,"Q value Beta Decay Fit; E[KeV]; Counts")
    histoBeta.SetMarkerColor(4)
    histoBeta.Draw("hist,p,same")
    BetaCurveFunction.Draw("same")
    BetaCurveFunction.SetLineColor(kGreen) 
    ConstFunction.Draw("same")
    ConstFunction.SetLineColor(kViolet)
    BetaCurveFitLowBound = TLine(FitLowBound1,gPad.GetUymax(),FitLowBound1,gPad.GetUymin())
    BetaCurveFitUppBound = TLine(FitUppBound1,gPad.GetUymax(),FitUppBound1,gPad.GetUymin())
    BetaCurveFitLowBound.SetLineColor(kGreen+2)
    BetaCurveFitUppBound.SetLineColor(kGreen+2)
    ConstCurveFitLowBound = TLine(FitLowBound2,gPad.GetUymax(),FitLowBound2,gPad.GetUymin())
    ConstCurveFitUppBound = TLine(FitUppBound2,gPad.GetUymax(),FitUppBound2,gPad.GetUymin())
    ConstCurveFitLowBound.SetLineColor(kViolet+2)
    ConstCurveFitUppBound.SetLineColor(kViolet+2)
    BetaCurveFitLowBound.Draw("same")
    BetaCurveFitUppBound.Draw("same")
    ConstCurveFitLowBound.Draw("same")
    ConstCurveFitUppBound.Draw("same")
    legend = TLegend(0.5,0.6,0.75,0.8)
    legend.SetTextFont(42)
    legend.SetTextSize(gStyle.GetTextSize()*0.7)
    legend.SetFillStyle(0)
    legend.AddEntry(histoBeta, 'Data', 'lf')
    legend.AddEntry(BetaCurveFunction, 'Beta Curve Fit', 'lf')
    legend.AddEntry(BetaCurveFitLowBound,'Beta curve fit range', 'lf')
    legend.AddEntry(ConstFunction, 'Plateau Fit', 'lf')
    legend.AddEntry(ConstCurveFitLowBound, 'Plateau fit range', 'lf')
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
    print('Q value estimate: ', QValueEstimate, u"\u00B1", QValueEstimateError)

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
    hFrame = pad.DrawFrame(DFbound[0],DFbound[1],DFbound[2],DFbound[3],"MCA normalised counts distribution;Energy [KeV];Counts")
    histo1copy.Scale(1/histo1copy.GetMaximum())
    SetObjectStyle(histo1copy, color = kBlue-4, fillalpha=0.5)
    histo1copy.Draw("hist,same")
    histo2copy.Scale(1/histo2copy.GetMaximum())
    SetObjectStyle(histo2copy, color = kYellow-4, fillalpha=0.9)
    histo2copy.Draw("hist,same")
    legend.Draw("same")

    padDiff.cd()
    # DA FARE: SOTTRARRE ISTOGRAMMI NORMALIZZATI ALL'AREA TOTALE
    hFrameDiff = pad.DrawFrame(DFbound[0],DFbound[1],DFbound[2],diffYbound,";Energy [KeV];Difference")
    histo = histo1copy.Clone()
    histo.Add(histo2copy,-1.)      # Performs subtraction
    SetObjectStyle(histo, color = kGreen-4, fillalpha=0.5)

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
    
    #energyErr = CalEnergyErr(rebin)
    #print('Energy calibration error: ', energyErr)
    #print(dict['Gain 1000'][1])
    DictHistos(dict, histofile, 4)

    ComptonEdgeFit(dict['Misura notturna con plastica'][1])
    InternalConversionPeakFit(dict['Gain 1000'][1])
    BetaQValueFit(dict['Gain 1000'][1],'BetaQValue')

    rebin = 4
    for key in dict.keys():
        print(key)
        dict[key][1].Rebin(rebin)
    print(dict['Gain 1000'][1].GetNbinsX())
    print(dict['Gain 200'][1].GetNbinsX())

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
    GainChCanva = 'Amplifier Gain Comparison;Channel;Counts'
    HistoComparison([dictCh['GainCh 1000'][1], dictCh['GainCh 200'][1]], GainChLegend, GainChCanva, GainChboundaries, 'data/output/Diamond/Cesio/GainChComp.pdf',
                    [1,1],[kBlue-4,kYellow-4],[0.5,0.9])

    #comparison between data taken with plastic source and scatterless source
    ScatterLegend = TLegend(0.6,0.6,0.8,0.8)
    ScatterLegend.SetHeader('Source feature')
    ScatterLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non scatterless','lf')
    ScatterLegend.AddEntry(dict['Misura notturna con plastica'][1],'Plastica','lf')
    ScatterLegend.SetTextFont(42)
    ScatterLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    ScatterLegend.SetFillStyle(0)
    Scatterboundaries = [71.74,0.,800.,1.1]
    ScatterCanva = 'Sources Comparison;Energy [KeV];Counts'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Misura notturna con plastica'][1]], ScatterLegend, ScatterCanva,
                    Scatterboundaries, 'data/output/Diamond/Cesio/SourceComp.pdf',[1,1],[kBlue-4,kYellow-4],[0.5,0.9])
#
    ##comparison between data taken with plastic source and scatterless source
    ScatNonScatLegend = TLegend(0.6,0.6,0.8,0.8)
    ScatNonScatLegend.SetHeader('Source feature')
    ScatNonScatLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non scatterless','lf')
    ScatNonScatLegend.AddEntry(dict['Gain 1000'][1],'Scatterless','lf')
    ScatNonScatLegend.SetTextFont(42)
    ScatNonScatLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    ScatNonScatLegend.SetFillStyle(0)
    ScatNonScatboundaries = [71.74,0.,1000.,1.1]
    ScatNonScatCanva = 'Sources Comparison;Energy [KeV];Counts'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Gain 1000'][1]], ScatNonScatLegend, ScatNonScatCanva,
                    ScatNonScatboundaries, 'data/output/Diamond/Cesio/ScatNonScatComp.pdf',[1,1],[kBlue-4,kYellow-4],[0.5,0.9])
#
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
    AllSourcesCanva = 'Sources Comparison;Energy [KeV];Counts'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Gain 1000'][1],dict['Misura notturna con plastica'][1]], AllSourcesLegend, AllSourcesCanva,
                     AllSourcesboundaries, 'data/output/Diamond/Cesio/AllSourcesComp.pdf',[1,1,1],[kBlue-4,kGreen-4,kYellow-4],[0.9,0.7,0.7])
#
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

