import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TLegend, gStyle, TF1, Math, TPad, kYellow, TLine, kGray, gPad 
from ReadMCA import DictHistos, HistoComparison, CalEnergyErr, FitStats

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.14, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.11, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

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

    FitLowBound1 = 375
    FitUppBound1 = 470
    FitLowBound2 = 560
    FitUppBound2 = 645
    BoundDrawBetaCurve = 580
    BoundDrawConstCurve = 500
    CanvaYAxisBottomBound = 0.
    CanvaYAxisTopBound = 1000.

    BetaCurveFunction = TF1("Beta Curve", "[0] + TMath::Exp(-[1]*(x-[2]) )", 350, BoundDrawBetaCurve)
    BetaCurveFunction.SetParameter(0,40)
    BetaCurveFunction.SetParameter(1,0.0109)
    BetaCurveFunction.SetParameter(2,910)

    ConstFunction = TF1("Compton Plateau", "[0]", BoundDrawConstCurve, 660)
    ConstFunction.SetParameter(1,25)

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
    BetaCurveFitLowBound = TLine(FitLowBound1,0.8*gPad.GetUymax(),FitLowBound1,0.21*gPad.GetUymax())
    BetaCurveFitUppBound = TLine(FitUppBound1,0.3*gPad.GetUymax(),FitUppBound1,0.01*gPad.GetUymax())
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
    BetaQValueFit.SaveAs('data/output/Diamond/'+outfilename+'.pdf')
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


if __name__ == "__main__":
    infilenames = ['data/input/Diamond/Sodio/sodio1.mca','data/input/Diamond/Sodio/sodio2merc.mca']
    histofile = TFile('data/input/Diamond/Sodio/SodiumHistosNoErr.root', 'recreate')


    dict = {'Elettroni': [infilenames[0],"en1000"], 'Fotoni': [infilenames[1],"en1000"]}
    
    color = kAzure-7
    DictHistos(dict, histofile, color, 8)

    print(BetaQValueFit(dict['Elettroni'][1],'BetaQValuesSodium',24.682567936394918,color))