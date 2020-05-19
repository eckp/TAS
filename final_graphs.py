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

def final_graph(cooling_rate, n_exp):
    '''Accepts cooling rate and tow number (0-3) to generate a graph
    with compaction force, laser power and cooling rate combined.
    Returns the matrix with graph data, where the compaction force is
    held constant throughout the columns and laser power throughout rows.'''
    
    graph_data = np.empty((3,3))
    n_points = len(experiment_params[:,0])
    xgraph = []
    comp_force = []

    # Generate usable matrix for graphs
    for i in range(int(n_points/3)):
        xgraph.append(experiment_params[i*3,0])
        comp_force.append(experiment_params[i,1])
        for j in range(int(n_points/3)):
            counter = i * 3 + j
            #columns -> constant comp. force
            #rows -> constant laser power
            graph_data[i,j] = cooling_rate[counter,n_exp]

    # Plot graphs
    for k in range(int(n_points/3)):
        ygraph = graph_data[:,k]
        plt.plot(xgraph, ygraph, label=comp_force[k])

    plt.legend()
    plt.show()
    return graph_data

def plot_all_cr(all_cr, hlines={}):
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for exp_idx, (exp_cr, ax) in enumerate(zip(all_cr, axes.flatten())):
        for tow_idx, tow_cr in enumerate(exp_cr):
            exp_params = experiment_params[exp_idx]
            ax.set_title(f'Experiment {exp_idx+1}: power = {exp_params[0]} W, force = {exp_params[1]} N')
            ax.plot(list(range(*sample_range)), tow_cr, c=colors[tow_idx])
            for line, style in zip(hlines, linestyles):
                ax.axhline(hlines[line][exp_idx][tow_idx], c=colors[tow_idx], linestyle=style, label=line)
    fig.legend(handles=[plt.Line2D([0], [0], c=colors[idx], label=f'tow nr. {idx*2+1}') for idx in range(tow_idx+1)] +
                       [plt.Line2D([0], [0], c='k', ls=linestyle, label=name) for name, linestyle in zip(hlines, linestyles[0:len(hlines)])])
    plt.show()


def save_rates(location='cooling/cooling_rate_dump', num=1):
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
        sample_range = (100, 700)  # range of indices to sample
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
            modes = [[stats.mode(np.round(tow_crs,3), axis=None)[0] for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
            medians = [[np.median(tow_crs) for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
        if '-s' in sys.argv:
            pickle.dump((sample_range, all_cooling_rates, means, modes, medians), open('cr_cache.p', 'wb'))
    plot_all_cr(all_cooling_rates, hlines={'mean':means, 'mode':modes, 'median':medians})


#    print(experiment_params)
#    graph_data = final_graph(cooling_rate, 0)
#    print(graph_data)
