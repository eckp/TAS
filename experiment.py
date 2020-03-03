class Experiment():

    def __init__(self, time, tow1, tow2, tow3, tow4, tow5, tow6, tow7, tow8):
        '''
        Experiment class used to store and process data for each experiment.

        Attributes:
            numpy.array(float64) time -> time in seconds since the beginning of the experiment
            numpy.array(float64) tow1 -> temperature data of tow 1 in degrees Celsius
            numpy.array(float64) tow2 -> temperature data of tow 2 in degrees Celsius
            numpy.array(float64) tow3 -> temperature data of tow 3 in degrees Celsius
            numpy.array(float64) tow4 -> temperature data of tow 4 in degrees Celsius
            numpy.array(float64) tow5 -> temperature data of tow 5 in degrees Celsius
            numpy.array(float64) tow6 -> temperature data of tow 6 in degrees Celsius
            numpy.array(float64) tow7 -> temperature data of tow 7 in degrees Celsius
            numpy.array(float64) tow8 -> temperature data of tow 8 in degrees Celsius
        ''' 

        self.time = time
        self.tow1 = tow1
        self.tow2 = tow2
        self.tow3 = tow3
        self.tow4 = tow4
        self.tow5 = tow5
        self.tow6 = tow6
        self.tow7 = tow7
        self.tow8 = tow8

