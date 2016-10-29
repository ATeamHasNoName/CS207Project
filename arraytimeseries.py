class ArrayTimeSeries(TimeSeries):
    '''
    AbsFun: two numpy arrays, one for times and one for values represent the sized container time series. 
    The list of times is optional and if it is not provided, times are treated as the indexes of the values 
    list. There cannot be duplicate times as there should only be one value recorded at each time.
    
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
    
    # Override
    def items(self):
        '''
        Returns numpy array of (time, value) tuples.
        If time is not provided, returns numpy array of (index, value) tuples.
        Parameters
        ----------
        None
        Returns
        -------
        Numpy array of tuples of (time, value)
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a.items()
        [(1.0, 0.0), (1.5, 2.0), (2.0, -1.0), (2.5, 0.5), (10.0, 0.0)]
        '''
        self.repOK(self.timesseq, self.valuesseq)
        return np.asarray(list(zip(self.timesseq, self.valuesseq)))
    