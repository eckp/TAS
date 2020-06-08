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

def plot_summary(values, error_bars, x_label, x_ticks, y_label, legend_names, sharex=False, sharey=True, size=(6.5,6.5)):
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
        if columns == 1 or not sharex:
            ax.set_xlabel(x_label)
            ax.set_xticks(x_ticks)
        if rows == 1 or not sharey:
            ax.set_ylabel(y_label)
        handles, labels = ax.get_legend_handles_labels()
        if rows*columns == 1:  # if there is only one subplot
            ax.set_title(f'Average of all 4 tows')
            ax.legend([h[0] for h in handles], labels)
        else:
            ax.set_title(f'Tow nr. {tow_idx*2+1}')
    fig.tight_layout()
    if rows*columns != 1:  # if there is more than one subplot
        fig.subplots_adjust(top=0.9)
        # put the legend on the top across all subplots
        fig.legend([h[0] for h in handles], labels,  # only markers and line style, no error bars in legend
                   bbox_to_anchor=(0.02, 0.95, 0.96, 0.), loc='lower left', ncol= len(labels), mode="expand", borderaxespad=0)  
    plt.show()

    


if __name__ == "__main__":
    ylabels = (*('temperature $[^\circ C]$',)*2, 'temperature difference $[^\circ C]$', 'cooling constant $k\ [s^{-1}]$')
    cr_values, cr_err = calc_stats(all_cooling_rates=load_cached_cr()[3])[0:2]  # 0:2 mean, 2:4 mode, 4:6 median
    cr_values, cr_err = cr_values.T.reshape((4,3,3)), cr_err.T.reshape((4,3,3))
    data = (front_arrays(), back_arrays(), diff_arrays(), (cr_values, cr_err))
    for ylabel, (values, err, *_) in zip(ylabels, data):
        plot_summary(values, err, 'Compaction force $[N]$', experiment_params[:3,1],
                     ylabel[0].upper()+ylabel[1:], [f'Laser power = {power} W' for power in experiment_params[::3,0]])
        plot_summary([np.mean(values, axis=0)], [np.mean(err, axis=0)], 'Compaction force $[N]$', experiment_params[:3,1],
                     'Average '+ylabel, [f'Laser power = {power} W' for power in experiment_params[::3,0]], size=(5,5))
