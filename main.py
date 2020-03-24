'''main.py, connecting all the separate functions'''

import numpy as np
from matplotlib import pyplot as plt
from experiment_read import generate_front, generate_back
from regression import exp_regression, exp_lin_regression, cooling_rate

exp_back = [generate_back(i) for i in range(9)]
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# cooling rate per tow per experiment
cooling_rates = cooling_rate(exp_back)
for i, exp in enumerate(cooling_rates):
    plt.plot([i]*len(exp), exp, 'o')
plt.show()
