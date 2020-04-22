from experiment_read import *
import matplotlib.pyplot as plt
from data import *
import pylab
from regression import *

'''
Script used to extract the temperature history of a single point.
This is done by first finding the distances between the measurement lines of the thermal camera.
Those distances are converted to time intervals from which it can be seen, for example, when measurement line 5
is going to record the temperature of the point that measurement line 4 recorded in the previous sample.
'''

'''
To generate data:
  pass the tow and the corresponding time array to the function get_temp_history(tow, time)
  returns:
      point_time -> array containing the time history of the point
      point_temp -> array containing the temperature history of the point

version date: 26.03.2020
Alex
'''

front = {f'Exp{i + 1}' : generate_front(i) for i in range(numExp)} #front camera data
back = {f'Exp{i + 1}' : generate_back(i) for i in range(numExp)} #rear camera data

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
            dist = (times[i + 1] - times[i]) * Vel
            distances.append(dist)
        except:
            pass

    return distances

#Helper function, find the element in an array that is nearest to a specific value
def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or np.absolute(value - array[idx-1]) < np.absolute(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]


#Final function returns the time and temperature histories
def get_temp_history(tow, time):
    distances = np.array(get_distances(tow, time))
    time_dist = distances / Vel

    for i in range(1, len(time_dist)):
        try:
            time_dist[i] += time_dist[i - 1]
        except:
            pass

    start_time = time[400]
    point_time = [time[400]]
    point_temp = [tow[0][400]]

    time_offset = time_dist + start_time
    time_offset = list(time_offset.flatten())

    index_table = []
    for i in range(len(time_offset)):
        idx = find_nearest(time, time_offset[i])
        index_table.append(np.where(time==idx))


    for i in range(len(time_offset)):
        temp = float(tow[i + 1][index_table[i]])
        point_temp.append(temp)

    point_time += time_offset

    return(point_time, point_temp)


if __name__ == '__main__':

    for i in range(numExp):
        time = back[f'Exp{i + 1}'].time
        for j in range(1, numTows, 2):
            data = eval("back[f'Exp{i + 1}'].tow" + str(j)) 

            t, temp = get_temp_history(data, time)
            
            plt.title(f'{experiment_params[i][0]}[W], {experiment_params[i][1]}[N]')
            plt.xlabel(f'Time[s]')
            plt.ylabel(f'Temperature[$^\circ$C]')
            plt.plot(t, temp, label=f'Tow {j}')
            
        plt.legend()
        plt.savefig(f'cooling\Exp{i+1}')
        plt.clf()
    
    
    
    
    
