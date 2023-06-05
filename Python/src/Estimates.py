import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

from ReadMCA import CalEnergyErr

if __name__ == "__main__":
    electronEn = 490
    electronEnErr = 20
    photonEn = 662
    c = 3*10*10*10*10*10*10*10*10
    electronMass = (2*photonEn*(photonEn-electronEn))/(electronEn)
    electronMassErr = ((2*photonEn*electronEnErr)/(electronEn))
    print(electronMass)
    print(electronMassErr)
    print('\n\n')
    # StopPowerPolyElectronsNIST = 1.769 #(MeV*cm2)/(g)
    StopPowerPolyElectronsNIST = 1769 # (keV*cm2)/(g)
    SpecificRhoPoly = 1.420 #(g/cm3)
    RhoPoly = SpecificRhoPoly*0.99823
    print(RhoPoly)
    PolyThickness = (662-650)/(RhoPoly*StopPowerPolyElectronsNIST)
    PolyThicknessErr = 20/(RhoPoly*StopPowerPolyElectronsNIST)
    print(PolyThickness)
    print(PolyThicknessErr)
 
    print('650')
    calibrationErr650 = CalEnergyErr(0.318,0.008,-30,40,5,-0.3480447107320089,650.7,1.1)
    error650 = np.sqrt(1.1*1.1 + calibrationErr650*calibrationErr650)
    print(calibrationErr650)
    print('490')
    calibrationErr490 = CalEnergyErr(0.318,0.008,-30,40,5,-0.3480447107320089,490,1.1)
    error490 = np.sqrt(1.1*1.1 + calibrationErr490*calibrationErr490)
    print(calibrationErr490)
    print('520')
    calibrationErr520 = CalEnergyErr(0.318,0.008,-30,40,5,-0.3480447107320089,520,324.0752775049542)
    error520 = np.sqrt(1.1*1.1 + calibrationErr520*calibrationErr520)
    print(calibrationErr520)
    print('360')
    calibrationErr360 = CalEnergyErr(0.318,0.008,-30,40,5,-0.3480447107320089,360.0,1.1)
    error360 = np.sqrt(1.1*1.1 + calibrationErr360*calibrationErr360)
    print(calibrationErr360)
    print('540')
    calibrationErr540 = CalEnergyErr(0.318,0.008,-30,40,5,-0.3480447107320089,540,87)
    error540 = np.sqrt(1.1*1.1 + calibrationErr540*calibrationErr540)
    print(calibrationErr540)
