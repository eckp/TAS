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
#    print(a, b)
    func = lambda x_: a*b**x_
    return func, (a, b)

def exp_offset_regression(x, y, p0=None, bounds=(-np.inf, np.inf)):
    '''Accept two lists of x and y values of the data points,
    with an optional list of initial guesses for the parameters.
    Return the fitted function y(x) = a*b**x + c and the parameters for later use'''
    x = np.array(x)
    y = np.array(y)
    (a, b, c), covariance = optimize.curve_fit(lambda t,a,b,c: a*b**x+c, x, y, p0=p0, bounds=bounds)
#    print(a, b, c)
    func = lambda x_: a*b**x_+c
    return func, (a, b, c)

def get_cooling_rate(tow, time_map):
    '''Calculate the cooling rate of a single tow'''
    # initial guesses (delta T, exponential base b and limit temperature)
    p0 = (tow[0]-tow[-1], 0.5, tow[-1])
    bounds = ([0,0,0], [300,1,300])  # bound the temperature delta to a realistic 0-300K, the base to 0-1 (temperature cannot become negative, nor on average increase during cooldown) and the limit temperature (cannot be negative and will be below 300C for sure)
    _, curve_parameters = exp_offset_regression(time_map, tow, p0=p0, bounds=bounds)
    return -np.log(curve_parameters[1])

def get_substrate_temp(tow, time_map):
    '''Calculate the limit substrate temperature of a single tow'''
    # initial guesses (delta T, exponential base b and limit temperature)
    p0 = (tow[0]-tow[-1], 0.5, tow[-1])
    bounds = ([0,0,0], [300,1,300])  # bound the temperature delta to a realistic 0-300K, the base to 0-1 (temperature cannot become negative, nor on average increase during cooldown) and the limit temperature (cannot be negative and will be below 300C for sure)
    _, curve_parameters = exp_offset_regression(time_map, tow, p0=p0, bounds=bounds)
    return curve_parameters[2]

