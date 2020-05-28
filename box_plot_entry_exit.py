from experiment_read import *
import matplotlib.pyplot as plt


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

# Generate average temperature and variance for each tow and experiment

"""
    This function creates four arrays. These are divided in two groups: 
    - Per tow measurements
        "tow_temp_avg" and "tow_temp_var" contains four 3x3 matrices. Each matrix corresponds to each tow (tows 1, 
        3, 5 and 7), and each matrix has three rows and three columns. Each row corresponds to a power setting 
        (1300 W, 1500 W, and 1750 W respectively), while each column corresponds to a compaction force. 
        
        This is how each matrix is structured:
                [ exp1  exp2    exp3
                  exp4  exp5    exp6
                  exp7  exp8    exp9 ]
        
        "tow_temp_avg" contains all the average temperatures per tow per experiment, while "tow_temp_var" contains 
        the variance in temperature. 
        
    - Per experiment measurements
        Very similar as the previous arrays, but this time there is only one matrix per array, containing the average
        and variance in "exp_temp_avg" and "exp_temp_var" respectively.
"""

def front_arrays():

    tow_temp_avg = np.zeros((4,3,3))
    tow_temp_var = np.zeros((4,3,3))
    exp_temp_avg = np.zeros((3,3))
    exp_temp_var = np.zeros((3,3))

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
                tow_temp_var[j][k][i] = np.var(tow_temp_interval) # Compute variance in the temperature

                # In case you want to see the line for each measurement (Select and "ctrl" +  "/" to uncomment ):
                # plt.plot(time_interval,tow_temp_interval)
                # plt.show()

                # Now make a temperature line for the experiment by combining the tow measurements

                if i + k == 0 and j != 1: # This excludes the bad measurements from tow 3 in exp no. 1
                    average_temp_front += 1 / 3 * tow_temp_interval

                elif i + k != 0:
                    average_temp_front += 0.25 * tow_temp_interval

            exp_temp_avg[k][i] = np.mean(average_temp_front) # Compute mean temperature
            exp_temp_var[k][i] = np.var(average_temp_front) # Compute variance in the temperature

    print('Average temperature of each tow for each experiment:')
    print(tow_temp_avg)
    print('Variance in temperature of each tow for each experiment:')
    print(tow_temp_var)
    print('Average temperature for each experiment, combining all tows:')
    print(exp_temp_avg)
    print('Variance in temperature for each experiment, combining all tows:')
    print(exp_temp_var)

    return tow_temp_avg, tow_temp_var, exp_temp_avg, exp_temp_var # End of function!!!


# Calling functions for validity check:
front_arrays()