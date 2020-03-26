'''main.py, connecting all the separate functions'''

import numpy as np
from matplotlib import pyplot as plt
from experiment_read import generate_front, generate_back
from regression import cooling_rate
from final_graphs import final_graph

exp_back = [generate_back(i) for i in range(9)]
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']  # for grouping plot elements by color

# requires the temperature histories and time_map to be generated first
#cooling_rates = cooling_rate(temperature_histories, time_map)
#final_graph(cooling_rates, 0)
