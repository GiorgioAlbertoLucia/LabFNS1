import sys
sys.path.append('Python/utils')
import pandas as pd
import numpy as np
from ReadMCA import GetPandas
from math import pi, exp
from datetime import date

r = 2.54
R = 10.
TCobaltA = 511.892000
TCobaltB = 610.138000
TSodiumA = 300.000000
TSodiumB = 300.000000

dfSodiumA = GetPandas('data/input/Gamma/SodiocalibrazioneA.mca')
dfSodiumB = GetPandas('data/input/Gamma/SodiocalibrazioneB.mca')
dfCobaltA = GetPandas('data/input/Gamma/CobaltocalibrazioneA.mca')
dfCobaltB = GetPandas('data/input/Gamma/CobaltocalibrazioneB.mca')

dfSodiumA = dfSodiumA.iloc[150:,:]
dfSodiumB = dfSodiumB.iloc[150:,:]
dfCobaltA = dfCobaltA.iloc[150:,:]
dfCobaltB = dfCobaltB.iloc[150:,:]

dfSodiumA = np.asarray(dfSodiumA[0],'d')
dfSodiumB = np.asarray(dfSodiumB[0],'d')
dfCobaltA = np.asarray(dfCobaltA[0],'d')
dfCobaltB = np.asarray(dfCobaltB[0],'d')

countsSodiumA = dfSodiumA.sum()
countsSodiumB = dfSodiumB.sum()
countsCobaltA = dfCobaltA.sum()
countsCobaltB = dfCobaltB.sum()

acceptance = r*r/(4*R*R)
print('Acceptance:', acceptance)

RateSodiumA = countsSodiumA/TSodiumA/acceptance
RateSodiumB = countsSodiumB/TSodiumB/acceptance
RateCobaltA = countsCobaltA/TCobaltA/acceptance
RateCobaltB = countsCobaltB/TCobaltB/acceptance

print('\n')
print('RateSodiumA: ', RateSodiumA)
print('RateSodiumB: ', RateSodiumB)
print('RateCobaltA: ', RateCobaltA)
print('RateCobaltB: ', RateCobaltB)

meanSodium = (RateSodiumA + RateSodiumB)/2
meanCobalt = (RateCobaltA + RateCobaltB)/2

print('\n')
print('meanSodium: ', meanSodium)
print('meanCobalt: ', meanCobalt)


RateSodiumTrue = 90.4e3
RateCobaltTrue = 19.869e3
DateSodium = date(2019,9,1)
DateCobalt = date(2018,1,30)
DateExp = date(2023,5,24)

diffSodium = abs((DateSodium-DateExp).days)
diffCobalt = abs((DateCobalt-DateExp).days)

LifeSodium = 2.6*365
LifeCobalt = 5.27*365

ExpectedSodiumRate = RateSodiumTrue * exp(-diffSodium/LifeSodium)
ExpectedCobaltRate = RateCobaltTrue * exp(-diffCobalt/LifeCobalt)

print('\n')
print('ExpectedSodiumRate: ', ExpectedSodiumRate)
print('ExpectedCobaltRate: ', ExpectedCobaltRate)