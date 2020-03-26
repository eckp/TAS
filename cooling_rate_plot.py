# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:40:19 2020

@author: loicm
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

"""
This file plots the cooling rate with respect to compaction force and laser power

input: cooling rate (numpy array (9,4)) of 9 experiments and 4 tows per experiment
output: plot of cooling rate (y-axis) by laser power (x-axis) and each colour represents a different
compaction force, shown in the legend. 3 colours for 3 experiments with equal compaction force,
each experiment having 4 different tows. Tows are shown in same colour and on same x-location (because same laser power)

"""

# Cooling rate: np.array (9,4) of each experiment (row) and then each tow (column)
rate = np.array([[0.66734257, 0.69078883, 0.77631882, 0.63813754],
       [0.39912428, 0.45883439, 0.49331085, 0.39826872],
       [0.73990755, 0.8245401 , 0.82595915, 0.70234445],
       [0.6686941 , 0.77086088, 0.74432964, 0.64881394],
       [0.71908277, 0.83954894, 0.8427713 , 0.71143514],
       [0.75150193, 0.85826932, 0.83488946, 0.71027249],
       [0.66258022, 0.76044122, 0.75452233, 0.63714172],
       [0.71199218, 0.82476226, 0.81331313, 0.70321665],
       [0.72214175, 0.79171589, 0.79241718, 0.67660492]])

# [W] Laser power of each experiment
power = np.array([1300,
1300,
1300,
1500,
1500,
1500,
1750,
1750,
1750
])

# [N] Compaction force of each experiment
force = np.array([100,
500,
1000,
100,
500,
1000,
100,
500,
1000
])

# Colours of plots, for each compaction force
col = ['blue','red','green']

# start plotting
for i in range(3):              # 3 different compaction forces, iterate through them
    idx = np.array([i,i+3,i+6]) # index of experiments with the same force, so we first plot experiment (0,3,6), etc.
    for j in range(4):          # each of the 4 tows of that experiment
        # plots jth tow of (i,i+3,i+6)th experiment, plotting all laser powers together with one compaction force
        plt.plot(np.take(power,idx),np.take(rate,idx,axis=0)[:,j],c=col[i],marker='o',label=('Compation force: '+str(force[idx[0]])+' [N]'))
    
plt.xlabel('Laser power [W]')
plt.ylabel('Cooling rate [-]')
handles, labels = plt.gca().get_legend_handles_labels() # some code to remove duplice labels
by_label = dict(zip(labels, handles))                   # (this code makes a dict to remove duplicates)
plt.legend(by_label.values(), by_label.keys())          # show the legend with unique labels
plt.title('Cooling rate')
plt.show()
