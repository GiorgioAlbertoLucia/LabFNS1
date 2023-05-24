import sys
import pandas as pd
import numpy as np
import yaml

from ROOT import TH1D, TH2D, TCanvas, kAzure, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFile, TPaveText

from Python.utils.StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=.12, padbottommargin=0.12, padrightmargin=1.6, padtopmargin=0.1, titleoffsety=1., titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)


if __name__ == '__main__':

    #load configurations
    configPath = 'Python/configs/imgGen_config.yml'
    with open(configPath, 'r') as configFile:
        config = yaml.load(configFile, yaml.FullLoader)

    inputRootPath = config['th2']['inputRootPath']
    inputHistName = config['th2']['inputHistName']

    palette = config['th2']['palette']

    xmin = config['canvas']['xmin'] 
    ymin = config['canvas']['ymin'] 
    xmax = config['canvas']['xmax'] 
    ymax = config['canvas']['ymax']
    title = config['canvas']['title']
    
    canvas = TCanvas(config['canvas']['name'], config['canvas']['name'], config['canvas']['height'], config['canvas']['width'])
    hFrame = canvas.cd().DrawFrame(xmin, ymin, xmax, ymax, title)
    gStyle.SetPalette(palette)

    # write on canvas
    textBoxs = []
    latexLines = []
    lines = config['latex']['lines']
    linePos = config['latex']['linePos']

    if config['latex']['box']:
        pt = TPaveText(config['latex']['boxPos'][0], config['latex']['boxPos'][1], config['latex']['boxPos'][2], config['latex']['boxPos'][3])
        pt.SetFillColor(0)
        for line in lines:  pt.AddText(line)
        textBoxs.append(pt)
    
    for box in textBoxs:    box.Draw()

    if not config['latex']['box']:
        for line, linePosition in zip(lines, linePos):
            text = TLatex(linePosition[0], linePosition[1], line)
            text.SetNDC()
            text.SetTextSize(gStyle.GetTextSize())
            text.SetTextFont(42)
            latexLines.append(text)
        for line in latexLines: line.Draw()

    # draw th2
    inputFile = TFile(inputRootPath)
    hist = inputFile.Get(inputHistName)
    hist.SetDirectory(0)
    inputFile.Close()
    canvas.cd()
    hist.Draw("colz1 same")

    # canvas options
    if config['canvas']['logx']:        canvas.SetLogx()
    if config['canvas']['logy']:        canvas.SetLogy()
    if config['canvas']['logz']:        canvas.SetLogz()
    canvas.Update()

    canvas.SaveAs(config['th2']['outputPath'])
    canvas.Draw()
    input('Press enter to continue')

        

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

