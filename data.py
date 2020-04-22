import numpy as np
'''File containing some handy data that will probably be used by multiple scripts'''

# Experiment parameters (laser power, compaction force)
experiment_params = np.array([[1300, 100],[1300, 500],[1300, 1000],\
                              [1500, 100],[1500, 500],[1500, 1000],\
                              [1750, 100],[1750, 500],[1750, 1000]])

numExp = 9 #Number of experiments
numTows = 8 #Number of tows per experiment
numLines = 10 #Number of lines per tow in the rear
Vel = 0.01 #Placement speed 100[mm/s]
