class Experiment():

    def __init__(self, time, **kwargs):
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

            If the class is used to store data from the rear camera,
            the tow variables become multidimensional arrays holding
            the temperature history of each line as a sub-array.

        version date: 07.03.2020
        '''
        
        self.time = time
        self.tow1 = kwargs.get('tow1')
        self.tow2 = kwargs.get('tow2')
        self.tow3 = kwargs.get('tow3')
        self.tow4 = kwargs.get('tow4')
        self.tow5 = kwargs.get('tow5')
        self.tow6 = kwargs.get('tow6')
        self.tow7 = kwargs.get('tow7')
        self.tow8 = kwargs.get('tow8')
            
