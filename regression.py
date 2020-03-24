'''Provides a function that fits an exponential curve of the form
y(x) = a*b**x
to the given data points
'''

import numpy as np
from scipy import optimize

def exp_regression(x, y, p0=None):
    '''Accepts two lists of x and y values of the data points,
    with an optional list of initial guesses for the parameters.
    Returns the fitted function y(x) = a*b**x'''
    x = np.array(x)
    y = np.array(y)
    (a, b), covariance = optimize.curve_fit(lambda t,a,b: a*b**x, x, y, p0=p0)
    print(a, b)
    return lambda x_: a*b**x_

def exp_lin_regression(x, y, p0=None):
    '''Accepts two lists of x and y values of the data points,
    with an optional list of initial guesses for the parameters.
    Returns the fitted function y(x) = a*b**x + c'''
    x = np.array(x)
    y = np.array(y)
    (a, b, c), covariance = optimize.curve_fit(lambda t,a,b,c: a*b**x+c, x, y, p0=p0)
    print(a, b, c)
    return lambda x_: a*b**x_+c


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    func = lambda x: 10*0.5**x
    x = np.linspace(0,10,50)
    y = func(x)
    plt.plot(x, y)
    y_noised = y + np.random.normal(size=x.size)
    plt.plot(x, y_noised)
    y_regressed = exp_regression(x, y_noised)(x)
    plt.plot(x, y_regressed)
    plt.show()
