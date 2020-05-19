'''generating the final graphs which should summarize all data'''
import sys
import pickle
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from data import *
from experiment_read import *
from regression import get_cooling_rate
from temperature_history import get_temp_history

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = (':', '-.', '--', '-')

def plot_all_cr(all_cr, hlines={}):
    fig, axes = plt.subplots(3,3, figsize=(12,12))#, sharex=True, sharey=True)
    for exp_idx, (exp_cr, ax) in enumerate(zip(all_cr, axes.flatten())):
        for tow_idx, tow_cr in enumerate(exp_cr):
            exp_params = experiment_params[exp_idx]
            ax.set_title(f'Experiment {exp_idx+1}: power = {exp_params[0]} W, force = {exp_params[1]} N')
            ax.plot(list(range(*sample_range)), tow_cr, c=colors[tow_idx])
            for line, style in zip(hlines, linestyles):
                ax.axhline(hlines[line][exp_idx][tow_idx], c=colors[tow_idx], linestyle=style, label=line)
    fig.legend(handles=[plt.Line2D([0], [0], c=colors[idx], label=f'tow nr. {idx*2+1}') for idx in range(tow_idx+1)] +
                       [plt.Line2D([0], [0], c='k', ls=linestyle, label=name) for name, linestyle in zip(hlines, linestyles[0:len(hlines)])])
    fig.tight_layout()
    plt.show()

def plot_summary(averaged_points, laser_x=False):
    '''Accept list of 9 experiments with list of cooling rates of 4 tows each.
    Setting laser_x=True invert the plot in the sense that there will be 
    three lines of different force, and that the laser power will be on the x-axis.'''
    fig, axes = plt.subplots(2,2, figsize=(10,10), sharex=False, sharey=True)
    data = np.array(averaged_points).reshape(3,3,4)
    experiment_parameters = np.array(experiment_params).reshape(3,3,2)
    for tow_idx, (tow_data, ax) in enumerate(zip(data.T, axes.flatten()[[0,2,3,1]])):
        if laser_x:
            tow_data = tow_data
            exp_prms = np.transpose(experiment_parameters, (1,0,2))
            x_ticks_idx = 0
            x_label = 'Laser power $[W]$'
            line_label = lambda force: f'{force} $N$'
        else:
            tow_data = tow_data.T
            exp_prms = experiment_parameters
            x_ticks_idx = 1
            x_label = 'Compaction force $[N]$'
            line_label = lambda power: f'{power} $W$'
        for settings, line in zip(exp_prms, tow_data):
            x = settings[:,x_ticks_idx]
            ax.set_xlabel(x_label)
            ax.set_ylabel('Cooling speed $k\ [s^{-1}]$')
            ax.set_title(f'Cooling speed for {("outer", "inner")[tow_idx in (1,2)]} tow {tow_idx*2+1}')
            ax.set_xticks(x)
            ax.plot(x, line, label=line_label(settings[0,~x_ticks_idx]))
            ax.legend()
    fig.tight_layout()
    plt.show()

def export_rates(location='cooling/cooling_rate_dump', num=1):
    import csv
    for exp_n, exp_rates in enumerate(all_cooling_rates):
        with open(f'{location}{num}_exp{exp_n+1}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for line in zip(*exp_rates):
                writer.writerow(line)

if __name__ == "__main__":
    if '-o' in sys.argv:
        sample_range, all_cooling_rates, means, modes, medians = pickle.load(open('cr_cache.p', 'rb'))
    else:
        back = {f'Exp{i + 1}' : [generate_back(i), experiment_params[i]] for i in range(numExp)} #rear camera data
        # sample the temp history along the sample range
        sample_range = (200, 600)  # range of indices to sample
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
    plot_all_cr(all_cooling_rates, hlines={'mean':means, 'mode':modes, 'median':medians})
    plot_summary(means)
    plot_summary(modes)
    plot_summary(medians)
