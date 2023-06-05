import pandas as pd
import numpy as np
import sys
#import argparse

sys.path.append('Python/utils')

from StyleFormatter import SetObjectStyle
from ROOT import TH1D, TCanvas, TLegend, TPad, TF1, gStyle, TPaveStats, gPad, TGraphErrors, TLatex, TFile 
from ROOT import kSpring, kBlue, kGreen, kRed, kBlue, kOrange, kBlack, kAzure,kGray, kMagenta

#________________________
# GLOBAL PARAMETERS

# calibration values
BB = -33 # offset
AA = 0.3176 # slope, keV^-1


#________________________


def CreateHist(infile, histName):
    '''
    Reads data from a .mca file and fills a histogram with it. Live time of the measurement is also returned.

    Parameters
    ----------
        infile (str): path to the file to read from
        histName (str): name of the histogram created
    
    Returns
    -------
        hist (TH1D): histogram filled with values from the file
        data (list[float]): data read from the file
        live_time (float): time passed during data acquisition (s)
    '''

    data = []
    live_time = 0

    with open(infile, 'r', errors='ignore') as file:#with chiude i automatico il file

        for line in file:
            if line.startswith('LIVE_TIME'):
                live_time = float(line.split('-')[-1].strip())
                break

        lines = file.readlines()[1:-1]
        start_index = lines.index('<<DATA>>\n') + 1
        end_index = lines.index('<<END>>\n')

        for line in lines[start_index:end_index]:
            value = int(line.strip())  # Convert the line to an integer
            data.append(value)  # Append the value to the list

    hist = TH1D(histName,"Hist",len(data),0,len(data))
    for i, x in enumerate(data): 
        hist.Fill(i, x)
        hist.SetBinError(i, np.sqrt(x))
    
    return hist, data, live_time

def ChannelToEnergy(chn, gain):
    '''
    Convert channel to energy using calibration results and takng into account the gain used for that acquisition
    '''
    return (200/gain)*(chn-BB)/AA

def HistoFromCtoE(data, histName, gain):
    '''
    Converts data from channels to energies and fills a histogram with it

    Parameters
    ----------
        data (list[float]): data to convert
        aa, bb (float): slope and offset of the calibration line
        gain (int): gain used (calibration was done with gain = 1000)
    
    Returns
    -------
        histE (TH1D): histogram filled with data after conversion in energy
    '''

    nbin = len(data)    
    histE = TH1D(histName,"HistE",nbin,ChannelToEnergy(0, gain),ChannelToEnergy(nbin, gain))
    
    for i, x in enumerate(data): 
        histE.Fill(ChannelToEnergy(i, gain)+1/(2*AA)*(200/gain), x)   # fill center of bin to avoid filling the same bin twice (root does strange things with bin edges)
        histE.SetBinError(i, np.sqrt(x))

    return histE 

def StudyNaSpectrum1(hist, outFile, live_time):
    '''
    Performs a study of the Na spectrum (first data acquisition), creating a histogram, fitting peaks and adding legends to the output. 

    Parameters
    ----------
        hist (TH1D): histogram with Na spectrum
        outFile (TFile): output file
        live_time (float): acquisition time
    '''

    canvas = TCanvas('Na1canvas', '', 1500, 1500)
    canvas.DrawFrame(50, 0, 1300, 420, 'Sodium spectrum; Energy (keV); Counts (a. u.)')
    
    hist.Draw('hist')

    outFile.cd()
    hist.Write()
    canvas.Write()

