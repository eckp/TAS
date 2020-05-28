'''generating the final graphs which should summarize all data'''
import numpy as np
from matplotlib import pyplot as plt
from data import *
from nip_point_front import *
from nip_point_back import *
from cooling_rate import *

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = (':', '-.', '--', '-')
markers = ('o', '^', 's', 'v')

def plot_summary(values, error_measure, x_label, x_ticks, y_label, legend_names, sharex=False, sharey=True):
    '''Scatter points of values with error bars.
    values is a list of p n*m matrices for p tows (for now hard-coded as 4), where the n rows contain lines of m points 
    along which the x_label parameter varies and the legend_names parameter has a fixed value.
    error_measure is of the same shape as values, and contains scalars denoting the variance of the averaged values'''
    fig, axes = plt.subplots(2, 2, figsize=(10,10), sharex=sharex, sharey=sharey)
    # set outer labels only if the axes are shared
    if sharex:
        for ax in axes[-1,:]:
            ax.set_xlabel(x_label)
    if sharey:
        for ax in axes[:,0]:
            ax.set_ylabel(y_label)
    # one tow per subplot, optional reordering of tows by slicing the axes array
    for ax, tow_values, tow_errors in zip(axes.flatten(), values, error_measure):
        for line, errors, name, marker in zip(tow_values, tow_errors, legend_names, markers):
            ax.errorbar(x_ticks, line, errors, ls=(0,(2,7)), lw=1, marker=marker, capsize=3, label=name)
        # set the individual subplot labels if axes are not shared
        if not sharex:
            ax.set_xlabel(x_label)
            ax.set_xticks(x_ticks)
        if not sharey:
            ax.set_ylabel(y_label)
        ax.legend()
    plt.show()


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
    
def old_plot_summary(averaged_points, laser_x=False):
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
            ax.fill_between(x, line*0.8, line*1.2, alpha=0.2)  # use plt.errorbar
            ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    pass
    # plot_all_cr(all_cooling_rates, hlines={'mean':means, 'mode':modes, 'median':medians})
    # plot_summary(means)
    # plot_summary(modes)
    # plot_summary(medians)
