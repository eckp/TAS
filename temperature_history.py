from experiment_read import *
import matplotlib.pyplot as plt
from data import *
import pylab
from regression import *
import scipy

'''
Script used to extract the temperature history of a single point.
This is done by first finding the distances between the measurement lines of the thermal camera.
Those distances are converted to time intervals from which it can be seen, for example, when measurement line 5
is going to record the temperature of the point that measurement line 4 recorded in the previous sample.
'''

'''
To generate data:
  pass the time and tow arrays as well as the number of the tow to the function get_temp_history(time, tow, townum)
  returns:
      point_time -> array containing the time history of the point
      point_temp -> array containing the temperature history of the point

version date: 11.05.2020
Alex

'''
#Group experimental data with its parameters 
front = {f'Exp{i + 1}' : [generate_front(i), experiment_params[i]]  for i in range(numExp)} #front camera data
back = {f'Exp{i + 1}' : [generate_back(i), experiment_params[i]] for i in range(numExp)} #rear camera data

Polynomial = np.polynomial.Polynomial

#General interval over which to construct the linear approximation of the curve
def get_data_to_fit(data, time, T_threshold):
    x = []
    y = []
    
    for i in range(len(data)):
        if data[i] > T_threshold:
            x.append(time[i - 1])
            x.append(time[i])
            y.append(data[i - 1])
            y.append(data[i])
            break

    return x, y

#Find the distances between the measurement lines
def get_distances(tow, time):
    times = []
    for i in range(numLines):
        data = tow[i]
        T_threshold = 55
        x, y = get_data_to_fit(data, time, T_threshold)

        pfit, stats = Polynomial.fit(x, y, 1, full=True)

        A0, m = pfit

        data = np.array([T_threshold for i in range(len(time))])
        y = np.array([pfit(x) for x in time])

        idx = np.argwhere(np.diff(np.sign(y - data))).flatten()
        times.append(time[idx])

    distances = []
    for i in range(len(times)):
        try:
            dist = (float(times[i + 1]) - float(times[i])) * Vel
            distances.append(dist)
        except:
            pass

    return np.asarray(distances)

#Helper function, find the element in an array that is nearest to a specific value
def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or np.absolute(value - array[idx-1]) < np.absolute(value - array[idx])):
        return idx-1
    else:
        return idx


#Final function returns the shifted time (stating from 0) and temperature histories
def get_temp_history(time, tow, townum, sample_idx=400):
    distances = line_distances[townum-1]
    time_dist = np.zeros(numLines)
    time_dist[1:] = distances / Vel

    for i in range(1, len(time_dist)):
        time_dist[i] += time_dist[i - 1]

    start_time = time[sample_idx]
    
    point_temp = np.zeros(numLines)
    point_temp[0] = tow[0][sample_idx]

    time_offset = time_dist + start_time
    index_table = np.zeros(numLines - 1, dtype=np.int32)
    
    for i in range(len(time_offset) - 1):
        idx = find_nearest(time, time_offset[i + 1])
        index_table[i] = idx

    for i in range(len(index_table)):
        temp = tow[i + 1][index_table[i]]
        point_temp[i + 1] = temp

    return(time_dist, point_temp)

# Define function to fit
def func(t, A, B, k):
    return A + B * np.exp(-k * t)

# Distances between measurement lines for each tow
line_distances = np.asarray([get_distances(back['Exp1'][0].tows[i], back['Exp1'][0].time) for i in range(numTows)])

if __name__ == '__main__':
    time = back['Exp1'][0].time
    tow = back['Exp1'][0].tow1

    t, temp = get_temp_history(time, tow, 1)
    
    #Make initial guesses for the parameters 
    k0 = 0.5
    coeff = np.exp(-k0 * t[-1])
    A = np.array([1, 1, 1, coeff]).reshape(2,2)
    B = np.array([temp[0], temp[-1]]).reshape(2, 1)

    A0, B0 = np.linalg.solve(A, B)
    A0 = float(A0)
    B0 = float(B0)

    #Fit exponential curve of form A + Be^(-kt) to experimental data

    params = scipy.optimize.curve_fit(func, t, temp, p0=[A0, B0, k0])[0]

    A = params[0]
    B = params[1]
    k = params[2]

    fit = func(t, A, B, k)

    plt.plot(t, fit, label='fit')
    plt.plot(t, temp, label='experimental')
    plt.legend()
    plt.show()

                    



          
        
    
    
    
