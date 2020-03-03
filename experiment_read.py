import numpy as np
import pandas as pd
import os
from experiment import *

"""
    Script to read the data from the excel files for the front data

    Dependencies:
        numpy, pandas, xlrd
        
    Requirements:
         Excel and Matlab files should be stored in a folder called 'data'.
         The Python files should be just placed outside of this folder

    Format:
        Data for each experiment is stored in an Experiment class which has the following attributes:
            time = time since the beginning of the experiment
            tow1 = temperature data of tow 1
            tow2 = temperature data of tow 2
            tow3 = temperature data of tow 3
            tow4 = temperature data of tow 4
            tow5 = temperature data of tow 5
            tow6 = temperature data of tow 6
            tow7 = temperature data of tow 7
            tow8 = temperature data of tow 8
            tow9 = temperature data of tow 9

        The type of each attribute is a numpy array        
        
    version date: 03.03.2020
"""

def generate(file_number):
    data = pd.read_csv(files[file_number])
    reltime = data[data.columns[2]].to_numpy()
    tow1 = data[data.columns[3]].to_numpy()
    tow2 = data[data.columns[4]].to_numpy()
    tow3 = data[data.columns[5]].to_numpy()
    tow4 = data[data.columns[6]].to_numpy()
    tow5 = data[data.columns[7]].to_numpy()
    tow6 = data[data.columns[8]].to_numpy()
    tow7 = data[data.columns[9]].to_numpy()
    tow8 = data[data.columns[10]].to_numpy()
    return Experiment(reltime, tow1, tow2, tow3, tow4, tow5, tow6, tow7, tow8)

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data'

filenames = os.listdir(dir_path)
files = ["data/" + x for x in filenames if x[-3:] == 'csv']

Exp1 = generate(0)
Exp2 = generate(1)
Exp3 = generate(2)
Exp4 = generate(3)
Exp5 = generate(4)
Exp6 = generate(5)
Exp7 = generate(6)
Exp8 = generate(7)
Exp9 = generate(8)


    
    
    
    
