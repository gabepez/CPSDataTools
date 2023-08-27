# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 08:29:13 2023

@author: gabe
"""

import pandas as pd

datFileLoc = "G:\\My Drive\\Grad School\\RawData\\CPS Veterans Supplement\\202208 Data\\"
datFileName = "aug22pub.dat"


data = pd.read_fwf(datFileLoc + datFileName, colspecs='infer', header=None)
