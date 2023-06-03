import numpy as np
import ctypes

from ROOT import TRandom3, gRandom, TH1D, TFile, TF1, TCanvas, TLatex, gStyle, TLegend

from math import acos, atan, cos, sin, tan, sqrt, radians



def GenerateDecay(theta):
    '''
    Generate photon emitted in a cone of opening theta centered on the z axis

    Parameters
    ----------
        theta (float): opening of the cone

    Returns 
    ------
        [x, y, z] (list[float]): versor describing the direction of the emitted photon
    '''

    x = ctypes.c_double()
    y = ctypes.c_double()
    z = ctypes.c_double()
    z.value=0

    while np.arccos(z.value) > abs(theta):     gRandom.Sphere(x,y,z,1.) 
    return [x.value, y.value, z.value]

def xzPlaneRotation(phi, vector):
    '''
    Rotate a vector by a phi angle in the xz plane

    Parameters
    ----------
        phi (float): angle to rotate your vector by
        vector (list[float]): [x, y, z], 3d vector to rotate

    Returns
    -------
        [xR, yR, zR] (list[float]): rotated vector
    '''

    rotationMatrix = [[np.cos(phi), 0, np.sin(phi)],
                      [0, 1, 0],
                      [-np.sin(phi), 0, np.cos(phi)]]

    xR = 0
    yR = 0
    zR = 0
    
    for i in range(3):
        xR += rotationMatrix[0][i] * vector[i]
        yR += rotationMatrix[1][i] * vector[i]
        zR += rotationMatrix[2][i] * vector[i]

    return [xR, yR, zR]

def generateMC(kNEvents, kRadius, kDistance, outfile, seed=42):
    '''
    '''
    
    kTan = kRadius/kDistance
    kTheta = np.arctan(kTan)
    
    gRandom = TRandom3()
    gRandom.SetSeed(seed)
    
    angles = list(np.linspace(-32,32,129))
    histo = TH1D("toyMC","toy MC", 137,-34,34)
    
    for alpha in angles:
        for i in range(kNEvents):
            
            if i%10000 == 0:    print(f'Processing event {i}, angle = {alpha}\r')


            photonDirection = GenerateDecay(kTheta)
            newPhotonDirection = xzPlaneRotation(-radians(alpha), photonDirection)    # photon direction in the second scintillator FR

            # check if the photon is in the cone of opening theta for the second scintillator and fill the histogram
            if np.arccos(newPhotonDirection[2]) < abs(kTheta):    histo.Fill(alpha)

    outfile = TFile("data/output/ToyMCgio.root",'recreate')
    histo.Write()
    outfile.Close()

def fitMC(outfile):
    '''
    Fit the MC distribution with a function derived from geometrical considerations and save it on canvas on a .root file
    '''

    MCinfile = TFile('data/output/ToyMCgio.root')
    histMC = MCinfile.Get('toyMC')
    histMC.SetFillColorAlpha(863, 0.4)
    histMC.SetTitle('Monte Carlo; Angles (deg); Counts (a. u.)')
    canvas = TCanvas('toyMC', 'Monte Carlo; Angles (deg); Counts (a. u.)', 1500, 1500)
    canvas.DrawFrame(-34, 0, 34, 12000, 'Monte Carlo; Angles (deg); Counts (a. u.)')
    
    # geom func
    fitMCg = TF1('fitMCg', '[0]*( 2/pi*acos([1]/[2]*sin(abs(pi*x/180)/2)) - 2*[1]*sin(abs(pi*x/180)/2)/(pi*[2]*[2])* sqrt( [2]*[2] - [1]*[1]*sin(abs(pi*x/180)/2)*sin(abs(pi*x/180)/2) ) )', -28, 28)
    fitMCg.SetParNames('Norm','R', 'r')
    fitMCg.SetParameters(10000, 10, 2.54)
    fitMCg.SetLineColor(797)

    histMC.Fit(fitMCg, 'b', '', -28, -28)
    print('Fit results:')
    print(f'#chi^2 / NDF = {fitMCg.GetChisquare():#.2f} / {fitMCg.GetNDF()}')

    leg = TLegend(0.15, 0.65, 0.4, 0.85)
    leg.SetTextFont(42)
    leg.SetTextSize(gStyle.GetTextSize()*0.9)
    leg.SetFillStyle(0)
    leg.AddEntry(histMC, 'Monte Carlo', 'lf')
    leg.AddEntry(fitMCg, 'Fit function', 'lf')

    gStyle.SetOptStat(0)
    text1 = TLatex(0.65, 0.70, 'Fit results:')
    text2 = TLatex(0.65, 0.66, f'[Norm] = {fitMCg.GetParameter(0):#.0f} #pm {fitMCg.GetParError(0):#.0f}')
    text3 = TLatex(0.65, 0.62, f'[R] = ({fitMCg.GetParameter(1):#.0f} #pm {fitMCg.GetParError(1):#.0f}) cm')
    text4 = TLatex(0.65, 0.58, f'[r] = ({fitMCg.GetParameter(2):#.1f} #pm {fitMCg.GetParError(2):#.1f}) cm')
    text5 = TLatex(0.65, 0.54, f'#chi^2 / NDF = {fitMCg.GetChisquare():#.0f} / {fitMCg.GetNDF()}')

    histMC.Draw('hist')
    fitMCg.Draw('same')
    leg.Draw('same')

    for text in [text1, text2, text3, text4, text5]:   
        text.SetNDC()
        text.SetTextSize(gStyle.GetTextSize()*0.8)
        text.SetTextFont(42)
        text.Draw()

    outfile.cd()
    histMC.Write()
    canvas.Write()
    canvas.SaveAs('data/output/Figures/GammaCoincidence/MCfit.pdf')

if __name__ == '__main__':
   
    kNEvents = 10000
    kRadius = 2.54
    kDistance = 10

    #generateMC(kNEvents, kRadius, kDistance)
    outfile = TFile('data/output/Gamma/ToyMCfit.root', 'recreate')
    fitMC(outfile)

    
