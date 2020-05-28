from experiment_read import *
import matplotlib.pyplot as plt
from scipy import stats


# Experiment                     |  Laser Power | Compaction Force

front_exp_1 = generate_front(0) #       1300 W  |       100  N
front_exp_2 = generate_front(1) #       1300 W  |       500  N
front_exp_3 = generate_front(2) #       1300 W  |       1000 N
front_exp_4 = generate_front(3) #       1500 W  |       100  N
front_exp_5 = generate_front(4) #       1500 W  |       500  N
front_exp_6 = generate_front(5) #       1500 W  |       1000 N
front_exp_7 = generate_front(6) #       1750 W  |       100  N
front_exp_8 = generate_front(7) #       1750 W  |       500  N
front_exp_9 = generate_front(8) #       1750 W  |       1000 N

back_exp_1 = generate_back(0)   #       1300 W  |       100  N
back_exp_2 = generate_back(1)   #       1300 W  |       500  N
back_exp_3 = generate_back(2)   #       1300 W  |       1000 N
back_exp_4 = generate_back(3)   #       1500 W  |       100  N
back_exp_5 = generate_back(4)   #       1500 W  |       500  N
back_exp_6 = generate_back(5)   #       1500 W  |       1000 N
back_exp_7 = generate_back(6)   #       1750 W  |       100  N
back_exp_8 = generate_back(7)   #       1750 W  |       500  N
back_exp_9 = generate_back(8)   #       1750 W  |       1000 N

# Entry Temp: Generate average temperature and variance for each tow and experiment

"""
    This function creates four arrays. These are divided in two groups: 
    - Per tow measurements
        "tow_temp_avg" and "tow_temp_std" contain four 3x3 matrices. Each matrix corresponds to each tow (tows 1, 
        3, 5 and 7), and each matrix has three rows and three columns. Each row corresponds to a power setting 
        (1300 W, 1500 W, and 1750 W respectively), while each column corresponds to a compaction force. 
        
        This is how each matrix is structured:
                [ exp1  exp2    exp3
                  exp4  exp5    exp6
                  exp7  exp8    exp9 ]
        
        "tow_temp_avg" contains all the average temperatures per tow per experiment, while "tow_temp_std" contains 
        the standard deviation in temperature. 
        
    - Per experiment measurements
        Very similar to the previous arrays, but this time there is only one matrix per array, containing the average
        and standard deviation in "exp_temp_avg" and "exp_temp_std" respectively.
        
    The function returns, in the following order: tow_temp_avg, tow_temp_std, exp_temp_avg, exp_temp_std
"""

def front_arrays():

    tow_temp_avg = np.zeros((4,3,3))
    tow_temp_std = np.zeros((4,3,3))
    exp_temp_avg = np.zeros((3,3))
    exp_temp_std = np.zeros((3,3))

    for k in range(3): # Corresponds to the row of the matrix, hence to the power setting

        for i in range(3): # Corresponds to the column of the matrix, hence to the compaction force setting

            # First take the relevant time interval by only taking the time during which tape was being placed
            time_interval = eval(
                f'front_exp_{3 * k + (i + 1)}.time[ (front_exp_{3 * k + (i + 1)}.time >= 4.0) & '
                f'(front_exp_{3 * k + (i + 1)}.time <= 11.0) ]')

            average_temp_front = np.zeros(len(time_interval)) # Initialize an array for the average of all tows

            for j in range(4): # Corresponds to tow 2 * j + 1

                # Take the temperatures corresponding to the time interval
                tow_temp_interval = eval(
                    f'front_exp_{3 * k + (i + 1)}.tow{2 * j + 1}[ (front_exp_{3 * k + (i + 1)}.time >= 4.0) & '
                    f'(front_exp_{3 * k + (i + 1)}.time <= 11.0) ]')

                tow_temp_avg[j][k][i] = np.mean(tow_temp_interval) # Compute mean temperature
                tow_temp_std[j][k][i] = np.std(tow_temp_interval) # Compute standard deviation in the temperature

                # In case you want to see the line for each measurement (Select and "ctrl" +  "/" to uncomment ):
                # plt.plot(time_interval,tow_temp_interval)
                # plt.show()

                # Now make a temperature line for the experiment by combining the tow measurements

                if i + k == 0 and j != 1: # This excludes the bad measurements from tow 3 in exp no. 1
                    average_temp_front += 1 / 3 * tow_temp_interval

                elif i + k != 0:
                    average_temp_front += 0.25 * tow_temp_interval

            exp_temp_avg[k][i] = np.mean(average_temp_front) # Compute mean temperature
            exp_temp_std[k][i] = np.std(average_temp_front) # Compute standard deviation in the temperature

    print('Average temperature of each tow for each experiment:')
    print(tow_temp_avg)
    print('Standard deviation in temperature of each tow for each experiment:')
    print(tow_temp_std)
    print('Average temperature for each experiment, combining all tows:')
    print(exp_temp_avg)
    print('Standard deviation in temperature for each experiment, combining all tows:')
    print(exp_temp_std)
    print()
    print('Finished front_arrays()')
    print()
    print()

    return tow_temp_avg, tow_temp_std, exp_temp_avg, exp_temp_std # End of function!!!


