import numpy as np
import pandas as pd
import os
from experiment import *

"""
    Script to read the data from the excel files for the front data

    Dependencies:
        numpy, pandas, xlrd
        
    Requirements:
         Excel files should be stored in a folder called 'data'.
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

        If the class is used to store data from the rear camera,
        the tow variables become multidimensional arrays holding
        the temperature history of each line as a sub-array.
            
        The type of each attribute is a numpy array        
        
    version date: 03.03.2020
    Alex
"""

def generate_front(file_number):
    data = pd.read_csv(front[file_number])
    reltime = data[data.columns[2]].to_numpy()
    _tow1 = data[data.columns[3]].to_numpy()
    _tow2 = data[data.columns[4]].to_numpy()
    _tow3 = data[data.columns[5]].to_numpy()
    _tow4 = data[data.columns[6]].to_numpy()
    _tow5 = data[data.columns[7]].to_numpy()
    _tow6 = data[data.columns[8]].to_numpy()
    _tow7 = data[data.columns[9]].to_numpy()
    _tow8 = data[data.columns[10]].to_numpy()
    return Experiment(reltime, tow1=_tow1, tow2=_tow2, tow3=_tow3,
                      tow4=_tow4, tow5=_tow5, tow6=_tow6, tow7=_tow7, tow8=_tow8)

def generate_back(file_number):
    data = pd.read_csv(rear[file_number], header=None)
    reltime = data[data.columns[0]].to_numpy()
    _tow1 = np.array([data[data.columns[1 + 8 * i]].to_numpy() for i in range(10)])
    _tow2 = np.array([data[data.columns[2 + 8 * i]].to_numpy() for i in range(10)])
    _tow3 = np.array([data[data.columns[3 + 8 * i]].to_numpy() for i in range(10)])
    _tow4 = np.array([data[data.columns[4 + 8 * i]].to_numpy() for i in range(10)])
    _tow5 = np.array([data[data.columns[5 + 8 * i]].to_numpy() for i in range(10)])
    _tow6 = np.array([data[data.columns[6 + 8 * i]].to_numpy() for i in range(10)])
    _tow7 = np.array([data[data.columns[7 + 8 * i]].to_numpy() for i in range(10)])
    _tow8 = np.array([data[data.columns[8 + 8 * i]].to_numpy() for i in range(10)])
    return Experiment(reltime, tow1=_tow1, tow2=_tow2, tow3=_tow3,
                      tow4=_tow4, tow5=_tow5, tow6=_tow6, tow7=_tow7, tow8=_tow8)


filenames = os.listdir('data')

front = ['data/' + x for x in filenames if x[-3:] == 'csv' and 'rear' not in x]
rear = ['data/' + x for x in  filenames if x[-8:] == 'rear.csv']


    
    
    
    