def get_cooling_rates(temperature_histories, time_map):
    '''Accept a list of experiments with the temperature history of a point on n tows per experiment,
    (which can be averaged or just a sample).
    temperature_histories should look like:
        [[[exp1_tow1_temp0, ..., exp1_tow1_temp10], ..., [exp1_tow7_temp0, ..., exp1_tow7_temp10]],
         ...,
         [[exp9_tow1_temp0, ..., exp9_tow1_temp10], ..., [exp9_tow7_temp0, ..., exp9_tow7_temp10]]]
    The time_map list is a list that contains the time-offset values of each line(/temperature measurement) 
    from the first line. It's like a list of x-values for the all the lists of y-values in the temperature histories. 
    Return a list of the cooling rate per tow per experiment.'''
    cooling_rates = np.empty(temperature_histories.shape[:-1])  # make an empty array to fit the cooling rates into
    for i, experiment in enumerate(temperature_histories):
        #t = np.arange(len(experiment[0,0]))  # number of measurement lines per tow, for now
        t = time_map  # time offset of each measurement from the first measurement line
        for j, tow in enumerate(experiment):
            print(tow)
            cooling_rates[i,j] = get_cooling_rate(tow, t)
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
    regress = exp_offset_regression(x, y_noised)
    y_regressed = regress[0](x)
    plt.plot(x, y_regressed, label=f'regressed: y(x) = {round(regress[1][0], 2)}*{round(regress[1][1], 2)}**x+{round(regress[1][2], 2)}')
    #plt.annotate(f'y(x) = {round(regress[1][0], 2)}*{round(regress[1][1], 2)}**x+{round(regress[1][2], 2)}',
    #             (x[int(len(x)*0.2)]*1.2, y_regressed[int(len(x)*0.2)]*1.2))
    plt.legend()
    plt.show()

    # cooling rate per tow per experiment
    # sample data for testing
    sample_temp_hists = np.array([[[197.97, 175.72, 162.1, 151.02, 142.66, 137.97, 131.97, 121.51, 117.5, 114.36],
                                   [216.01, 193.8, 178.61, 169.44, 161.63, 154.79, 147.63, 138.27, 133.54, 129.71],
                                   [208.47, 187.63, 174.42, 165.47, 156.1, 149.56, 137.73, 127.93, 122.62, 119.23],
                                   [211.59, 189.13, 172.76, 159.41, 150.53, 143.16, 136.53, 129.54, 124.81, 121.0]],
                                  [[153.88, 118.8, 111.28, 105.08, 100.1, 97.71, 93.01, 87.7, 85.47, 83.79],
                                   [162.61, 127.86, 119.33, 114.62, 110.72, 107.37, 101.11, 94.57, 92.24, 89.78],
                                   [162.04, 126.33, 118.88, 114.12, 109.77, 105.81, 96.84, 91.97, 89.12, 87.62],
                                   [155.28, 120.13, 112.11, 106.19, 101.88, 97.88, 92.37, 88.7, 86.77, 85.04]],
                                  [[177.28, 163.51, 151.92, 142.64, 134.69, 130.16, 119.6, 114.37, 110.75, 108.29],
                                   [184.81, 173.06, 161.37, 154.38, 148.16, 141.97, 129.43, 123.37, 119.77, 116.79],
                                   [184.33, 170.78, 158.64, 150.93, 143.54, 135.35, 119.81, 113.79, 110.04, 107.97],
                                   [178.66, 163.32, 150.94, 141.11, 134.02, 126.97, 116.83, 112.1, 109.69, 107.55]],
                                  [[213.24, 189.51, 174.84, 163.14, 153.42, 148.18, 141.94, 130.81, 126.6, 123.06],
                                   [226.08, 203.5, 188.07, 178.84, 170.61, 163.06, 153.81, 141.71, 135.51, 130.66],
                                   [223.63, 200.79, 185.73, 175.44, 166.57, 158.81, 146.18, 136.84, 131.94, 128.25],
                                   [220.14, 196.46, 179.81, 167.12, 158.2, 150.02, 142.45, 134.76, 130.31, 126.67]],
                                  [[198.63, 181.44, 167.48, 156.43, 147.43, 142.29, 132.77, 124.91, 120.55, 117.7],
                                   [207.44, 193.37, 178.93, 169.51, 162.05, 155.12, 142.69, 132.12, 127.36, 122.91],
                                   [204.25, 190.32, 177.36, 168.36, 159.89, 152.37, 136.17, 128.82, 123.9, 120.95],
                                   [199.91, 183.73, 169.22, 157.96, 149.82, 142.42,132.68, 126.71, 122.74, 119.72]],
                                  [[194.21, 178.63, 165.49, 155.71, 146.75, 141.17, 128.56, 122.94, 118.45, 115.98],
                                   [200.15, 186.73, 173.1, 165.07, 157.69, 150.67, 134.39, 126.53, 121.82, 118.17],
                                   [200.98, 187.73, 174.72, 166.5, 158.29, 149.19, 133.77, 127.04, 122.83, 120.27],
                                   [194.75, 178.6, 165.17, 154.42, 146.04, 137.9, 126.33, 121.71, 118.9, 116.78]],
                                  [[235.42, 209.47, 193.12, 180.25, 170.59, 164.81, 157.39, 146.23, 141.58, 137.3],
                                   [256.55, 229.04, 210.57, 200.49, 190.91, 182.96, 172.46, 157.83, 150.65, 145.05],
                                   [255.21, 228.32, 210.86, 199.17, 187.66, 178.82, 165.13, 153.2, 146.53, 142.18],
                                   [252.22, 222.76, 202.13, 186.93, 176.45, 167.12, 158.48, 148.97, 143.47, 138.93]],
                                  [[223.78, 203.88, 187.34, 174.73, 164.34, 158.39, 147.87, 138.97, 133.8, 130.44],
                                   [231.73, 214.26, 197.53, 186.55, 178.11, 170.31, 156.23, 143.9, 138.6, 133.64],
                                   [231.87, 215.32, 199.62, 189.11, 179.42, 170.51, 155.22, 146.3, 140.46, 137.21],
                                   [227.05, 207.57, 189.86, 176.77, 167.36, 158.5, 146.56, 139.75, 135.37, 132.05]],
                                  [[201.36, 183.27, 170.56, 161.76, 153.25, 147.87, 136.46, 130.74, 126.69, 124.05],
                                   [211.29, 193.93, 181.1, 174.0, 167.57, 161.24, 147.34, 139.9, 136.36, 133.1],
                                   [209.66, 192.95, 180.69, 173.49, 166.58, 159.07, 144.85, 138.07, 134.69, 132.4],
                                   [207.28, 187.32, 174.3, 164.35, 156.75, 149.12, 139.08, 133.8, 131.19, 128.35]]])
    sample_time_map = np.array([0, 0.54, 0.97, 1.48, 2.02, 2.53, 3.01, 3.44, 3.98, 4.49])
    cooling_rates = get_cooling_rates(sample_temp_hists, sample_time_map)
    for i, exp in enumerate(cooling_rates):
        plt.plot([i]*len(exp), exp, 'o')
    plt.show()
