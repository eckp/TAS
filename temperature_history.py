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


def plot_all_cr(all_cr, hlines={}):
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for ax in axes[-1,:]:
            ax.set_xlabel('Sampling point along run')
    for ax in axes[:,0]:
            ax.set_ylabel('Subtrate temperature$')
    for exp_idx, (exp_cr, ax) in enumerate(zip(all_cr, axes.flatten())):
        for tow_idx, tow_cr in enumerate(exp_cr):
            exp_params = experiment_params[exp_idx]
            ax.set_title(f'Experiment {exp_idx+1}: power = {exp_params[0]} W, force = {exp_params[1]} N')
            ax.plot(list(range(sample_range.start, sample_range.start+len(tow_cr))), tow_cr, c=colors[tow_idx])
            for line, style in zip(hlines, linestyles):
                ax.axhline(hlines[line][exp_idx][tow_idx], c=colors[tow_idx], linestyle=style, label=line)
    fig.legend(handles=[plt.Line2D([0], [0], c=colors[idx], label=f'tow nr. {idx*2+1}') for idx in range(tow_idx+1)] +
                       [plt.Line2D([0], [0], c='k', ls=linestyle, label=name) for name, linestyle in zip(hlines, linestyles[0:len(hlines)])])
    fig.tight_layout()
    plt.show()




# Distances between measurement lines for each tow
line_distances = np.asarray([get_distances(back['Exp1'][0].tows[i], back['Exp1'][0].time) for i in range(numTows)])

if __name__ == '__main__':
    run = False
    if run:
        Ts = {f'Exp{i}' : [[], [], [], []] for i in range(1, 10)}
        for exp_num in range(1,10):
            for tow_num in [1, 3, 5, 7]:
                for sample_index in range(200, 600):
                    time = back[f'Exp{exp_num}'][0].time
                    tow = eval("back[f'Exp{exp_num}'][0].tow" + f'{tow_num}')

                    t, temp = get_temp_history(time, tow, tow_num, sample_index)
                    
                    #Make initial guesses for the parameters 
                    k0 = 0.5
                    coeff = np.exp(-k0 * t[-1])
                    A = np.array([1, 1, 1, coeff]).reshape(2,2)
                    B = np.array([temp[0], temp[-1]]).reshape(2, 1)

                    A0, B0 = np.linalg.solve(A, B)
                    A0 = float(A0)
                    B0 = float(B0)

                    #Fit exponential curve of form A + Be^(-kt) to experimental data

                    try:
                        params = scipy.optimize.curve_fit(func, t, temp, p0=[A0, B0, k0])[0]

                        A = params[0]
                        B = params[1]
                        k = params[2]
                        
                        a = 0
                        if tow_num == 1: a = 0;
                        if tow_num == 3: a = 1;
                        if tow_num == 5: a = 2;
                        if tow_num == 7: a = 3;

                        Ts[f'Exp{exp_num}'][a].append(A)
                        
                    except:
                        print(f'{exp_num}, {tow_num}, {sample_index}')

                    



          
        
    
    
    
