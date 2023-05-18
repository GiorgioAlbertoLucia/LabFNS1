import pandas as pd
import numpy as np
import uproot
from ROOT import TH1D, TCanvas, kAzure, kRed, kGreen, kSpring, TLegend, TLatex, gStyle, TFitResultPtr

import sys
sys.path.append('/home/marcello/LabFNS1/Python/utils')

from StyleFormatter import SetGlobalStyle, SetObjectStyle

SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)

# ROOT histograms created for each pedestal acquisition

treeNoInpSix=uproot.open("/home/marcello/LabFNS1/data/input/pedestals_trees/pulseronly_6ms.root")["fTreeData"]
tNoInpSix=treeNoInpSix.arrays(library='pd')
tNoInpSix=tNoInpSix[["Module4_10","Module4_11"]]

hCh10pedSix = TH1D("hCh10pedSix","hCh10pedSix",2048,0,2048)
hCh10pedSix.FillN(len(tNoInpSix["Module4_10"]),np.asarray(tNoInpSix["Module4_10"],'d'),np.asarray([1]*len(tNoInpSix["Module4_10"]),'d'))
hCh10pedSix.Scale(1/len(tNoInpSix))
hCh10pedSix.Rebin(2)
hCh10pedSix.Fit("gaus")
print('Pedestal Gate 6 mu s channel 10: ', hCh10pedSix.GetMean(), ' RMS: ', hCh10pedSix.GetRMS())


hCh11pedSix = TH1D("hCh11pedSix","hCh11pedSix",2048,0,2048)
hCh11pedSix.FillN(len(tNoInpSix["Module4_11"]),np.asarray(tNoInpSix["Module4_11"],'d'),np.asarray([1]*len(tNoInpSix["Module4_11"]),'d'))
hCh11pedSix.Scale(1/len(tNoInpSix))
hCh11pedSix.Rebin(2)
hCh11pedSix.Fit("gaus")
print('Pedestal Gate 6 mu s channel 11: ', hCh11pedSix.GetMean(), ' RMS: ', hCh11pedSix.GetRMS())


treeNoInpTen=uproot.open("/home/marcello/LabFNS1/data/input/pedestals_trees/pulseronly_10ms.root")["fTreeData"]
tNoInpTen=treeNoInpTen.arrays(library='pd')
tNoInpTen=tNoInpTen[["Module4_10","Module4_11"]]

hCh10pedTen = TH1D("hCh10pedTen","hCh10pedTen",2048,0,2048)
hCh10pedTen.FillN(len(tNoInpTen["Module4_10"]),np.asarray(tNoInpTen["Module4_10"],'d'),np.asarray([1]*len(tNoInpTen["Module4_10"]),'d'))
hCh10pedTen.Scale(1/len(tNoInpTen))
hCh10pedTen.Rebin(2)
hCh10pedTen.Fit("gaus")
print('Pedestal Gate 6 mu s channel 10: ', hCh10pedTen.GetMean(), ' RMS: ', hCh10pedTen.GetRMS())

hCh11pedTen = TH1D("hCh11pedTen","hCh11pedTen",2048,0,2048)
hCh11pedTen.FillN(len(tNoInpTen["Module4_11"]),np.asarray(tNoInpTen["Module4_11"],'d'),np.asarray([1]*len(tNoInpTen["Module4_11"]),'d'))
hCh11pedTen.Scale(1/len(tNoInpTen))
hCh11pedTen.Rebin(2)
hCh11pedTen.Fit("gaus")
print('Pedestal Gate 6 mu s channel 11: ', hCh11pedTen.GetMean(), ' RMS: ', hCh11pedTen.GetRMS())

treeInpSix=uproot.open("/home/marcello/LabFNS1/data/input/pedestals_trees/S1SG_6ms.root")["fTreeData"]
tInpSix=treeInpSix.arrays(library='pd')
tInpSix=tInpSix[["Module4_10","Module4_11"]]

hCh10pedInpSix = TH1D("hCh10pedInpSix","hCh10pedInpSix",2048,0,2048)
hCh10pedInpSix.FillN(len(tNoInpSix["Module4_10"]),np.asarray(tNoInpSix["Module4_10"],'d'),np.asarray([1]*len(tNoInpSix["Module4_10"]),'d'))
hCh10pedInpSix.Scale(1/len(tNoInpSix))
hCh10pedInpSix.Rebin(2)
hCh10pedInpSix.Fit("gaus")
print('Pedestal Gate 6 mu s channel 10: ', hCh10pedInpSix.GetMean(), ' RMS: ', hCh10pedInpSix.GetRMS())

