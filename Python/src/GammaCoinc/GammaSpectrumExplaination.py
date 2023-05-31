import sys
sys.path.append('Python/utils')

from ReadMCA import CreateHist
from ROOT import TCanvas, TPad, TFile, TLatex, TArrow, kAzure, kOrange, kRed, gStyle
from StyleFormatter import SetObjectStyle, SetGlobalStyle 

SetGlobalStyle(padleftmargin=0.1, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=0.9, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

def CreateExplainedSpectrum():
    Infile = 'data/input/Gamma/Merc/SodioWithPb.mca'
    rebin = 8
    xmax = 1024
    ymax = 6.e4

    ###########################################


    canvas = TCanvas("Canvas", "Canvas",1000,1000)
    hFrame = canvas.DrawFrame(0,0.1,xmax,ymax,"MCA counts distribution;Channel;Counts")
    hFrame.GetYaxis().SetMaxDigits(3)
    histo = CreateHist(Infile,0)
    SetObjectStyle(histo, color = kAzure+3, fillalpha=0.5)
    histo.Draw("hist,same")
    histo.Rebin(rebin)

    LeadX =TLatex(0.15, 0.51,"Pb X-rays")
    LeadX.SetNDC()
    LeadX.SetTextSize(gStyle.GetTextSize()*0.4)
    LeadX.SetTextFont(42)
    LeadX.Draw()
    ArrowLead = TArrow(0.15,0.3, 0.18,0.5,0.01,"<|")
    ArrowLead.SetAngle(60)
    ArrowLead.SetLineWidth(2)
    ArrowLead.SetFillColor(kAzure)
    ArrowLead.SetNDC()
    ArrowLead.Draw()
    BS =TLatex(0.18, 0.41,"Backscattering")
    BS.SetNDC()
    BS.SetTextSize(gStyle.GetTextSize()*0.4)
    BS.SetTextFont(42)
    BS.Draw()
    ArrowBS = TArrow(0.21,0.32, 0.22,0.4,0.01,"<|")
    ArrowBS.SetAngle(60)
    ArrowBS.SetLineWidth(2)
    ArrowBS.SetFillColor(kAzure)
    ArrowBS.SetNDC()
    ArrowBS.Draw()
    C511 =TLatex(0.26, 0.62,"#splitline{Compton edge}{#kern[0.1]{#gamma (511 keV)}}")
    C511.SetNDC()
    C511.SetTextSize(gStyle.GetTextSize()*0.4)
    C511.SetTextFont(42)
    C511.Draw()
    ArrowC511 = TArrow(0.29,0.25, 0.33,0.6,0.01,"<|")
    ArrowC511.SetAngle(60)
    ArrowC511.SetLineWidth(2)
    ArrowC511.SetFillColor(kAzure)
    ArrowC511.SetNDC()
    ArrowC511.Draw()
    Ph511 =TLatex(0.33, 0.80,"#splitline{Photoelectric peak}{#kern[0.25]{#gamma (511 keV)}}")
    Ph511.SetNDC()
    Ph511.SetTextSize(gStyle.GetTextSize()*0.4)
    Ph511.SetTextFont(42)
    Ph511.Draw()
    C1275 =TLatex(0.58, 0.28,"#splitline{Compton edge}{#kern[0.1]{#gamma (1275 keV)}}")
    C1275.SetNDC()
    C1275.SetTextSize(gStyle.GetTextSize()*0.4)
    C1275.SetTextFont(42)
    C1275.Draw()
    ArrowC1275 = TArrow(0.67,0.17, 0.64,0.26,0.01,"<|")
    ArrowC1275.SetAngle(60)
    ArrowC1275.SetLineWidth(2)
    ArrowC1275.SetFillColor(kAzure)
    ArrowC1275.SetNDC()
    ArrowC1275.Draw()
    Ph1275 =TLatex(0.74, 0.3,"#splitline{Photoelectric peak}{#kern[0.2]{#gamma (1275 keV)}}")
    Ph1275.SetNDC()
    Ph1275.SetTextSize(gStyle.GetTextSize()*0.4)
    Ph1275.SetTextFont(42)
    Ph1275.Draw()
    ArrowPh1275 = TArrow(0.81,0.21, 0.81,0.28,0.01,"<|")
    ArrowPh1275.SetAngle(60)
    ArrowPh1275.SetLineWidth(2)
    ArrowPh1275.SetFillColor(kAzure)
    ArrowPh1275.SetNDC()
    ArrowPh1275.Draw()

    Title =TLatex(0.51, 0.60,"^{22}Na spectrum")
    Title.SetNDC()
    Title.SetTextSize(gStyle.GetTextSize())
    Title.SetTextFont(42)
    Title.Draw()
    text =TLatex(0.55, 0.54,"Acquisition time: 100 s")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize()*0.7)
    text.SetTextFont(42)
    text.Draw()

    canvas.SaveAs('data/output/Figures/GammaCoincidence/Gammaspectrum.pdf')
    
    outfile = TFile('data/output/Figures/GammaCoincidence/Gammaspectrum.root','recreate')
    canvas.Write()
    outfile.Close()

def CreateSumSpectrum():
    Infile = '/home/fabrizio/Documents/Lectures/Lab1/LabFNS1/data/input/Gamma/SodioPiccoSomma.mca'
    rebin = 8
    xmax = 1024
    ymax = 1.e6

    ###########################################


    canvas = TCanvas("Canvas", "Canvas",1000,1000)
    canvas.SetLogy()
    canvas.SetLeftMargin(0.13)
    hFrame = canvas.DrawFrame(0,1,xmax,ymax,"MCA counts distribution;Channel;Counts")
    hFrame.GetYaxis().SetMaxDigits(3)
    hFrame.GetYaxis().SetTitleOffset(1.2)
    histo = CreateHist(Infile,0)
    SetObjectStyle(histo, color = kAzure+3, fillalpha=0.5)
    histo.Draw("hist,same")
    histo.Rebin(rebin)

    Title =TLatex(0.51, 0.75,"^{22}Na spectrum")
    Title.SetNDC()
    Title.SetTextSize(gStyle.GetTextSize())
    Title.SetTextFont(42)
    Title.Draw()
    text =TLatex(0.55, 0.69,"Acquisition time: 353.75 s")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize()*0.7)
    text.SetTextFont(42)
    text.Draw()

    canvas.SaveAs('data/output/Figures/GammaCoincidence/GammaSumSpectrum.pdf')
    outfile = TFile('data/output/Figures/GammaCoincidence/GammaSumspectrum.root','recreate')
    canvas.Write()
    outfile.Close()

    
if __name__ == '__main__':
    #CreateExplainedSpectrum()
    CreateSumSpectrum()