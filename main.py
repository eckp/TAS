'''main.py, connecting all the separate functions'''

import numpy as np
from matplotlib import pyplot as plt
from experiment_read import generate_front, generate_back
from regression import exp_regression, exp_lin_regression

exp_back = [generate_back(i) for i in range(9)]
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# exponential regression of the cooling rate
for i, exp in enumerate(exp_back[::2]):
    x = np.arange(len(exp.tow1))
    y = exp.tow1[:,300]
    #print(list(zip(x,y)))
    plt.plot(x, y, c=colors[i])
    plt.plot(x, exp_regression(x, y)(x), c=colors[i], linestyle='--')
plt.show()
