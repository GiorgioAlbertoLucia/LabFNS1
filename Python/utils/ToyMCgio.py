import numpy as np
import ctypes

from ROOT import TRandom3, gRandom, TH1D, TFile

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


if __name__ == '__main__':
   
    kNEvents = 10000
    kRadius = 2.54
    kDistance = 10
    kTan = kRadius/kDistance
    kTheta = np.arctan(kTan)
    
    gRandom = TRandom3()
    gRandom.SetSeed(42)
    
    angles = list(range(-32,32,4))
    histo = TH1D("toyMC","toy MC", 17,-34,34)
    
    for alpha in angles:
        for i in range(kNEvents):
            
            if i%10000 == 0:    print(f'Processing event {i}\r')


            photonDirection = GenerateDecay(kTheta)
            newPhotonDirection = xzPlaneRotation(-radians(alpha), photonDirection)    # photon direction in the second scintillator FR

            # check if the photon is in the cone of opening theta for the second scintillator and fill the histogram
            if np.arccos(newPhotonDirection[2]) < abs(kTheta):    histo.Fill(alpha)

            #x,y,z = GenerateDecay(kTan)
            #centre = (kDistance*sin(radians(alpha)),0,kDistance*cos(radians(alpha)))
            ##print(centre)
            #x = x.value
            #y = y.value
            #z = z.value
            ##time = (x*centre[0]+y*centre[1]+z*centre[2])
            #time = (kDistance*cos(radians(alpha))+kDistance*sin(radians(alpha))*tan(radians(alpha)))/(z+tan(radians(alpha))*x)
            ##print(time)
            ##distance = sqrt((x*time-centre[0])*(x*time-centre[0]) + (y*time-centre[1])*(y*time-centre[1]) + (z*time-centre[2])*(z*time-centre[2]))
            #distance = sqrt((x*time-centre[0])*(x*time-centre[0]) + (y*time-centre[1])*(y*time-centre[1]) + (z*time-centre[2])*(z*time-centre[2]))
            ##print(distance, x, y, z)
            #if distance<kRadius:
            #    #print("here")
            #    histo.Fill(alpha)
            #input()

    outfile = TFile("data/output/ToyMCgio.root",'recreate')
    histo.Write()
    outfile.Close()
