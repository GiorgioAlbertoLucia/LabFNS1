import sys
sys.path.append('Python/utils')

from ReadMCA import CreateHist
from ROOT import TCanvas, TPad, TFile, kAzure, kOrange, kRed
from StyleFormatter import SetObjectStyle, SetGlobalStyle 

SetGlobalStyle(padleftmargin=0.1, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1., titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

if __name__ == '__main__':

    InfileLead = 'data/input/Gamma/Merc/SodioWithPb.mca'
    InfileNoLead = 'data/input/Gamma/Merc/SodioNoPb.mca'
    rebin = 8
    SizeLittlePad = 0.3   # size in %
    xmax = 1024
    ymax = 6.e4
    ymaxDifference = 5.e3

    ###########################################


    canvas = TCanvas("Canvas", "Canvas",1000,1000)

    pad = TPad("pad","pad",0.,SizeLittlePad,1.,1.)
    #pad.SetTopMargin(0.)
    pad.SetBottomMargin(0.)
    pad.Draw()
    padDiff = TPad("padDiff","padDiff",0.,0.,1.,SizeLittlePad)
    padDiff.SetTopMargin(0.)
    padDiff.SetBottomMargin(0.3)
    padDiff.Draw()

    pad.cd()
    hFrame = pad.DrawFrame(0,0.1,xmax,ymax,"MCA counts distribution;Channel;Counts")
    histoLead = CreateHist(InfileLead,0)
    SetObjectStyle(histoLead, color = kAzure+3, fillalpha=0.5)
    histoLead.Draw("hist,same")
    histoLead.Rebin(rebin)
    histoNoLead = CreateHist(InfileNoLead,0)
    SetObjectStyle(histoNoLead, color = kOrange-3, fillalpha=0.5)
    histoNoLead.Draw("hist,same")
    histoNoLead.Rebin(rebin)

    padDiff.cd()
    hFrameDiff = pad.DrawFrame(0,0,xmax,ymaxDifference,";Channel;Difference")
    histo = histoLead.Clone()
    histo.Add(histoNoLead,-1.)      # Performs subtraction
    for idx in range(histo.GetNbinsX()):
        histo.SetBinContent(idx,abs(histo.GetBinContent(idx)))
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

    canvas.SaveAs('data/output/Figures/GammaCoincidence/LeadDifference.pdf')
    
    outfile = TFile('data/output/Figures/GammaCoincidence/LeadDifference.root','recreate')
    canvas.Write()
    outfile.Close()




