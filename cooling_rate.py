'''Calculate the cooling rates combining temperature history and regression'''
import sys
import pickle
from scipy import stats
from experiment_read import *
from regression import get_cooling_rate
from temperature_history import get_temp_history


# def export_rates(location='cooling/cooling_rate_dump', num=1):
#     import csv
#     for exp_n, exp_rates in enumerate(all_cooling_rates):
#         with open(f'{location}{num}_exp{exp_n+1}.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             for line in zip(*exp_rates):
#                 writer.writerow(line)

if '-o' in sys.argv:
    sample_range, all_cooling_rates, means, modes, medians = pickle.load(open('cr_cache.p', 'rb'))
else:
    back = {f'Exp{i + 1}' : [generate_back(i), experiment_params[i]] for i in range(numExp)} #rear camera data
    # sample the temp history along the sample range
    sample_range = (80, 720)  # range of indices to sample
    all_cooling_rates = []
    for exp in back.values():
        exp_cooling_rates = []
        for itow in range(0,8,2):  # odd tows 1 through 7
            print(f'experiment {exp[1]}, tow nr. {itow+1}')
            time = exp[0].time  # get the time list of this tow
            tow_temp = exp[0].tows[itow]  # get the temperature data of this tow
            tow_time_temps = np.array([get_temp_history(time, tow_temp, itow//2, sample_idx=sample_idx) for sample_idx in range(*sample_range)])
            #            plt.pcolor(tow_time_temps[:,1,:].T, cmap='inferno')
            #            plt.show()
            #            for temp_h in tow_time_temps[:,1,:]:
            #                plt.plot(tow_time_temps[0,0,:], temp_h)
            #            plt.show()
            try:
                tow_cooling_rates = [get_cooling_rate(temp_hist, time_map) for time_map, temp_hist  in tow_time_temps]#[sample_range[0]:sample_range[1]+1]]
            finally:
                exp_cooling_rates.append(tow_cooling_rates)
                #            plt.plot(list(range(*sample_range)), tow_cooling_rates)
                #            plt.show()
        all_cooling_rates.append(exp_cooling_rates)
        means = [[np.mean(tow_crs) for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
        modes = [[stats.mode(np.round(tow_crs,2), axis=None)[0] for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
        medians = [[np.median(tow_crs) for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
    if '-s' in sys.argv:
        pickle.dump((sample_range, all_cooling_rates, means, modes, medians), open('cr_cache.p', 'wb'))