def StudyNaSpectrum2(hist, outFile, live_time):
    '''
    Performs a study of the Na spectrum (second data acquisition), creating a histogram, fitting peaks and adding legends to the output. 

    Parameters
    ----------
        hist (TH1D): histogram with Na spectrum
        outFile (TFile): output file
        live_time (float): acquisition time
    '''

    gStyle.SetOptStat(0)

    canvas = TCanvas('Na2canvas', '', 1500, 1500)
    canvas.DrawFrame(50, 0.01, 800, 120, 'Sodium spectrum; Energy [keV]; Counts [a. u.]')

    hist.SetLineColor(kOrange-3)
    hist.SetFillColorAlpha(kOrange-3, 0.4)
    hist.SetTitle('Sodium spectrum (with plastic cover); Energy [keV]; Counts [a. u.]')
    hist.Draw('hist')
    canvas.SetLogy()
    canvas.SaveAs('data/output/Diamond/NaPlastic.pdf')

    # Compton edge 341 keV
    compton1 = TF1('compton1', '[0] + [2]/(  1 + exp( (x-[1])/[3] )  )', 320, 420)
    compton1.SetParNames('y_0', 'x_0', 'a', 'b')
    compton1.SetParameters(50, 341, 150, 4)
    compton1.SetParLimits(0, 30, 70)
    compton1.SetParLimits(1, 330, 370)
    compton1.SetParLimits(2, 120, 180)
    compton1.SetParLimits(3, 0.001, 10)
    compton1.SetLineColor(kBlue-3)
    hist.Fit(compton1, 'rm', '', 300, 450)

    leg1 = TLegend(0.15, 0.5, 0.55, 0.85)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.7)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(hist, '^{22}Na Spectrum (with plastic cover)', 'lf')
    leg1.AddEntry(compton1, 'N(E) = [Bkg] + #frac{[a]}{1 + exp#left(#frac{E - [E_{C}]}{[b]}#right)}', 'lf')

    text0 = TLatex(0.55, 0.80, '#bf{Acquisition time:} '+f'{live_time:#.0f} s')
    text1 = TLatex(0.55, 0.75, '#bf{Fit results:}')
    text2 = TLatex(0.55, 0.70, f'[Bkg] = {compton1.GetParameter(0):#.1f} #pm {compton1.GetParError(0):#.1f}')
    text3 = TLatex(0.55, 0.65, '[E_{C}] = '+f'({compton1.GetParameter(1):#.1f} #pm ) keV')
    text4 = TLatex(0.55, 0.60, f'[a] = ({compton1.GetParameter(2):#.0f} #pm {compton1.GetParError(2):#.0f})')
    text5 = TLatex(0.55, 0.55, f'[b] = ({compton1.GetParameter(3):#.1f} #pm {compton1.GetParError(3):#.1f}) keV')
    text6 = TLatex(0.55, 0.50, f'#chi^2 / NDF = {compton1.GetChisquare():#.0f} / {compton1.GetNDF()}')

    canvasCompton1 = TCanvas('Na2canvasCompton1', '', 1500, 1500)

    hist.GetXaxis().SetRangeUser(200, 600)
    hist.GetYaxis().SetRangeUser(0, 500)
    hist.SetTitle('Sodium spectrum - Compton edge (511 keV); Energy (keV); Counts (a. u.)')
    hist.Draw('hist')
    compton1.Draw('same')
    leg1.Draw('same')

    for text in [text0, text1, text2, text3, text4, text5, text6]:   
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.8)
        text.SetTextFont(42)
        text.Draw()

    # Compton edge 841 keV
    compton2 = TF1('compton2', '[0] + [2]/(  1 + exp( (x-[1])/[3] )  )', 800, 900)
    compton2.SetParNames('y_0', 'x_0', 'a', 'b')
    compton2.SetParameters(1, 864, 9, 4)
    compton2.SetParLimits(0, 0, 3)
    compton2.SetParLimits(1, 800, 900)
    compton2.SetParLimits(2, 5, 15)
    compton2.SetParLimits(3, 0.001, 10)
    compton2.SetLineColor(kBlue-3)
    hist.Fit(compton2, 'lrm', '', 800, 950)

    leg2 = TLegend(0.15, 0.5, 0.55, 0.85)
    leg2.SetTextFont(42)
    leg2.SetTextSize(gStyle.GetTextSize()*0.7)
    leg2.SetFillStyle(0)
    leg2.SetBorderSize(0)
    leg2.AddEntry(hist, '^{22}Na Spectrum (with plastic cover)', 'lf')
    leg2.AddEntry(compton2, 'N(E) = [Bkg] + #frac{[a]}{1 + exp#left(#frac{E - [E_{C}]}{[b]}#right)}', 'lf')

    text0 = TLatex(0.55, 0.80, '#bf{Acquisition time:} '+f'{live_time:#.0f} s')
    text1 = TLatex(0.55, 0.75, '#bf{Fit results:}')
    text2 = TLatex(0.55, 0.70, f'[Bkg] = {compton2.GetParameter(0):#.1f} #pm {compton2.GetParError(0):#.1f}')
    text3 = TLatex(0.55, 0.65, '[E_{C}] = '+f'({compton2.GetParameter(1):#.1f} #pm {compton2.GetParError(1):#.1f}) keV')
    text4 = TLatex(0.55, 0.60, f'[a] = ({compton2.GetParameter(2):#.0f} #pm {compton2.GetParError(2):#.0f})')
    text5 = TLatex(0.55, 0.55, f'[b] = ({compton2.GetParameter(3):#.1f} #pm {compton2.GetParError(3):#.1f}) keV')
    text6 = TLatex(0.55, 0.50, f'#chi^2 / NDF = {compton2.GetChisquare():#.0f} / {compton2.GetNDF()}')

    canvasCompton2 = TCanvas('Na2canvasCompton2', '', 1500, 1500)
    
    hist.GetXaxis().SetRangeUser(700, 1200)
    hist.GetYaxis().SetRangeUser(0, 40)
    hist.SetTitle('Sodium spectrum - Compton edge (1274 keV); Energy (keV); Counts (a. u.)')
    hist.Draw('hist')
    compton2.Draw('same')
    leg2.Draw('same')

    for text in [text0, text1, text2, text3, text4, text5, text6]:   
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.8)
        text.SetTextFont(42)
        text.Draw()

    outFile.cd()
    hist.Write()
    canvas.Write()
    canvasCompton1.Write()
    canvasCompton1.SaveAs('data/output/Diamond/NaCompton1.pdf')
    canvasCompton2.Write()
    canvasCompton2.SaveAs('data/output/Diamond/NaCompton2.pdf')

