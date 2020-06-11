'''Calculate the cooling rates combining temperature history and regression'''
import sys
import pickle
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from data import experiment_params, numExp
from experiment_read import generate_back
from regression import get_cooling_rate, get_substrate_temp, exp_offset_regression
from temperature_history import get_temp_history

# some lists of styles to use for grouping points
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = (':', '-.', '--', '-')
markers = ('o', '^', 's', 'v')

# helper function for caching the computationally intensive results
def load_cached_cr(location='cr_cache.p'):
    return pickle.load(open(location, 'rb'))

def write_cache_cr(cr_data=None, location='cr_cache.p'):
    if cr_data is None:
        cr_data = (back, data_range, sample_range, all_tow_temp_hist, all_temp_hist, select_temp_hist, all_cooling_rates, select_cooling_rates, all_substrate_temps, select_substrate_temps, means, sse, modes, modes_rmse, medians, medians_rmse)
    pickle.dump(cr_data, open(location, 'wb'))

# helper function for computing the root mean squared error
def rmse(target, prediction):
    return np.sqrt(np.mean((target-prediction)**2))
    
# computation functions
def calc_temp_hist(data=None, data_range=slice(0,-1)):
    if data is None:
        data = [generate_back(i) for i in range(numExp)]
    all_temp_hist = []
    for iexp, exp in enumerate(data):
        time = exp.time  # get the time list of this experiment
        exp_temp_hist = []
        for itow, tow in enumerate(exp.tows):#[0:8:2]):  # odd tows 1 through 7 (zero-based indexing, though)
            print(f'Temp hist: experiment {iexp+1}, tow nr. {itow+1}')
            tow_time_temps = np.array([get_temp_history(time, tow, itow//2, sample_idx=sample_idx) for sample_idx, sample_time in enumerate(time[data_range])])
            exp_temp_hist.append(tow_time_temps)
        all_temp_hist.append(exp_temp_hist)
    return np.array(all_temp_hist)

def calc_cr(all_temp_hist=None, sample_range=slice(180, 650)):
    '''Calculate the cooling rates per experiment per tow from the temperature data of the tows.
    data thus is an array with 9 entries containing 4 temperature series of the 4 tows.
    Return the cooling rate at all locations along a run (within the sample_range) for 4 tows for 9 experiments.
    sample_range is a tuple specifying the range of samples along which the cooling rate will be calculated.
    Needs to be set carefully to exclude chaotic start-up and cool-down regions, 
    as the curve_fit might not cope with too irregular data.'''
    if all_temp_hist is None:
        all_temp_hist = calc_temp_hist()
    all_cr = []
    for iexp, exp_temp_hist in enumerate(all_temp_hist):
        exp_cr = []
        for itow, tow_temp_hist in enumerate(exp_temp_hist):
            print(f'Cooling rate: experiment {iexp+1}, tow nr. {itow+1}')
            try:
                tow_cr = [get_cooling_rate(temp_hist, time_map) for time_map, temp_hist  in tow_temp_hist[sample_range]]  # right now this slices the previously already sliced temperature history
            finally:
                exp_cr.append(tow_cr)
        all_cr.append(exp_cr)
    return np.array(all_cr)

def calc_ts(all_temp_hist=None, sample_range=slice(180, 650)):
    '''Calculate the substrate temperature per experiment per tow from the temperature data of the tows.
    data thus is an array with 9 entries containing 4 temperature series of the 4 tows.
    Return the cooling rate at all locations along a run (within the sample_range) for 4 tows for 9 experiments.
    sample_range is a tuple specifying the range of samples along which the cooling rate will be calculated.
    Needs to be set carefully to exclude chaotic start-up and cool-down regions, 
    as the curve_fit might not cope with too irregular data.'''
    if all_temp_hist is None:
        all_temp_hist = calc_temp_hist()
    all_ts = []
    for iexp, exp_temp_hist in enumerate(all_temp_hist):
        exp_ts = []
        for itow, tow_temp_hist in enumerate(exp_temp_hist):
            print(f'Substrate temperature: experiment {iexp+1}, tow nr. {itow+1}')
            try:
                tow_ts = [get_substrate_temp(temp_hist, time_map) for time_map, temp_hist  in tow_temp_hist[sample_range]]  # right now this slices the previously already sliced temperature history
            finally:
                exp_ts.append(tow_ts)
        all_ts.append(exp_ts)
    return np.array(all_ts)


def calc_stats(all_cooling_rates=None, mode_rounding=2):
    '''Calculate the mean, mode and median cooling rate for each tow.
    Additionally calculates the standard error, to be used for plotting 1 SE error bars around the mean data points.'''
    if all_cooling_rates is None:
        all_cooling_rates = calc_cr()
    all_cooling_rates[0][1][0] = np.nan  # exclude tow 3 from exp 1 from the computations
    means = [[np.mean(tow_crs) for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
    sse = [[np.std(tow_crs) for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
    modes = [[stats.mode(np.round(tow_crs, mode_rounding), axis=None)[0] for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
    modes_rmse = [[rmse(tow_crs, tow_mode) for tow_crs, tow_mode in zip(exp_crs, exp_modes)] for exp_crs, exp_modes in zip(all_cooling_rates, modes)]
    medians = [[np.median(tow_crs) for tow_crs in exp_crs] for exp_crs in all_cooling_rates]
    medians_rmse = [[rmse(tow_crs, tow_median) for tow_crs, tow_median in zip(exp_crs, exp_medians)] for exp_crs, exp_medians in zip(all_cooling_rates, medians)]
    return np.array(means), np.array(sse), np.array(modes), np.array(modes_rmse), np.array(medians), np.array(medians_rmse)

# cooling rate-related plotting functions
def plot_pseudo_IR(all_temp_hist, tow_idx=0):
    '''Plot a heat color map of the time histories of points along the run'''
    fig, axes = plt.subplots(3,3, figsize=(12,12))#, sharex=True, sharey=True)
    for exp_idx, (exp_temp_hist, ax) in enumerate(zip(all_temp_hist, axes.flatten())):
        ax.pcolor(exp_temp_hist[tow_idx][:,1,:].T, cmap='inferno')
    plt.show()

def plot_temp_hist(all_temp_hist, tow_idx=0):
    '''Plot all temperature histories along one tow over each other (temperature as a function of time).'''
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for exp_idx, (exp_temp_hist, ax) in enumerate(zip(all_temp_hist, axes.flatten())):
        rel_time = exp_temp_hist[tow_idx][0,0,:]
        for temp_h in exp_temp_hist[tow_idx][:,1,:]:
            ax.plot(rel_time, temp_h)
    plt.show()

def plot_temp_series(data, tow_idx=0):
    '''Plots the temperatures for one tow measured by the 10 trailing lines'''
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for exp_idx, (exp, ax) in enumerate(zip(data, axes.flatten())):
        time = exp.time
        tow = exp.tows[tow_idx]
        for line in tow:
            ax.plot(time, line)
    plt.show()

def plot_all_cr(all_cr, hlines={}):
    '''Plot the cooling rates along the entire run per tow per experiment in a 3*3 subplot.
    optionally add horizontal lines'''
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for ax in axes[-1,:]:
            ax.set_xlabel('Sampling point along run')
    for ax in axes[:,0]:
            ax.set_ylabel('Cooling constant $k\ [s^{-1}]$')
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

def plot_all_ts(all_ts, hlines={}):
    '''Plot the substrate temperatures along the entire run per tow per experiment in a 3*3 subplot.
    optionally add horizontal lines'''
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for ax in axes[-1,:]:
            ax.set_xlabel('Sampling point along run')
    for ax in axes[:,0]:
            ax.set_ylabel('Substrate temperature $T_s\ [^{\circ} C]$')
    for exp_idx, (exp_ts, ax) in enumerate(zip(all_ts, axes.flatten())):
        for tow_idx, tow_ts in enumerate(exp_ts):
            exp_params = experiment_params[exp_idx]
            ax.set_title(f'Experiment {exp_idx+1}: power = {exp_params[0]} W, force = {exp_params[1]} N')
            ax.plot(list(range(sample_range.start, sample_range.start+len(tow_ts))), tow_ts, c=colors[tow_idx])
            for line, style in zip(hlines, linestyles):
                ax.axhline(hlines[line][exp_idx][tow_idx], c=colors[tow_idx], linestyle=style, label=line)
    fig.legend(handles=[plt.Line2D([0], [0], c=colors[idx], label=f'tow nr. {idx*2+1}') for idx in range(tow_idx+1)] +
                       [plt.Line2D([0], [0], c='k', ls=linestyle, label=name) for name, linestyle in zip(hlines, linestyles[0:len(hlines)])])
    fig.tight_layout()
    plt.show()
    
def plot_ts_vs_cr(cr, ts):
    '''Plot the cooling rates versus substrate temperature'''
    
    fig, axes = plt.subplots(3,3, figsize=(12,12), sharex=True, sharey=True)
    for ax in axes[-1,:]:
            ax.set_xlabel(r'Subtrate temperature $[^{\circ} C]$')
    for ax in axes[:,0]:
            ax.set_ylabel('Cooling constant $k\ [s^{-1}]$')

    for i in range(0, 9):
        for j in range(0, 4):
            axes.flatten()[i].scatter(ts[i][j], cr[i][j])
    fig.tight_layout()
    plt.show()

def plot_curve_fit_comparison(all_temp_hist, exp_idx, tow_idx, sample_idx, fixed=False, extend=False):
    '''Plot the experimental data and the fitted curve for comparison.'''
    time, temp = all_temp_hist[exp_idx][tow_idx][sample_idx]
    f_time, f_temp = time[0:6], temp[0:6]  # 'fix': only use the first 6 measurement lines
    func, params = exp_offset_regression(time, temp, p0=(temp[0]-temp[-1], 0.5, temp[-1]), bounds=([0, 0, 75], [300, 1, 200]))
    f_func, f_params = exp_offset_regression(f_time, f_temp, p0=(f_temp[0]-f_temp[-1], 0.5, f_temp[-1]), bounds=([0, 0, 75], [300, 1, 200]))
    fig, ax = plt.subplots(figsize=(5,3.5))
    ax.set_title(f'Point {sample_idx} from tow {tow_idx*2+1}, experiment {exp_idx+1}')
    ax.set_xlabel('Time $[s]$')
    ax.set_ylabel('Temperature $[^{\circ} C]$')
    ax.plot(time, temp, marker=markers[0], label='Temperature history')
    ax.plot(time, func(time), marker=markers[1], label='Exponential curve fit')
    if fixed:
        if extend:
            ax.plot(time, f_func(time), marker=markers[2], markevery=[0,2,4,6,7,8,9], label='Fixed exponential curve fit')
        else:
            ax.plot(f_time, f_func(f_time), marker=markers[2], markevery=[0,2,4], label='Fixed exponential curve fit')
    ax.legend()
    fig.tight_layout()
    plt.show()
    
    
if __name__ == '__main__':
    if '-o' in sys.argv:
        back, data_range, sample_range, all_tow_temp_hist, all_temp_hist, select_temp_hist, all_cooling_rates, select_cooling_rates, all_substrate_temps, select_substrate_temps, means, sse, modes, modes_rmse, medians, medians_rmse = load_cached_cr()
    else:
        back = [generate_back(i) for i in range(numExp)]
        data_range = slice(0, -1)
        sample_range = slice(180, 650)
        all_tow_temp_hist = calc_temp_hist(data=back, data_range=data_range)  # also for the inactive tows
        all_temp_hist = all_tow_temp_hist[:,0:8:2]  # select only active tows
        # select only the first few measurement lines, as there is a kink from line 7 onwards
        select_temp_hist = [[np.array(tow[:,:,0:6]) for tow in exp] for exp in all_temp_hist]
        all_cooling_rates = calc_cr(all_temp_hist=all_temp_hist, sample_range=sample_range)
        select_cooling_rates = calc_cr(all_temp_hist=select_temp_hist, sample_range=sample_range)
        means, sse, modes, modes_rmse, medians, medians_rmse = calc_stats(select_cooling_rates)
        all_substrate_temps = calc_ts(all_temp_hist=all_temp_hist, sample_range=sample_range)
        select_substrate_temps = calc_ts(all_temp_hist=select_temp_hist, sample_range=sample_range)
        if '-s' in sys.argv:
            write_cache_cr()
    plot_all_cr(all_cooling_rates)
    plot_all_ts(all_substrate_temps)
    plot_ts_vs_cr(all_cooling_rates, all_substrate_temps)
    plot_all_cr(select_cooling_rates, hlines={'mean':means, 'mode':modes})
    plot_all_ts(select_substrate_temps)
    plot_ts_vs_cr(select_cooling_rates, select_substrate_temps)

    # investigating if bad curve fits have something to do with the hot spots on the empty tows
    e6t4_th = all_tow_temp_hist[5][3]  # temp hist of empty tow to the left of tow 5
    e6t5_ts = select_substrate_temps[5][2]  # curve fit substrate temp of tow 5
    e6t6_th = all_tow_temp_hist[5][5]  # temp hist of empty tow to the right of tow 5
    fig, axes = plt.subplots(3,1, sharex=True)
    axes[0].pcolor(e6t4_th[:,1,:].T, cmap='inferno')
    axes[1].plot(range(180, 650), e6t5_ts)
    axes[2].pcolor(e6t6_th[:,1,:].T, cmap='inferno')
    fig.tight_layout()
    plt.show()