hCh11pedInpSix = TH1D("hCh11pedInpSix","hCh11pedInpSix",2048,0,2048)
hCh11pedInpSix.FillN(len(tNoInpSix["Module4_11"]),np.asarray(tNoInpSix["Module4_11"],'d'),np.asarray([1]*len(tNoInpSix["Module4_11"]),'d'))
hCh11pedInpSix.Scale(1/len(tNoInpSix))
hCh11pedInpSix.Rebin(2)
hCh11pedInpSix.Fit("gaus")
print('Pedestal Gate 6 mu s channel 11: ', hCh11pedInpSix.GetMean(), ' RMS: ', hCh11pedInpSix.GetRMS())

treeInpTen=uproot.open("/home/marcello/LabFNS1/data/input/pedestals_trees/S1SG_10ms.root")["fTreeData"]
tInpTen=treeInpTen.arrays(library='pd')
tInpTen=tInpTen[["Module4_10","Module4_11"]]

hCh10pedInpTen = TH1D("hCh10pedInpTen","hCh10pedInpTen",2048,0,2048)
hCh10pedInpTen.FillN(len(tNoInpTen["Module4_10"]),np.asarray(tNoInpTen["Module4_10"],'d'),np.asarray([1]*len(tNoInpTen["Module4_10"]),'d'))
hCh10pedInpTen.Scale(1/len(tNoInpTen))
hCh10pedInpTen.Rebin(2)
hCh10pedInpTen.Fit("gaus")
print('Pedestal Gate 6 mu s channel 10: ', hCh10pedInpTen.GetMean(), ' RMS: ', hCh10pedInpTen.GetRMS())

hCh11pedInpTen = TH1D("hCh11pedInpTen","hCh11pedInpTen",2048,0,2048)
hCh11pedInpTen.FillN(len(tNoInpTen["Module4_11"]),np.asarray(tNoInpTen["Module4_11"],'d'),np.asarray([1]*len(tNoInpTen["Module4_11"]),'d'))
hCh11pedInpTen.Scale(1/len(tNoInpTen))
hCh11pedInpTen.Rebin(2)
hCh11pedInpTen.Fit("gaus")
print('Pedestal Gate 6 mu s channel 10: ', hCh11pedInpTen.GetMean(), ' RMS: ', hCh11pedInpTen.GetRMS())

text = TLatex(0.2, 0.46,"Using 2249W ADC")
text.SetNDC()
text.SetTextSize(gStyle.GetTextSize()*0.7)
text.SetTextFont(42)

######################################################
#   COMPARISONS ON SAME CHANNEL VARYING GATE WIDTH   #
######################################################

text1 = TLatex(0.2, 0.60,"Gate width")
text1.SetNDC()
text1.SetTextSize(gStyle.GetTextSize())
text1.SetTextFont(42)