def PlasticComparison(hist1, hist2, outFile):
    '''
    Creates a histogram from the difference of two other histograms given as inputs. Draws all of them on a canvas
    split in two parts and then saves everythong to a root file

    Parameters
    ----------
        hist1, hist2 (TH1): histograms whose difference will be computed
        outFile (TFile): file where the canvas will be written to
    '''
    
    histDifference = hist1.Clone()
    histDifference.Add(hist2,-1.)      # Performs subtraction
    histDifference.SetLineColor(kGreen-2)
    histDifference.SetFillColorAlpha(kGreen-2, 0.5)

    SizeLittlePad = 0.4   # size in %
    canvas = TCanvas('plasticComp', '', 1500, 1500)
    
    pad = TPad("pad","pad",0.,SizeLittlePad,1.,1.)
    pad.SetBottomMargin(0.)
    pad.Draw()
    
    padDiff = TPad("padDiff","padDiff",0.,0.,1.,SizeLittlePad)
    padDiff.SetTopMargin(0.)
    padDiff.SetBottomMargin(0.3)
    padDiff.Draw()

    pad.cd()
    hFrame = pad.DrawFrame(0, 0, 800, 3.2, "^{22}Na spectrum - difference using a plastic cover;Energy [keV];Rate [Hz]")
    hFrame.GetYaxis().SetTitleSize(0.05)
    hFrame.GetYaxis().SetLabelSize(0.05)
    hFrame.GetYaxis().SetTitleOffset(0.61)
    hist1.SetLineColor(kAzure-3)
    hist1.SetFillColorAlpha(kAzure-3, 0.4)
    hist2.SetLineColor(kOrange-3)
    hist2.SetFillColorAlpha(kOrange-3, 0.6)
    hist1.Draw("hist same")
    hist2.Draw("hist same")

    leg = TLegend(0.5, 0.5, 0.85, 0.85)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hist1, '^{22}Na Spectrum (without plastic cover)', 'lf')
    leg.AddEntry(hist2, '^{22}Na Spectrum (with plastic cover)', 'lf')
    leg.AddEntry(histDifference, 'Difference', 'lf')
    leg.Draw("same")

    padDiff.cd()
    hFrameDiff = pad.DrawFrame(0, 0, 800, 3.2, ";Energy [keV];Difference") 
    hFrameDiff.GetYaxis().SetTitleSize(0.08)
    hFrameDiff.GetXaxis().SetTitleSize(0.08)
    hFrameDiff.GetYaxis().SetLabelSize(0.08)
    hFrameDiff.GetXaxis().SetLabelSize(0.08)
    hFrameDiff.GetYaxis().SetTitleOffset(0.41)
    hFrameDiff.GetXaxis().SetTitleOffset(0.8)
    hFrameDiff.SetTickLength(0.06,'X')
    hFrameDiff.SetTickLength(0.04,'Y')
    hFrameDiff.GetYaxis().SetNdivisions(3,5,0,True)

    histDifference.Draw("hist same")

    canvas.cd()
    canvas.Modified()
    canvas.Update()

    outFile.cd()
    histDifference.Write()
    canvas.Write()
    canvas.SaveAs('data/output/Diamond/NaDifference.pdf')

