from experiment_read import *
import matplotlib.pyplot as plt
import pylab

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

numExp = 9 #Number of experiments
numTows = 8 #Number of tows per experiment
numLines = 10 #Number of lines per tow in the rear
Vel = 0.01 #Placement speed 100[mm/s]

front = {f'Exp{i + 1}' : generate_front(i) for i in range(numExp)} #front camera data
back = {f'Exp{i + 1}' : generate_back(i) for i in range(numExp)} #rear camera data

Polynomial = np.polynomial.Polynomial

#General interval over which to construct the linear approximation of the curve
def get_data_to_fit(data, T_threshold):
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
def get_distances(tow):
    times = []
    for i in range(numLines):
        data = tow[i]
        T_threshold = 55
        x, y = get_data_to_fit(data, T_threshold)

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


#Final function that finds
def get_temp_history(tow, time):
    distances = np.array(get_distances(tow))
    time_dist = distances / Vel

    for i in range(1, len(time_dist)):
        try:
            time_dist[i] += time_dist[i - 1]
        except:
            pass

    start_time = time[400]
    point_time = [time[400]]
    point_temp = [data[0][400]]

    time_offset = time_dist + start_time
    time_offset = list(time_offset.flatten())

    index_table = []
    for i in range(len(time_offset)):
        idx = find_nearest(time, time_offset[i])
        index_table.append(np.where(time==idx))


    for i in range(len(time_offset)):
        temp = float(data[i + 1][index_table[i]])
        point_temp.append(temp)

    point_time += time_offset

    return(point_time, point_temp)


if __name__ == '__main__':
    time = back['Exp1'].time
    data = back['Exp4'].tow1

    t, temp = get_temp_history(data, time)

    plt.xlabel('Time[s]')
    plt.ylabel('Temperature[C]')
    plt.plot(t, temp)
      
    plt.show()

