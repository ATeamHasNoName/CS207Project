class ArrayTimeSeries(TimeSeries):
    '''
    Numpy array implementation of time series, extended from TimeSeries
    
    RepInv: Times and values must only include numbers, and must be same length.
    '''
    def __init__(self, times, values):
        '''
        Extends from TimeSeries to represent data internally with a numpy array.
        
        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> z = TimeSeries(t,v)
        >>> z[3]
        1.5
        '''
        TimeSeries.__init__(self, values, times)
        # Represent data now as numpy array
        self.__timesseq = np.array(times, dtype=float)
        self.__valuesseq = np.array(values, dtype=float)
        self.__times_to_index = {t: i for i, t in enumerate(times)}

    # Override
    @property
    def timesseq(self):
        '''
        Time series index
        '''
        return self.__timesseq

    # Override
    @property
    def valuesseq(self):
        '''
        Time serires value
        '''
        return self.__valuesseq

    # Override
    @property
    def times_to_index(self):
        '''
        map time index with integer index of the array
        Priviate property - can't be called directly
        '''
        return self.__times_to_index