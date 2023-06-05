import pandas as pd
import numpy as np
import sys
sys.path.append('Python/utils')

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

    fitResults = graph.Fit(calibrationfit, 'S')
    covMatrix = fitResults.GetCovarianceMatrix()

    cov650 = 
    cov490 = 
    cov520 = 
    cov360 = 
    cov540 =  
    calibrationErr650 = CalEnergyErr(0.318,0.008,-30,40,5,cov650,650)
    calibrationErr490 = CalEnergyErr(0.318,0.008,-30,40,5,cov490,490)
    calibrationErr520 = CalEnergyErr(0.318,0.008,-30,40,5,cov520,520)
    calibrationErr360 = CalEnergyErr(0.318,0.008,-30,40,5,cov360,360)
    calibrationErr540 = CalEnergyErr(0.318,0.008,-30,40,5,cov540,540)
