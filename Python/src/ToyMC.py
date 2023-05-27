from ROOT import TRandom3, gRandom, TH1D, TFile
from math import acos, atan, cos, sin, tan, sqrt, radians
import ctypes

def GenerateDecay(TgTheta):
    x = ctypes.c_double()
    y = ctypes.c_double()
    z = ctypes.c_double()
    z.value=0
    while (acos(z.value)>abs(atan(TgTheta))):
        gRandom.Sphere(x,y,z,1.)
    #print(acos(z.value),atan(Tgalpha))
    return x,y,z


if __name__ == '__main__':
    kNEvents = 10000
    kRadius = 2.54
    kDistance = 10
    kTan = kRadius/kDistance
    gRandom = TRandom3()
    gRandom.SetSeed(42)
    angles = list(range(-32,32,4))
    histo = TH1D("toyMC","toy MC", 17,-34,34)
    for alpha in angles:
        for i in range(kNEvents):
            if i%10000 == 0:
                print(f'Processing event {i}\r')
            x,y,z = GenerateDecay(kTan)
            centre = (kDistance*sin(radians(alpha)),0,kDistance*cos(radians(alpha)))
            #print(centre)
            x = x.value
            y = y.value
            z = z.value
            #time = (x*centre[0]+y*centre[1]+z*centre[2])
            time = (kDistance*cos(radians(alpha))+kDistance*sin(radians(alpha))*tan(radians(alpha)))/(z+tan(radians(alpha))*x)
            #print(time)
            distance = sqrt((x*time-centre[0])*(x*time-centre[0]) + (y*time-centre[1])*(y*time-centre[1]) + (z*time-centre[2])*(z*time-centre[2]))
            #print(distance, x, y, z)
            if distance<kRadius:
                #print("here")
                histo.Fill(alpha)
            #input()
    outfile = TFile("data/output/ToyMC.root",'recreate')
    histo.Write()
    outfile.Close()