# Exit Temperature:

"""
    This function creates six arrays. These are divided in two groups: 
    - Per tow measurements
        "tow_temp_avg", "tow_temp_slope" and "tow_temp_std" contain four 3x3 matrices. Each matrix corresponds 
        to each tow (tows 1, 3, 5 and 7), and each matrix has three rows and columns. Each row corresponds to a 
        power setting (1300 W, 1500 W, and 1750 W respectively), while each column corresponds to a compaction force. 
        
        This is how each matrix is structured:
                [ exp1  exp2    exp3
                  exp4  exp5    exp6
                  exp7  exp8    exp9 ]
        
        "tow_temp_avg" contains all the average temperatures per tow per experiment, "tow_temp_slope" contains
        the slope "a" of the regressed line of the form "T(t) = a*t + b", and "tow_temp_ste" contains 
        the standard error in temperature. 
        
    - Per experiment measurements
        Very similar to the previous arrays, but this time there is only one matrix per array, containing the average,
        the slope and standard error in "exp_temp_avg", "exp_temp_slope" and "exp_temp_ste" respectively.

    The function returns, in the following order: tow_temp_avg, tow_temp_slope, tow_temp_ste, 
    exp_temp_avg, exp_temp_slope, exp_temp_ste
"""


def back_arrays():
    tow_temp_avg = np.zeros((4, 3, 3))
    tow_temp_slope = np.zeros((4, 3, 3))
    tow_temp_ste = np.zeros((4, 3, 3))
    exp_temp_avg = np.zeros((3, 3))
    exp_temp_slope = np.zeros((3, 3))
    exp_temp_ste = np.zeros((3, 3))

    for k in range(3):  # Corresponds to the row of the matrix, hence to the power setting

        for i in range(3):  # Corresponds to the column of the matrix, hence to the compaction force setting

            # First take the relevant time interval by only taking the time during which tape was being placed
            time_interval = eval(
                f'back_exp_{3 * k + (i + 1)}.time[ (back_exp_{3 * k + (i + 1)}.time >= 2.0) & '
                f'(back_exp_{3 * k + (i + 1)}.time <= 11.0) ]')

            average_temp_back = np.zeros(len(time_interval))  # Initialize an array for the average of all tows

            for j in range(4):  # Corresponds to tow 2 * j + 1

                # Take the temperatures corresponding to the time interval
                tow_temp_interval = eval(
                    f'back_exp_{3 * k + (i + 1)}.tow{2 * j + 1}[0][ (back_exp_{3 * k + (i + 1)}.time >= 2.0) & '
                f'(back_exp_{3 * k + (i + 1)}.time <= 11.0) ]')

                tow_temp_avg[j][k][i] = np.mean(tow_temp_interval)  # Compute mean temperature
                # Perform linear regression:
                slope, intercept, r_value, p_value, std_err = stats.linregress(time_interval, tow_temp_interval)
                tow_temp_slope[j][k][i] = slope # Slope of the regression line
                tow_temp_ste[j][k][i] = np.std( tow_temp_interval - ( slope * time_interval ) )

                # In case you want to see the line for each measurement (Select and "ctrl" +  "/" to uncomment ):
                # plt.plot(time_interval,tow_temp_interval)
                # plt.show()

                # Now make a temperature line for the experiment by combining the tow measurements

                if i + k == 0 and j != 1:  # This excludes the bad measurements from tow 3 in exp no. 1
                    average_temp_back += 1 / 3 * tow_temp_interval

                elif i + k != 0:
                    average_temp_back += 0.25 * tow_temp_interval

            exp_temp_avg[k][i] = np.mean(average_temp_back)  # Compute mean temperature
            # Perform linear regression:
            slope, intercept, r_value, p_value, std_err = stats.linregress(time_interval, average_temp_back)
            exp_temp_slope[k][i] = slope # Slope of the regression line
            exp_temp_ste[k][i] = np.std( average_temp_back - ( slope * time_interval ) )

            # In case you want to see this plotted (Select and "ctrl" +  "/" to uncomment ):
            # plt.plot(time_interval, average_temp_back)
            # plt.plot(time_interval, ( slope * time_interval + intercept ) )
            # plt.plot(time_interval, (slope * time_interval + intercept + exp_temp_ste[k][i]))
            # plt.plot(time_interval, (slope * time_interval + intercept - exp_temp_ste[k][i]))
            # plt.show()

    print('Average temperature of each tow for each experiment:')
    print(tow_temp_avg)
    print('Slope of T-history regression for each tow for each experiment:')
    print(tow_temp_slope)
    print('Standard error in temperature of each tow for each experiment:')
    print(tow_temp_ste)
    print('Average temperature for each experiment, combining all tows:')
    print(exp_temp_avg)
    print('Slope of T-history regression for each experiment, combining all tows:')
    print(exp_temp_slope)
    print('Standard error in temperature for each experiment, combining all tows:')
    print(exp_temp_ste)
    print()
    print('Finished back_arrays()')
    print()
    print()

    return tow_temp_avg, tow_temp_slope, tow_temp_ste, exp_temp_avg, exp_temp_slope, exp_temp_ste  # End of function!


# Calling functions for validity check:

front_arrays()
back_arrays()