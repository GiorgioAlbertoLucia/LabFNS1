import pandas as pd
import numpy as np

from ROOT import TH2D, 
import uproot

from StyleFormatter import SetGlobalStyle, SetObjectStyle
SetGlobalStyle(padleftmargin=0.12, padbottommargin=0.12, padrightmargin=0.05, padtopmargin=0.1, titleoffsety=1.2, titleoffsetx=0.9, titleoffset= 0.7, opttitle=1)


if __name__ == '__main__':
    Tree=uproot.open("data/processed/Test.root")["fTreeData"]