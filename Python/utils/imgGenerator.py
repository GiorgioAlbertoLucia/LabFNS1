import sys
import pandas as pd
import numpy as np
import yaml

from ROOT import TH1D, TCanvas, kAzure, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFile

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)



def addHistToCanvas(canvas, legend, inputRootPath, inputHistName, styleOptions, legendCaption):
    '''

    Parameters
    ----------
        styleOptions (list): [color, fillalpha, linewidth]
    '''

    inputFile = TFile(inputRootPath)
    hist = inputFile.Get(inputHistName)
    hist.SetDirectory(0)
    inputFile.Close()

    [color, fillalpha, linewidth] = styleOptions
    SetObjectStyle(hist, color=color, fillalpha=fillalpha, linewidth=linewidth)
    hist.Draw("hist,same")
    leg.AddEntry(hist, legendCaption, 'lf')



if __name__ == '__main__':

    configPath = 'Python/configs/imgGen_config.yml'
    with open(configPath, 'r') as configFile:
        config = yaml.load(configFile, yaml.FullLoader)

    inputRootPaths = config['inputRootPaths']
    inputHistNames = config['inputHistNames']
    colors = config['colors']
    fillalphas = config['fillalphas']
    linewidths = config['linewidths']
    legCaptions = config['legCaptions']
    
    canvas = TCanvas(config['canvas']['name'], config['canvas']['name'], config['canvas']['height'], config['canvas']['width'])
    canvas.SetTitle(config['canvas']['title'])
    leg = TLegend(config['legend']['pos'][0], config['legend']['pos'][1], config['legend']['pos'][2], config['legend']['pos'][3])
    leg.SetTextFont(config['legend']['font'])
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(config['legend']['fillstyle'])

    for inputRootPath, inputHistName, color, fillalpha, linewidth, legCaption in zip(inputRootPaths, inputHistNames, colors, fillalphas, linewidths, legCaptions):
        styleOptions = [color, fillalpha, linewidth]
        addHistToCanvas(canvas, leg, inputRootPath, inputHistName, styleOptions, legCaption)

    leg.Draw('same')
    canvas.SaveAs(config['outputPath'])
        

#text =TLatex(0.45, 0.73,"S1 Scintillator + PMXP2020")
#text.SetNDC()
#text.SetTextSize(gStyle.GetTextSize())
#text.SetTextFont(42)
#text.Draw()
#text2 =TLatex(0.45, 0.55,"Using V259 pattern unit")
#text2.SetNDC()
#text2.SetTextSize(gStyle.GetTextSize()*0.7)
#text2.SetTextFont(42)
#text2.Draw()
#text3 =TLatex(0.45, 0.49,"Acquisition time: 236985 s")
#text3.SetNDC()
#text3.SetTextSize(gStyle.GetTextSize()*0.7)
#text3.SetTextFont(42)
#text3.Draw()
#text4 =TLatex(0.45, 0.43,"Discriminator threshold value: (#font[122]{-}39.6 #pm 0.5) mV")
#text4.SetNDC()
#text4.SetTextSize(gStyle.GetTextSize()*0.7)
#text4.SetTextFont(42)
#text4.Draw()

