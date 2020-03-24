'''Provide functions that fit exponential curves to a given set of data points.'''

import numpy as np
from scipy import optimize

def exp_regression(x, y, p0=None):
    '''Accept two lists of x and y values of the data points,
    with an optional list of initial guesses for the parameters.
    Return the fitted function y(x) = a*b**x and the parameters for later use'''
    x = np.array(x)
    y = np.array(y)
    (a, b), covariance = optimize.curve_fit(lambda t,a,b: a*b**x, x, y, p0=p0)
    print(a, b)
    func = lambda x_: a*b**x_
    return func, (a, b)

def exp_lin_regression(x, y, p0=None):
    '''Accept two lists of x and y values of the data points,
    with an optional list of initial guesses for the parameters.
    Return the fitted function y(x) = a*b**x + c and the parameters for later use'''
    x = np.array(x)
    y = np.array(y)
    (a, b, c), covariance = optimize.curve_fit(lambda t,a,b,c: a*b**x+c, x, y, p0=p0)
    print(a, b, c)
    func = lambda x_: a*b**x_+c
    return func, (a, b, c)


def cooling_rate(experiments):
    '''Accept a list of experiments with one list of timestamps and n tows per experiment,
    where the tow is a list of the temperature values of a point (averaged or just a sample).
    Return a list of the cooling rate per tow per experiment.'''
    cooling_rates = np.empty((len(experiments), len(experiments[0].samples)))
    for i, experiment in enumerate(experiments):
        t = np.arange(0,10)  # number of lines per tow
        for j, tow in enumerate(experiment.samples):
            print(tow)
            cooling_rates[i,j] = exp_lin_regression(t, tow, p0=(tow[0]-tow[-1], 0.9, tow[-1]))[1][1]
    return cooling_rates

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    a, b, c = 34, 0.55, 10
    func = lambda x: a*b**x+c
    x = np.linspace(0,10,50)
    y = func(x)
    plt.plot(x, y, label=f'original: y(x) = {a}*{b}**x+{c}')
    y_noised = y + np.random.normal(size=x.size)
    plt.plot(x, y_noised, label='original + noise')
    regress = exp_lin_regression(x, y_noised)
    y_regressed = regress[0](x)
    plt.plot(x, y_regressed, label=f'regressed: y(x) = {round(regress[1][0], 2)}*{round(regress[1][1], 2)}**x+{round(regress[1][2], 2)}')
    #plt.annotate(f'y(x) = {round(regress[1][0], 2)}*{round(regress[1][1], 2)}**x+{round(regress[1][2], 2)}',
    #             (x[int(len(x)*0.2)]*1.2, y_regressed[int(len(x)*0.2)]*1.2))
    plt.legend()
    plt.show()
