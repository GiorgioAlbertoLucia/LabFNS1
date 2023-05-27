import numpy as np
import pandas as pd
from ROOT import TGraphErrors, TGraph, TCanvas, TFile

# Read the .mca file
i = 0

def rateOfAcquisition(infile):
    '''
    Returns the rate of a specific angle acquisition
    '''

    data = []
    live_time = 100

    with open(infile, 'r', errors='ignore') as file:

        lines = file.readlines()[1:-1]
        for line in file:
            if line.startswith('LIVE_TIME'):
                live_time = line
                #live_time = line.split('-')[-1].strip()
                print(live_time)

        start_index = lines.index('<<DATA>>\n') + 1
        end_index = lines.index('<<END>>\n')

        for line in lines[start_index:end_index]:
                value = int(line.strip())  # Convert the line to an integer
                data.append(value)  # Append the value to the list

    tot_counts = 0
    for x in data:  tot_counts += x

    return tot_counts#/live_time

    print(i)
    i += 1


if __name__ == '__main__':

    angles = [31, 27, 23, 19, 15, 11, 7]
    inputFiles =   ['data/input/Gamma/PositroniumDecays/pos10min31deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos9min27deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos8min23deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos7min19deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos6min15deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos5min11deg.mca',
                    'data/input/Gamma/PositroniumDecays/pos4min7deg.mca',
                    #'data/input/Gamma/PositroniumDecays/pos7min19deg.mca'
                    ]

    rates = []
    live_times = [600, 540, 480, 420, 360, 300, 240]
    for angle, live_time, infile in zip(angles, live_times, inputFiles):
        #rate = rateOfAcquisition(infile)
        #rates.append(rate)
        tot_count = rateOfAcquisition(infile)
        rates.append(tot_count/live_time)

    graph = TGraph(7, np.asarray(angles, 'd'), np.asarray(rates, 'd'))
    graph.
    
    outfile = TFile('test.root', 'recreate')
    graph.Write()

    input(' ')
    


    