def RateHist(data, live_time, histName, gain=1000):
    '''
    Takes in data (in energy) and creates a rate histogram 

    Parameters
    ----------
        data (list[float]): counts for each bin oh the histogram
        live_time (float): data acquisition time
        histName (str): name of the histogram
        gain (int): gain used in data acquisition (necessary to convert channels to energy)

    Returns
    -------
        rateHist (TH1D): histogram of rates
    '''

    nbin = len(data)
    rateHist = TH1D(histName, '', nbin, ChannelToEnergy(0, gain), ChannelToEnergy(nbin, gain))
    for i, x in enumerate(data):
        rateHist.Fill(ChannelToEnergy(i, gain)+1/(2*AA)*(200/gain), x/live_time)
        rateHist.SetBinError(i, np.sqrt(x)/live_time)

    return rateHist

if __name__ == '__main__':

    # output file initialization    
    outfilePath = 'data/output/Diamond/NaStudy.root'
    root_file = TFile(outfilePath, 'recreate')
    print(f'ROOT file created at {outfilePath}')

    # first sodium data acquisition (e- visible)
    infilePath1 = 'data/input/Diamonds/sodio1.mca'
    histNa1, dataNa1, live_timeNa1 = CreateHist(infilePath1, 'Na1Spectrum')
    histNa1E = HistoFromCtoE(dataNa1, 'Na1SpectrumE', gain=1000)
    histNa1.Rebin(8)
    histNa1E.Rebin(8)
    #StudyNaSpectrum1(histNa1, root_file, live_timeNa1)
    StudyNaSpectrum1(histNa1E, root_file, live_timeNa1)

    # second sodium data acquisition (e- visible)
    infilePath2 = 'data/input/Diamonds/sodio2merc.mca'
    histNa2, dataNa2, live_timeNa2 = CreateHist(infilePath2, 'Na2Spectrum')
    histNa2E = HistoFromCtoE(dataNa2, 'Na2SpectrumE', gain=1000)
    histNa2.Rebin(8)
    histNa2E.Rebin(8)
    #StudyNaSpectrum2(histNa2, root_file, live_timeNa2)
    StudyNaSpectrum2(histNa2E, root_file, live_timeNa2)

    # plastic comparison
    rateHistNa1 = RateHist(dataNa1, live_timeNa1, 'RateNa1SpectrumE')
    rateHistNa2 = RateHist(dataNa2, live_timeNa2, 'RateNa2SpectrumE')
    rateHistNa1.Rebin(8)
    rateHistNa2.Rebin(8)
    PlasticComparison(rateHistNa1, rateHistNa2, root_file)



    root_file.Close()


    '''

    infilename='data/input/Diamonds/Tuesday/sorgente_tripla.mca'
    c = TCanvas('c','c',1000,1000)
    leg = TLegend(0.435, 0.71, 0.85, 0.59)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.7)
    leg.SetFillStyle(0)
    histo=CreateHist(infilename,data)
    histo.Draw("E")

    gStyle.SetOptFit(1111)
    Americio = TF1('Americio', "gaus", 1700, 1720)
    Curio = TF1('CUrio', "gaus", 1800, 1825)
    #Neptunio1=TF1('Neptunio1', "gaus", 1430, 1460)
    #Neptunio2=TF1('Neptunio2', "gaus", 1470, 1500)
    #Neptunio3=TF1('Neptunio2', "gaus", 1510, 1525)


    histo.Fit(Americio,"RM")
    c.Update()
    histo.Fit(Curio,"RM")
    c.Update()
    #histo.Fit(Neptunio1,"RM")
    #c.Update()
    #histo.Fit(Neptunio2,"RM")
    #c.Update()
    #histo.Fit(Neptunio3,"RM")

    Neptunio=TF1('Neptunio', "gaus", 1470, 1500)
    #Neptunio2picchi=TF1("Neptunio2picchi","gaus(0)+gaus(3)",1470,1500)
    #Neptunio.SetParNames("Norm_{1}", "#mu_{1}", "#sigma_{1}", "Norm_{2}", "#mu_{2}", "#sigma_{2}", "Norm_{3}", "#mu_{3}", "#sigma_{3}")
    #Neptunio.SetParameter(1,Neptunio1.GetParameter(1))
    #Neptunio.SetParLimits(1,1443,1444)
    #Neptunio.SetParameter(4,Neptunio2.GetParameter(1))
    #Neptunio.SetParLimits(4,1485,1486)
    #Neptunio.SetParameter(7,Neptunio3.GetParameter(1))
    #Neptunio.SetParLimits(7,1515,1516)
    #Neptunio.SetParameter(2,Neptunio1.GetParameter(2))
    #Neptunio.SetParLimits(2,5.0,5.6)
    #Neptunio.SetParameter(5,Neptunio2.GetParameter(2))
    #Neptunio.SetParLimits(5,5.6,6.6)
    #Neptunio.SetParameter(8,Neptunio3.GetParameter(2))
    #Neptunio.SetParLimits(8,2.5,3)

    #Neptunio2picchi.SetParameters(1,1483)
    #Neptunio2picchi.SetParameters(4,1490)

  
    #Neptunio.SetParameter(3,Neptunio1.GetParameter(3))
    #Neptunio.SetParameter(6,Neptunio2.GetParameter(3))
    #Neptunio.SetParameter(9,Neptunio3.GetParameter(3))


    c.Update()
    histo.Fit(Neptunio,"RM")
    
    
    Americio.SetLineColor(kGreen)
    Curio.SetLineColor(kOrange-3)
    Neptunio.SetLineColor(kMagenta)
    #Neptunio1.SetLineColor(kRed)
    #Neptunio2.SetLineColor(kRed+2)
    #Neptunio3.SetLineColor(kRed+4)
    #Neptunio.SetLineColor(kOrange-3)

    Americio.Draw("same")
    Curio.Draw("same")
    Neptunio.Draw("same")
    #Neptunio3.Draw("same")
    #Neptunio2.Draw("same")
   # Neptunio1.Draw("same")
    #Neptunio.Draw("same")

    #print("primo picco= ",Neptunio1.GetChisquare()/Neptunio1.GetNDF(),end='\n') 
    #print("secondo picco= ",Neptunio2.GetChisquare()/Neptunio2.GetNDF(),end='\n') 
    #print("terzo picco= ",Neptunio3.GetChisquare()//Neptunio3.GetNDF(),end='\n') 
    gStyle.SetOptFit(1111)
    stat = TPaveStats()
    stat1 = TPaveStats()
    stat = Americio.FindObject("stats")
    stat1 = Curio.FindObject("stats")
    if(stat and stat1):
        stat.SetTextColor(kBlue+3);
        stat1.SetTextColor(kOrange-3);
        height = stat1.GetY2NDC() - stat1.GetY1NDC();
        stat1.SetY1NDC(stat.GetY1NDC() - height);
        stat1.SetY2NDC(stat.GetY1NDC() );
        stat1.Draw('same');
        stat.Draw('same');
    leg.AddEntry(histo, "Data from triple source", 'lf')
    leg.AddEntry(Neptunio, "Gauss: fit on ^{237}Np", 'lf')
    leg.AddEntry(Americio, "Gauss: fit on ^{241}Am", 'lf')
    leg.AddEntry(Curio, "Gauss: fit on ^{244}Cm", 'lf')
    leg.Draw("same")

    text =TLatex(0.30, 0.7,"Diamond detector, spectrum of triple source ")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text1 =TLatex(0.30, 0.62,"Acquisition time:4000s")
    text1.SetNDC()
    text1.SetTextSize(gStyle.GetTextSize()*0.7)
    text1.SetTextFont(42)
    text1.Draw()
    
    
    c.Modified()
    c.Update()
    root_file.cd()
    c.Write()
    gPad.Update()

    c1 = TCanvas('c1','c1',1000,1000)
    c1.cd()
    points=[1710,1810,1485 ]
    sigmapoint=[5,6,6]
    energy=[5486,5805.0,4780.70]
    energyerr=[0.,0.,0.]
    retcal = TGraphErrors(3,np.asarray(energy,'d'),np.asarray(points,'d'),
                     np.asarray(energyerr,'d'),np.asarray(sigmapoint,'d'))
    retta=TF1("retta","[0]+[1]*x",-10,6000)
    retcal.SetTitle("Retta calibrazione")
    retcal.GetXaxis().SetTitle("Energy [keV]")
    retcal.GetYaxis().SetTitle("Channels")
    retcal.Fit(retta,"RM")
    retcal.Draw("AP")
    retcal.SetMarkerStyle(8)
    retcal.SetMarkerSize(1.2)
    retta.Draw("same")
    text =TLatex(0.30, 0.7,"Calibration Fit")
    text.SetNDC()
    text.SetTextSize(gStyle.GetTextSize())
    text.SetTextFont(42)
    text.Draw()
    text2 =TLatex(0.30, 0.62,"Diamond detector, with triple source")
    text2.SetNDC()
    text2.SetTextSize(gStyle.GetTextSize()*0.7)
    text2.SetTextFont(42)
    text2.Draw()
    text3 =TLatex(0.30, 0.56,"chn= a*Energy + b")
    text3.SetNDC()
    text3.SetTextSize(gStyle.GetTextSize()*0.7)
    text3.SetTextFont(42)
    text3.Draw()
    text4 =TLatex(0.30, 0.48,"a=(0.3207 #pm 0.0008) keV^{-1}")
    text4.SetNDC()
    text4.SetTextSize(gStyle.GetTextSize()*0.7)
    text4.SetTextFont(42)
    text4.Draw()
    text5 =TLatex(0.30, 0.40,"b= (-5*10^{1} #pm 5*10^{1}) chn")
    text5.SetNDC()
    text5.SetTextSize(gStyle.GetTextSize()*0.7)
    text5.SetTextFont(42)
    text5.Draw()
    c1.Modified()
    c1.Update()
    root_file.cd()
    c1.Write()

    c2 = TCanvas('c2','c2',1000,1000)
    c2.cd()
    Neptunio2picchi1=TF1("Neptunio2picchi1","gaus",1470,1500)
    Neptunio2picchi2=TF1("Neptunio2picchi1","gaus",1470,1500)
    Neptunio2picchi=TF1("Neptunio2picchi","gaus(0)+gaus(3)+gaus(6)",1470,1500)
    Neptunio2picchi.SetLineColor(kBlack)
    Neptunio2picchi1.SetLineColor(kRed)
    Neptunio2picchi2.SetLineColor(kSpring)
    Neptunio2picchi.SetParLimits(0,0,1000)
    Neptunio2picchi.SetParameter(0,147)
    Neptunio2picchi.SetParameter(2,4)
    Neptunio2picchi.SetParLimits(1,1481,1484)
    Neptunio2picchi.SetParameter(4,1490)
    Neptunio2picchi.SetParameter(3,154)
    Neptunio2picchi.SetParameter(5,5)
    Neptunio2picchi.SetParLimits(4,1485,1489)
    histo.Fit(Neptunio2picchi,"RM")
    Neptunio2picchi1.SetParameters(Neptunio2picchi.GetParameter(0),Neptunio2picchi.GetParameter(1),Neptunio2picchi.GetParameter(2))
    Neptunio2picchi2.SetParameters(Neptunio2picchi.GetParameter(3),Neptunio2picchi.GetParameter(4),Neptunio2picchi.GetParameter(5))
    #histo.Fit(Neptunio2picchi1,"RM")
    #histo.Fit(Neptunio2picchi2,"RM")
    histo.Draw("E")

    Neptunio2picchi.Draw("same")
    Neptunio2picchi1.Draw("same")
    Neptunio2picchi2.Draw("same")
    root_file.cd()
    c2.Write()

    c3 = TCanvas('c3','c3',1000,1000)
    c3.cd()
    histE =HistoFromCtoE(data,retta.GetParameter(1),retta.GetParameter(0),histo.GetNbinsX())

    histE.GetXaxis().SetTitle("Energy [keV]")
    histE.GetYaxis().SetTitle("Counts")
    Curio1=TF1("Curio1","gaus",5715,5850)
    Curio2=TF1("Curio2","gaus",5715,5850)
    CurioTot=TF1("CurioTot","gaus(0)+gaus(3)+[6]",5715,5850)
    CurioTot.SetParLimits(0,0,150)
    CurioTot.SetParameter(1,5763)
    CurioTot.SetParLimits(2,1,20)
    CurioTot.SetParLimits(4,5803,5807)
    CurioTot.SetParLimits(1,5760,5767)
    CurioTot.SetParameter(5,15)
    histE.Fit(CurioTot,"RM")
    Curio1.SetParameters(CurioTot.GetParameter(0),CurioTot.GetParameter(1),CurioTot.GetParameter(2))
    Curio2.SetParameters(CurioTot.GetParameter(3),CurioTot.GetParameter(4),CurioTot.GetParameter(5))
    CurioTot.SetLineColor(kRed+3)
    Curio1.SetLineColor(kRed)
    Curio2.SetLineColor(kRed+2)
    histE.Draw("E")
    CurioTot.Draw("same")
    Curio1.Draw("same")
    Curio2.Draw("same")

    Americio1=TF1("Americio1","gaus",5430,5540)
    Americio2=TF1("Americio2","gaus",5430,5540)
    #Americio1=TF1("Americio2","gaus",5410,5540)
    AmericioTot=TF1("AmericioTot","gaus(0)+gaus(3)+[6]",5425,5540)
    AmericioTot.SetParLimits(0,0,150)
    AmericioTot.SetParLimits(1,5440,5450)
    AmericioTot.SetParLimits(4,5482,5499)
    AmericioTot.SetParameter(5,15)
    histE.Fit(AmericioTot,"RM")
    Americio1.SetParameters(AmericioTot.GetParameter(0),AmericioTot.GetParameter(1),AmericioTot.GetParameter(2))
    Americio2.SetParameters(AmericioTot.GetParameter(3),AmericioTot.GetParameter(4),AmericioTot.GetParameter(5))
    #mericio3.SetParameters(AmericioTot.GetParameter(6),AmericioTot.GetParameter(7),AmericioTot.GetParameter(8))
    AmericioTot.SetLineColor(kGreen)
    Americio1.SetLineColor(kRed)
    Americio2.SetLineColor(kGreen+2)
    #Americio2.SetLineColor(kGreen+1)
    histE.Draw("E")
    AmericioTot.Draw("same")
    Americio1.Draw("same")
    Americio2.Draw("same")
    Americio3.Draw("same")

    NEptunioo1=TF1("NEptunioo1","gaus",4600,4910)
    NEptunioo2=TF1("NEptunioo2","gaus",4600,4910)
    NEptunioo3=TF1("NEptunioo3","gaus",4600,4910)
    NEptunioo4=TF1("NEptunioo4","gaus",4600,4910)
    NEptuniooTot=TF1("NEptuniooTot","gaus(0)+gaus(3)+gaus(6)+gaus(9) +[12]",4600,4910)
    NEptuniooTot.SetParLimits(4,4767,4780)
    NEptuniooTot.SetParLimits(7,4780,4791)
    NEptuniooTot.SetParLimits(10,4870,4880)
    NEptuniooTot.SetParLimits(1,4640,4646)
    NEptuniooTot.SetParLimits(2,0.5,100)
    NEptuniooTot.SetParLimits(5,0,100)
    NEptuniooTot.SetParLimits(8,1,30)
    NEptuniooTot.SetParLimits(11,1,10)
    NEptuniooTot.SetParLimits(0,1,40)
    NEptuniooTot.SetParLimits(6,0,130)
    NEptuniooTot.SetParLimits(3,1,60)
    NEptuniooTot.SetParLimits(9,1,120)
    
    #NEptuniooTot.SetParLimits(7,4785,4790)
    #NEptuniooTot.SetParLimits(6,0,170)
    #NEptuniooTot.SetParLimits(8,1,8)
    NEptuniooTot.SetParameter(5,15)
    histE.Fit(NEptuniooTot,"RM")
    NEptunioo1.SetParameters(NEptuniooTot.GetParameter(0),NEptuniooTot.GetParameter(1),NEptuniooTot.GetParameter(2))
    NEptunioo2.SetParameters(NEptuniooTot.GetParameter(3),NEptuniooTot.GetParameter(4),NEptuniooTot.GetParameter(5))
    NEptunioo3.SetParameters(NEptuniooTot.GetParameter(6),NEptuniooTot.GetParameter(7),NEptuniooTot.GetParameter(8))
    NEptunioo4.SetParameters(NEptuniooTot.GetParameter(9),NEptuniooTot.GetParameter(10),NEptuniooTot.GetParameter(11))
    NEptuniooTot.SetLineColor(kBlack)
    NEptunioo1.SetLineColor(kGray)
    NEptunioo2.SetLineColor(kGray+1)
    NEptunioo3.SetLineColor(kBlue)
    NEptunioo4.SetLineColor(kRed)
    histE.Draw("E")
    NEptuniooTot.Draw("same")
    NEptunioo1.Draw("same")
    NEptunioo2.Draw("same")
    NEptunioo3.Draw("same")
    NEptunioo4.Draw("same")



    leg1 = TLegend(0.435, 0.71, 0.85, 0.59)
    leg1.SetTextFont(42)
    leg1.SetTextSize(gStyle.GetTextSize()*0.4)
    leg1.SetFillStyle(0)
    leg1.AddEntry(histE, "Data from triple source", 'lf')
    leg1.AddEntry(NEptunioo1, "Gauss1: ^{237}Np 4771 keV peak", 'lf')
    leg1.AddEntry(NEptunioo2, "Gauss2: ^{237}Np 4788 keV peak", 'lf')
    leg1.AddEntry(NEptunioo3, "Gauss3: ^{237}Np 4640 keV peak", 'lf')
    leg1.AddEntry(NEptunioo4, "Gauss4: ^{237}Np 4872 keV peak", 'lf')
    leg1.AddEntry(NEptuniooTot, "Gauss1 + Gauss2 + Gauss3 + Gauss4 : fit on ^{237}Np  peaks", 'lf')
    leg1.Draw("same")
    c3.SaveAs('test.png')
    input()
    

    '''