'''generating the final graphs which should summarize all data'''
import numpy as np
from matplotlib import pyplot as plt
from data import experiment_params
from box_plot_entry_exit import front_arrays, back_arrays
from cooling_rate import load_cached_cr, calc_stats

# some lists of styles to use for grouping points
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = (':', '-.', '--', '-')
markers = ('o', '^', 's', 'v')

def plot_summary(values, error_bars, x_label, x_ticks, y_label, legend_names, sharex=False, sharey=True):
    '''Scatter points of values with error bars.
    values is a list of p n*m matrices for p tows (for now hard-coded as 4), where the n rows contain lines of m points 
    along which the x_label parameter varies and the legend_names parameter has a fixed value.
    error_bars is of the same shape as values, and contains scalars denoting the variance(/std dev or similar) of the averaged values'''
    fig, axes = plt.subplots(2, 2, figsize=(8,8), sharex=sharex, sharey=sharey)
    # set outer labels only if the axes are shared
    if sharex:
        for ax in axes[-1,:]:
            ax.set_xlabel(x_label)
    if sharey:
        for ax in axes[:,0]:
            ax.set_ylabel(y_label)
    # one tow per subplot, optional reordering of tows by slicing the axes array
    for ax, tow_values, tow_errors in zip(axes.flatten(), values, error_bars):
        for line, errors, name, marker in zip(tow_values, tow_errors, legend_names, markers):
            ax.errorbar(x_ticks, line, errors, ls=(0,(2,7)), lw=1, marker=marker, capsize=3, label=name)
        # set the individual subplot labels if axes are not shared
        if not sharex:
            ax.set_xlabel(x_label)
            ax.set_xticks(x_ticks)
        if not sharey:
            ax.set_ylabel(y_label)
        ax.legend()
    fig.tight_layout()
    plt.show()

    


if __name__ == "__main__":
    # nip point summary plot
    nip_values, nip_err, *_ = front_arrays()
    plot_summary(nip_values, nip_err, 'Compaction force $[N]$', experiment_params[::3,0],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[:3,1]])
    # exit point summary plot
    exit_values, exit_err, *_ = back_arrays()
    plot_summary(exit_values, exit_err, 'Compaction force $[N]$', experiment_params[::3,0],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[:3,1]])
    # cooling rate summary plot
    data_range, sample_range, back, all_cooling_rates, means, modes, medians = load_cached_cr()
    cr_values, _, _, cr_err = calc_stats(all_cooling_rates=all_cooling_rates)
    plot_summary(cr_values.T.reshape((4,3,3)), cr_err.T.reshape((4,3,3)), 'Compaction force $[N]$', experiment_params[::3,0],
                 'Cooling constant $k\ [s^{-1}]$', [f'Laser power = {power} W' for power in experiment_params[:3,1]])
