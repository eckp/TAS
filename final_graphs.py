'''generating the final graphs which should summarize all data'''
import numpy as np
from matplotlib import pyplot as plt
from data import experiment_params
from box_plot_entry_exit import front_arrays, back_arrays, diff_arrays
from cooling_rate import load_cached_cr, calc_stats

# some lists of styles to use for grouping points
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = (':', '-.', '--', '-')
markers = ('o', '^', 's', 'v')

def largest_factors(n):
    for i in range(int(np.sqrt(n))+1, 0, -1):
        if n%i == 0:
            return i, n//i            

def plot_summary(values, error_bars, x_label, x_ticks, y_label, legend_names, sharex=False, sharey=True, size=(8,8)):
    '''Scatter points of values with error bars.
    values is a list of p n*m matrices for p tows (for now hard-coded as 4), where the n rows contain lines of m points 
    along which the x_label parameter varies and the legend_names parameter has a fixed value.
    error_bars is of the same shape as values, and contains scalars denoting the variance(/std dev or similar) of the averaged values'''
    rows, columns = largest_factors(len(values))
    fig, axes = plt.subplots(rows, columns, figsize=size, sharex=sharex, sharey=sharey, squeeze=False)
    # set outer labels only if the axes are shared
    if columns>1 and sharex:
        for ax in axes[-1,:]:
            ax.set_xlabel(x_label)
    if rows>1 and sharey:
        for ax in axes[:,0]:
            ax.set_ylabel(y_label)
    # one tow per subplot, optional reordering of tows by slicing the axes array
    for tow_idx, (ax, tow_values, tow_errors) in enumerate(zip(axes.flatten(), values, error_bars)):
        for line, errors, name, marker in zip(tow_values, tow_errors, legend_names, markers):
            ax.errorbar(x_ticks, line, errors, ls=(0,(2,7)), lw=1, marker=marker, capsize=3, label=name)
        # set the individual subplot labels if axes are not shared
        if not sharex:
            ax.set_xlabel(x_label)
            ax.set_xticks(x_ticks)
        if not sharey:
            ax.set_ylabel(y_label)
        ax.set_title(f'Tow nr. {tow_idx*2+1}')
        handles, labels = ax.get_legend_handles_labels()
        #ax.legend()
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    # put the legend on the top across all subplots
    fig.legend([h[0] for h in handles], labels,  # only markers and line style, no error bars in legend
               bbox_to_anchor=(0.05, 0.95, 0.9, 0.), loc='lower left', ncol= len(labels), mode="expand", borderaxespad=0)  
    plt.show()

    


if __name__ == "__main__":
    avg_size = (5,5)
    # nip point summary plot
    nip_values, nip_err, *_ = front_arrays()
    plot_summary(nip_values, nip_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]])
    # nip average over all tows
    avg_nip_values = np.array([np.mean(nip_values, axis=0)])
    avg_nip_err = np.array([np.mean(nip_err, axis=0)])
    plot_summary(avg_nip_values, avg_nip_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]], size=avg_size)
    raise RuntimeError
    # exit point summary plot
    exit_values, exit_err, *_ = back_arrays()
    plot_summary(exit_values, exit_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]])
    # exit average over all tows
    avg_exit_values = np.array([np.mean(exit_values, axis=0)])
    avg_exit_err = np.array([np.mean(exit_err, axis=0)])
    plot_summary(avg_exit_values, avg_exit_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]], size=avg_size)
    # nip-exit difference summary plot
    diff_values, diff_err, *_ = diff_arrays()
    plot_summary(diff_values, diff_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Temperature difference $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]])
    # nip-exit average over all tows
    avg_diff_values = np.array([np.mean(diff_values, axis=0)])
    avg_diff_err = np.array([np.mean(diff_err, axis=0)])
    plot_summary(avg_diff_values, avg_diff_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average temperature $[^\circ C]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]], size=avg_size)
    # cooling rate summary plot
    cr_values, cr_err, *_ = calc_stats(all_cooling_rates=load_cached_cr()[3])
    cr_values, cr_err = cr_values.T.reshape((4,3,3)), cr_err.T.reshape((4,3,3))
    plot_summary(cr_values, cr_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average cooling constant $k\ [s^{-1}]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]])
    # cooling rate average over all tows
    avg_cr_values = np.array([np.mean(cr_values, axis=0)])
    avg_cr_err = np.array([np.mean(cr_err, axis=0)])
    plot_summary(avg_cr_values, avg_cr_err, 'Compaction force $[N]$', experiment_params[:3,1],
                 'Average cooling constant $k\ [s^{-1}]$', [f'Laser power = {power} W' for power in experiment_params[::3,0]], size=avg_size)
