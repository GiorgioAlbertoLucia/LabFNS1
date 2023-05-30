import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ROOT import TCanvas, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure, kViolet, TFile, TLegend, gStyle, TF1, Math, TPad 
from ReadMCA import DictHistos, HistoComparison

from StyleFormatter import SetObjectStyle, SetGlobalStyle

SetGlobalStyle(padleftmargin=0.14, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.11, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

if __name__ == "__main__":

    infilenames = ['data/input/Diamond/Cesio/cesio1.mca','data/input/Diamond/Cesio/cesio2.mca',
                   'data/input/Diamond/Cesio/cesio3.mca', 'data/input/Diamond/Cesio/cesio4.mca',
                   'data/input/Diamond/Cesio/CesioNight.mca']
    histofile = TFile('data/input/Diamond/Cesio/CesiumHistos.root', 'recreate')

    dict = {'Gain 200': infilenames[0], 'Gain 1000': infilenames[1], 'Plastica prova': infilenames[2],
            'Sorgente non scatterless': infilenames[3], 'Misura notturna con plastica': infilenames[4]}
    
    DictHistos(dict, histofile, 4)


    #comparison between data taken with different gain
    #GainLegend = TLegend(0.6,0.6,0.8,0.8)
    #GainLegend.SetHeader('Amplifier gain','C')
    #GainLegend.AddEntry(dict['Gain 200'][1],'200','lf')
    #GainLegend.AddEntry(dict['Gain 1000'][1],'1000','lf')
    #GainLegend.SetTextFont(42)
    #GainLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    #GainLegend.SetFillStyle(0)
    #Gainboundaries = [0.,0.,1200.,1.1]
    #GainCanva = 'Gain Comparison;Channel;Counts'
    #HistoComparison([dict['Gain 1000'][1], dict['Gain 200'][1]], GainLegend, GainCanva, Gainboundaries, 'data/output/Diamond/Cesio/GainComp.pdf',
    #                [4,4],[kAzure+3,kOrange-3],[0.5,0.9])

    #comparison between data taken with plastic source and scatterless source
    #ScatterLegend = TLegend(0.6,0.6,0.8,0.8)
    #ScatterLegend.SetHeader('Source feature','C')
    #ScatterLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non scatterless','lf')
    #ScatterLegend.AddEntry(dict['Misura notturna con plastica'][1],'Plastica','lf')
    #ScatterLegend.SetTextFont(42)
    #ScatterLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    #ScatterLegend.SetFillStyle(0)
    #Scatterboundaries = [300.,0.,3400.,1.1]
    #ScatterCanva = 'Sources Comparison;Energy [KeV];Counts'
    #HistoComparison([dict['Sorgente non scatterless'][1], dict['Misura notturna con plastica'][1]], ScatterLegend, ScatterCanva,
    #                Scatterboundaries, 'data/output/Diamond/Cesio/SourceComp.pdf',[4,4],[kAzure+3,kOrange-3],[0.5,0.9])
    
    #comparison between data taken with plastic source and scatterless source
    ScatNonScatLegend = TLegend(0.6,0.6,0.8,0.8)
    ScatNonScatLegend.SetHeader('Source feature','C')
    ScatNonScatLegend.AddEntry(dict['Sorgente non scatterless'][1],'Non scatterless','lf')
    ScatNonScatLegend.AddEntry(dict['Gain 1000'][1],'Scatterless','lf')
    ScatNonScatLegend.SetTextFont(42)
    ScatNonScatLegend.SetTextSize(gStyle.GetTextSize()*0.7)
    ScatNonScatLegend.SetFillStyle(0)
    ScatNonScatboundaries = [0.,0.,1000.,1.1]
    ScatNonScatCanva = 'Sources Comparison;Energy [KeV];Counts'
    HistoComparison([dict['Sorgente non scatterless'][1], dict['Gain 1000'][1]], ScatNonScatLegend, ScatNonScatCanva,
                    ScatNonScatboundaries, 'data/output/Diamond/Cesio/ScatNonScatComp.pdf',[4,4],[kAzure+3,kOrange-3],[0.5,0.9])
    

    # FIT COMPTON EDGE ACQUISITION WITH PLASTIC - NO BETA ELECTRONS
    #FileFitEdge = TFile('data/output/Diamond/Cesio/ComptonEdge.root', 'recreate')
    #FitLowBound = 455
    #FitUppBound = 530
    #ComptonEdgeFunction = TF1("Compton Edge", " [0] / (1+TMath::Exp( - ( x-[1] )/[2] ) ) + TMath::Exp(-[3]*x)", FitLowBound, FitUppBound)
    #ComptonEdgeFunction.SetParameter(1,490)
    ##ComptonEdgeFunction = TF1("Compton Edge", " [0] / (1+TMath::Exp( - ( x-[1] )/[2] ) ) + [3]*(1/([4]*x+[5]) )", FitLowBound, FitUppBound)
    ##ComptonEdgeFunction.SetParameter(0,0.9)
    ##ComptonEdgeFunction.SetParameter(0,490)
    ##ComptonEdgeFunction.SetParameter(2,30)
    #dict['Misura notturna con plastica'][1].Fit(ComptonEdgeFunction,"L","",FitLowBound,FitUppBound) # provare 3° opzione func
    #dict['Misura notturna con plastica'][1].SetMarkerColor(4)
    #dict['Misura notturna con plastica'][1].Draw("hist,p")
    #dict['Misura notturna con plastica'][1].Write()
    #Chisquare = ComptonEdgeFunction.GetChisquare()
    #Chicrit = Math.chisquared_quantile_c(0.05,ComptonEdgeFunction.GetNDF())
    #NDegFreedom = ComptonEdgeFunction.GetNDF()
    #Pvalue = ComptonEdgeFunction.GetProb()
    #FileFitEdge.Close()
    #print('Chi Square:', Chisquare, ', Degrees of freedom:', NDegFreedom, ', Critical Chi Square:', Chicrit,', P-value: ', Pvalue)

    # FIT PICCO CONVERSIONE INTERNA GUADAGNO 1000 - NO BETA ELECTRONS
    #FileFitIntConvPeak = TFile('data/output/Diamond/Cesio/InternalConvPeak.root', 'recreate')
    #FitLowBound = 640
    #FitUppBound = 680
    #IntConvPeak = TF1("Internal conversion peak", "gaus(0)", FitLowBound, FitUppBound)
    ##IntConvPeak.SetParameter(0,0.9)
    #IntConvPeak.SetParameter(1,660)
    #dict['Gain 1000'][1].Fit(IntConvPeak,"RM+","",FitLowBound,FitUppBound) # provare 3° opzione func
    #dict['Gain 1000'][1].SetMarkerColor(4)
    #dict['Gain 1000'][1].Draw("hist,p")
    #dict['Gain 1000'][1].Write()
    #Chisquare = IntConvPeak.GetChisquare()
    #Chicrit = Math.chisquared_quantile_c(0.05,IntConvPeak.GetNDF())
    #NDegFreedom = IntConvPeak.GetNDF()
    #Pvalue = IntConvPeak.GetProb()
    #FileFitIntConvPeak.Close()
    #print('Chi Square:', Chisquare, ', Degrees of freedom:', NDegFreedom, ', Critical Chi Square:', Chicrit,', P-value: ', Pvalue)


    ###########################################


    #SizeLittlePad = 0.3   # size in %
    #canvas = TCanvas("Canvas", "Canvas",1000,1000)
    #pad = TPad("pad","pad",0.,SizeLittlePad,1.,1.)
    ##pad.SetTopMargin(0.)
    #pad.SetBottomMargin(0.)
    #pad.Draw()
    #padDiff = TPad("padDiff","padDiff",0.,0.,1.,SizeLittlePad)
    #padDiff.SetTopMargin(0.)
    #padDiff.SetBottomMargin(0.3)
    #padDiff.Draw()
#
    #pad.cd()
    #hFrame = pad.DrawFrame(71.74,0,800,1.1,"MCA normalised counts distribution;Energy [KeV];Counts")
    #dict['Sorgente non scatterless'][1].Scale(1/dict['Sorgente non scatterless'][1].GetMaximum())
    #SetObjectStyle(dict['Sorgente non scatterless'][1], color = kAzure+3, fillalpha=0.5)
    #dict['Sorgente non scatterless'][1].Draw("hist,same")
    #dict['Misura notturna con plastica'][1].Scale(1/dict['Misura notturna con plastica'][1].GetMaximum())
    #SetObjectStyle(dict['Misura notturna con plastica'][1], color = kOrange-3, fillalpha=0.9)
    #dict['Misura notturna con plastica'][1].Draw("hist,same")
#
    #padDiff.cd()
    ## DA FARE: SOTTRARRE ISTOGRAMMI NORMALIZZATI ALL'AREA TOTALE
    #hFrameDiff = pad.DrawFrame(71.74,0,800,1.1,";Energy [KeV];Difference")
    #histo = dict['Sorgente non scatterless'][1].Clone()
    #histo.Add(dict['Misura notturna con plastica'][1],-1.)      # Performs subtraction
    #SetObjectStyle(histo, color = kRed, fillalpha=0.5)
#
    #hFrameDiff.GetYaxis().SetTitleSize(0.12)
    #hFrameDiff.GetXaxis().SetTitleSize(0.12)
    #hFrameDiff.GetYaxis().SetLabelSize(0.1)
    #hFrameDiff.GetXaxis().SetLabelSize(0.1)
    #hFrameDiff.GetYaxis().SetTitleOffset(0.41)
    #hFrameDiff.GetXaxis().SetTitleOffset(0.8)
    #hFrameDiff.SetTickLength(0.06,'X')
    #hFrameDiff.SetTickLength(0.04,'Y')
    #hFrameDiff.GetYaxis().SetNdivisions(3,5,0,True)
#
    #histo.Draw("hist,same")
#
    #canvas.cd()
    #canvas.Modified()
    #canvas.Update()
#
    #canvas.SaveAs('data/output/Diamond/Cesio/PlasticScatterlessDifference.pdf')
