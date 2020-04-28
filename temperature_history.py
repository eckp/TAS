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
  pass the tow and the corresponding time array to the function get_temp_history(tow, time)
  returns:
      point_time -> array containing the time history of the point
      point_temp -> array containing the temperature history of the point

version date: 27.04.2020
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


#Final function returns the shifted time (stating from 0) and temperature histories
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
    
    time_dist = list(time_dist.flatten())
    time_dist.insert(0, 0)
    

    return(time_dist, point_temp)

def func(t, A, B, k):
    return A + B * np.exp(-k * t)
    

if __name__ == '__main__':

    P13_1 = [[], []]
    P15_1 = [[], []]
    P175_1 = [[], []]

    P13_3 = [[], []]
    P15_3 = [[], []]
    P175_3 = [[], []]

    P13_5 = [[], []]
    P15_5 = [[], []]
    P175_5 = [[], []]

    P13_7 = [[], []]
    P15_7 = [[], []]
    P175_7 = [[], []]
    
    for exp in back.values():
        for i in ['1', '3', '5', '7']:
            
            time = exp[0].time
            tow = eval('exp[0].tow' + i)
            t, temp = get_temp_history(tow, time)

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

            k = params[2]
            P = exp[1][0]
            F = exp[1][1]

            if i == '1':

                if P == 1300:
                    P13_1[0].append(F)
                    P13_1[1].append(k)

                if P == 1500:
                    P15_1[0].append(F)
                    P15_1[1].append(k)

                if P == 1750:
                    P175_1[0].append(F)
                    P175_1[1].append(k)

            if i == '3':

                if P == 1300:
                    P13_3[0].append(F)
                    P13_3[1].append(k)

                if P == 1500:
                    P15_3[0].append(F)
                    P15_3[1].append(k)

                if P == 1750:
                    P175_3[0].append(F)
                    P175_3[1].append(k)

            if i == '5':

                if P == 1300:
                    P13_5[0].append(F)
                    P13_5[1].append(k)

                if P == 1500:
                    P15_5[0].append(F)
                    P15_5[1].append(k)

                if P == 1750:
                    P175_5[0].append(F)
                    P175_5[1].append(k)

            if i == '7':

                if P == 1300:
                    P13_7[0].append(F)
                    P13_7[1].append(k)

                if P == 1500:
                    P15_7[0].append(F)
                    P15_7[1].append(k)

                if P == 1750:
                    P175_7[0].append(F)
                    P175_7[1].append(k)
                    

    plt.xlabel('Force $[N]$')
    plt.ylabel('Cooling constant $k\ [s^{-1}]$')
    plt.box()
    plt.axhline(y=0, color='k', linewidth=0.75)
    plt.axvline(x=0, color='k', linewidth=0.75)
    plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
    plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.xticks([100, 500, 1000])
    plt.plot(P13_1[0], P13_1[1], color='r', label='$1300\ W$')
    plt.plot(P15_1[0], P15_1[1], color='g', label='$1500\ W$')
    plt.plot(P175_1[0], P175_1[1], color='b', label='$1750\ W$')
    plt.title('Cooling rate versus Power for Tow 1')
    plt.legend(loc="best", fancybox = True, shadow = True)
    plt.savefig('cooling/fit/Tow1.png')
    plt.clf()

    plt.xlabel('Force $[N]$')
    plt.ylabel('Cooling constant $k\ [s^{-1}]$')
    plt.box()
    plt.axhline(y=0, color='k', linewidth=0.75)
    plt.axvline(x=0, color='k', linewidth=0.75)
    plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
    plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.xticks([100, 500, 1000])
    plt.plot(P13_7[0], P13_7[1], color='r', label='$1300\ W$')
    plt.plot(P15_7[0], P15_7[1], color='g',label='$1500\ W$')
    plt.plot(P175_7[0], P175_7[1], color='b', label='$1750\ W$')
    plt.title('Cooling rate versus Power for Tow 7')
    plt.legend(loc="best", fancybox = True, shadow = True)
    plt.savefig('cooling/fit/Tow7.png')
    plt.clf()

    
    plt.xlabel('Force $[N]$')
    plt.ylabel('Cooling constant $k\ [s^{-1}]$')
    plt.box()
    plt.axhline(y=0, color='k', linewidth=0.75)
    plt.axvline(x=0, color='k', linewidth=0.75)
    plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
    plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.xticks([100, 500, 1000])
    plt.plot(P13_3[0], P13_3[1], color='c', label='$1300\ W$')
    plt.plot(P15_3[0], P15_3[1], color='m', label='$1500\ W$')
    plt.plot(P175_3[0], P175_3[1], color='y', label='$1750\ W$')
    plt.title('Cooling rate versus Power for Tow 3')
    plt.legend(loc="best", fancybox = True, shadow = True)
    plt.savefig('cooling/fit/Tow3.png')
    plt.clf()

    plt.xlabel('Force $[N]$')
    plt.ylabel('Cooling constant $k\ [s^{-1}]$')
    plt.box()
    plt.axhline(y=0, color='k', linewidth=0.75)
    plt.axvline(x=0, color='k', linewidth=0.75)
    plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
    plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.xticks([100, 500, 1000])
    plt.plot(P13_5[0], P13_5[1], color='c', label='$1300\ W$')
    plt.plot(P15_5[0], P15_5[1], color='m', label='$1500\ W$')
    plt.plot(P175_5[0], P175_5[1], color='y', label='$1750\ W$')
    plt.title('Cooling rate versus Power for Tow 5')
    plt.legend(loc="best", fancybox = True, shadow = True)
    plt.savefig('cooling/fit/Tow5.png')
    plt.clf()


          
        
    
    
    
