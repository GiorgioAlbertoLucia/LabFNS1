import numpy as np
import ctypes

from ROOT import TRandom3, gRandom, TH1D, TFile, TF1, TCanvas

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
    '''

    MCinfile = TFile('data/output/ToyMCgio.root')
    histMC = MCinfile.Get('toyMC')
    canvas = TCanvas('toyMC', 'toyMC; Angles (deg); Counts (a. u.)')
    
    # pol3
    #fitMC1 = TF1('fitMC1', '([0] + [1]*x + [2]*x*x + [3]*x*x*x)', 0, 28)
    #fitMC1.SetParNames('p0', 'p1', 'p2', 'p3')
    #fitMC1.SetParameters(9900, -400, -4.9, 0.23)
#
    #histMC.Fit(fitMC1, 'b', '', 0, 28)
    #print('Right fit results:')
    #print(f'#chi^2 / NDF = {fitMC1.GetChisquare():#.2f} / {fitMC1.GetNDF()}')
#
    #fitMC2 = TF1('fitMC2', '([0] + [1]*x + [2]*x*x + [3]*x*x*x)', -28, 0)
    #fitMC2.SetParNames('p0', 'p1', 'p2', 'p3')
    #fitMC2.SetParameters(-9900, 400, 4.9, -0.23)
#
    #histMC.Fit(fitMC2, 'b', '', -28, 0)
    #print('Left fit results:')
    #print(f'#chi^2 / NDF = {fitMC2.GetChisquare():#.2f} / {fitMC2.GetNDF()}')

    # geom func
    fitMCg = TF1('fitMCg', '[0]*( 2/pi*acos([1]/[2]*sin(abs(pi*x/180)/2)) - 2*[1]*sin(abs(pi*x/180)/2)/(pi*[2]*[2])* sqrt( [2]*[2] - [1]*[1]*sin(abs(pi*x/180)/2)*sin(abs(pi*x/180)/2) ) )', -28, 28)
    fitMCg.SetParNames('Norm','R', 'r')
    fitMCg.SetParameters(10000, 10, 2.54)

    histMC.Fit(fitMCg, 'b', '', -28, -28)
    print('Left fit results:')
    print(f'#chi^2 / NDF = {fitMCg.GetChisquare():#.2f} / {fitMCg.GetNDF()}')

    #gaus fit
    #fitMCg = TF1('fitMCg', 'gaus(0)', -28, 28)
    #fitMCg.SetParNames('Norm','#mu', '#sigma')
    #fitMCg.SetParameters(10000, 0, 20)
#
    #histMC.Fit(fitMCg, 'b', '', -28, -28)
    #print('Left fit results:')
    #print(f'#chi^2 / NDF = {fitMCg.GetChisquare():#.2f} / {fitMCg.GetNDF()}')


    histMC.Draw('hist')
    #fitMC1.Draw('same')
    #fitMC2.Draw('same')
    fitMCg.Draw('same')

    outfile.cd()
    histMC.Write()
    canvas.Write()

if __name__ == '__main__':
   
    kNEvents = 10000
    kRadius = 2.54
    kDistance = 10

    #generateMC(kNEvents, kRadius, kDistance)
    outfile = TFile('data/output/Gamma/ToyMCfit.root', 'recreate')
    fitMC(outfile)

    