# Ch 10 no input
cCh10noinp = TCanvas("Ch10","Ch10",1500,1500)
hFrame = cCh10noinp.DrawFrame(tNoInpSix["Module4_10"].min()*0.9,0.0001,tNoInpTen["Module4_10"].max()*1.02,1.,"Pedestals Ch 10 no input; Channel; Counts")
SetObjectStyle(hCh10pedSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh10pedSix.Draw("hist,same")
SetObjectStyle(hCh10pedTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh10pedTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedSix, '6 #mu s', 'lf')
leg1.AddEntry(hCh10pedTen, '10 #mu s', 'lf')
leg1.Draw("same")
text.Draw()
text1.Draw()
cCh10noinp.SaveAs('/home/marcello/LabFNS1/data/output/Ch10NoInput.pdf')

# Ch11 no input  
cCh11NoInp = TCanvas("Ch11","Ch11",1500,1500)
hFrame = cCh11NoInp.DrawFrame(tNoInpSix["Module4_11"].min()*0.9,0.0001,tNoInpTen["Module4_11"].max()*1.02,1.,"Pedestals Ch 11 no input; Channel; Counts")
SetObjectStyle(hCh11pedSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh11pedSix.Draw("hist,same")
SetObjectStyle(hCh11pedTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh11pedTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh11pedSix, '6 #mu s', 'lf')
leg1.AddEntry(hCh11pedTen, '10 #mu s', 'lf')
leg1.Draw("same")
text.Draw()
text1.Draw()
cCh11NoInp.SaveAs('/home/marcello/LabFNS1/data/output/Ch11NoInput.pdf')

# Ch10 input 
cCh10Inp = TCanvas("Ch10inp","Ch10inp",1500,1500)
hFrame = cCh10Inp.DrawFrame(tInpSix["Module4_10"].min()*0.9,0.0001,tInpTen["Module4_10"].max()*1.02,1.,"Pedestals Ch 10 input S_{1}; Channel; Counts")
SetObjectStyle(hCh10pedInpSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh10pedInpSix.Draw("hist,same")
SetObjectStyle(hCh10pedInpTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh10pedInpTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedInpSix, '6 #mu s', 'lf')
leg1.AddEntry(hCh10pedInpTen, '10 #mu s', 'lf')
leg1.Draw("same")
text.Draw()
text1.Draw()
cCh10Inp.SaveAs('/home/marcello/LabFNS1/data/output/Ch10Input.pdf')

# Ch11 input  
cCh11Inp = TCanvas("Ch11inp","Ch11inp",1500,1500)
hFrame = cCh11Inp.DrawFrame(tInpSix["Module4_11"].min()*0.9,0.0001,tInpTen["Module4_11"].max()*1.02,1.,"Pedestals Ch 11 input S_{G}; Channel; Counts")
SetObjectStyle(hCh11pedInpSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh11pedInpSix.Draw("hist,same")
SetObjectStyle(hCh11pedInpTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh11pedInpTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh11pedInpSix, '6 #mu s', 'lf')
leg1.AddEntry(hCh11pedInpTen, '10 #mu s', 'lf')
leg1.Draw("same")
text.Draw()
text1.Draw()
cCh11Inp.SaveAs('/home/marcello/LabFNS1/data/output/Ch11Input.pdf')

###############################
#   COMPARISONS Ch10 - Ch11   #
###############################

leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
text2 = TLatex(0.2, 0.60,"Channel")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize())
text2.SetTextFont(42)

# gate 6 #mu s no input
cCh10Ch11SixNoInp = TCanvas("Ch10Ch11SixNoInp","Ch10Ch11SixNoInp",1500,1500)
hFrame = cCh10Ch11SixNoInp.DrawFrame(tNoInpSix["Module4_10"].min()*0.7,0.0001,tNoInpSix["Module4_11"].max()*1.3,1.,"Pedestals Ch 10 - Ch 11 no input 6 #mu s; Channel; Counts")
SetObjectStyle(hCh10pedSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh10pedSix.Draw("hist,same")
SetObjectStyle(hCh11pedSix,color=kRed,fillalpha=0.5,linewidth=1)
hCh11pedSix.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedSix, 'Ch 10', 'lf')
leg1.AddEntry(hCh11pedSix, 'Ch 11', 'lf')
leg1.Draw("same")
text.Draw()
text2.Draw()
cCh10Ch11SixNoInp.SaveAs('/home/marcello/LabFNS1/data/output/Ch10Ch11SixNoInput.pdf')

# gate 10 #mu s no input 
cCh10Ch11TenNoInp = TCanvas("Ch10Ch11TenNoInp","Ch10Ch11TenNoInp",1500,1500)
hFrame = cCh10Ch11TenNoInp.DrawFrame(tNoInpTen["Module4_10"].min()*0.7,0.0001,tNoInpTen["Module4_11"].max()*1.3,1.,"Pedestals Ch 10 - Ch 11 no input 10 #mu s; Channel; Counts")
SetObjectStyle(hCh10pedTen,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh10pedTen.Draw("hist,same")
SetObjectStyle(hCh11pedTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh11pedTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedTen, 'Ch10', 'lf')
leg1.AddEntry(hCh11pedTen, 'Ch11', 'lf')
leg1.Draw("same")
text.Draw()
text2.Draw()
cCh10Ch11TenNoInp.SaveAs('/home/marcello/LabFNS1/data/output/Ch10Ch11TenNoInput.pdf')

######################################################
#   COMPARISONS SAME CHANNEL WITH OR WITHOUT INPUT   #
######################################################

text2 = TLatex(0.2, 0.60,"ADC inputs")
text2.SetNDC()
text2.SetTextSize(gStyle.GetTextSize())
text2.SetTextFont(42)

# Ch10 gate input 6 #mu s 
cCh10SixBoth = TCanvas("Ch10SixBoth","Ch10SixBoth",1500,1500)
hFrame = cCh10SixBoth.DrawFrame(tInpSix["Module4_10"].min()*0.7,0.0001,tNoInpSix["Module4_10"].max()*1.3,1.,"Pedestals Ch 10 6 gate #mu s; Channel; Counts")
SetObjectStyle(hCh10pedSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh10pedSix.Draw("hist,same")
SetObjectStyle(hCh10pedInpSix,color=kRed,fillalpha=0.5,linewidth=1)
hCh10pedInpSix.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedSix, 'No input', 'lf')
leg1.AddEntry(hCh10pedInpSix, 'S1', 'lf')
leg1.Draw("same")
text.Draw()
text2.Draw()
cCh10SixBoth.SaveAs('/home/marcello/LabFNS1/data/output/Ch10SixBoth.pdf')

# Ch10 gate input 10 #mu s 
cCh10TenBoth = TCanvas("Ch10TenBoth","Ch10TenBoth",1500,1500)
hFrame = cCh10TenBoth.DrawFrame(tInpTen["Module4_10"].min()*0.7,0.0001,tNoInpTen["Module4_10"].max()*1.3,1.,"Pedestals Ch 10 gate 10 #mu s; Channel; Counts")
SetObjectStyle(hCh10pedTen,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh10pedTen.Draw("hist,same")
SetObjectStyle(hCh10pedInpTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh10pedInpTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedSix, 'No input', 'lf')
leg1.AddEntry(hCh10pedInpSix, 'S1', 'lf')
leg1.Draw("same")
text.Draw()
text2.Draw()
cCh10TenBoth.SaveAs('/home/marcello/LabFNS1/data/output/Ch10TenBoth.pdf')

# Ch11 gate input 6 #mu s 
cCh11SixBoth = TCanvas("Ch11SixBoth","Ch11SixBoth",1500,1500)
hFrame = cCh11SixBoth.DrawFrame(tInpSix["Module4_11"].min()*0.7,0.0001,tNoInpSix["Module4_11"].max()*1.3,1.,"Pedestals Ch 11 gate input 6 #mu s; Channel; Counts")
SetObjectStyle(hCh11pedSix,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh11pedSix.Draw("hist,same")
SetObjectStyle(hCh11pedInpSix,color=kRed,fillalpha=0.5,linewidth=1)
hCh11pedInpSix.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh11pedSix, 'No input', 'lf')
leg1.AddEntry(hCh11pedInpSix, 'SG', 'lf')
leg1.Draw("same")
text.Draw()
text2.Draw()
cCh11SixBoth.SaveAs('/home/marcello/LabFNS1/data/output/Ch11SixBoth.pdf')

# Ch11 gate input 10 #mu s 
cCh11TenBoth = TCanvas("Ch11TenBoth","Ch11TenBoth",1500,1500)
hFrame = cCh11TenBoth.DrawFrame(tInpTen["Module4_11"].min()*0.7,0.0001,tNoInpTen["Module4_11"].max()*1.3,1.,"Pedestals Ch 11 gate input 10 #mu s; Channel; Counts")
SetObjectStyle(hCh11pedTen,color=kAzure+3,fillalpha=0.9,linewidth=1)
hCh11pedTen.Draw("hist,same")
SetObjectStyle(hCh11pedInpTen,color=kRed,fillalpha=0.5,linewidth=1)
hCh11pedInpTen.Draw("hist,same")
leg1 = TLegend(0.185, 0.50, 0.85, 0.59)
leg1.SetTextFont(42)
leg1.SetTextSize(gStyle.GetTextSize()*0.7)
leg1.SetFillStyle(0)
leg1.AddEntry(hCh10pedTen, 'No input', 'lf')
leg1.AddEntry(hCh10pedInpTen, 'With input', 'lf')
leg1.Draw("same")
text.Draw()
text2.Draw()
cCh11TenBoth.SaveAs('/home/marcello/LabFNS1/data/output/Ch11TenBoth.pdf')