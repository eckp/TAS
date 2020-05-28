'''generating the final graphs which should summarize all data'''
import numpy as np
from matplotlib import pyplot as plt
from data import *
from nip_point_front import *
from nip_point_back import *
from cooling_rate import *

# some lists of styles to use for grouping points
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

    


if __name__ == "__main__":
    pass
    # plot_all_cr(all_cooling_rates, hlines={'mean':means, 'mode':modes, 'median':medians})
    # plot_summary(means)
    # plot_summary(modes)
    # plot_summary(medians)
