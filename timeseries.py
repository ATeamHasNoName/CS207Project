import itertools
import reprlib

class TimeSeries:
    
    def __init__(self, times, values):
        
        '''

        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> z = TimeSeries(t,v)
        >>> z[3]
        1.5

        '''

        #numpy - provide a length of the sequence
        times = np.array(times, dtype=float)
        values = np.array(values, dtype=float)

        #sort ties in ascending order
        sort_order = np.argsort(times)
        times = times[sort_order]
        values = values[sort_order]

        #create private propterty
        self.__timesseq = np.array(times)
        self.__valuesseq = np.array(values)
        self.__times_to_index = {t: i for i, t in enumerate(times)}

    @ propterty
    def timesseq(self):
        '''
        Time serires index
        Priviate property - can't be called directly
        '''
        return self.__timesseq


    @ propterty
    def valuesseq(self):
        '''
        Time serires value
        Priviate property - can't be called directly
        '''
        return self.__valuesseq

    @property
    def times_to_index(self):
        '''
        map time index with integer index of the array
        Priviate property - can't be called directly
        '''
        return self.__times_to_index



    def times(self):
        '''
        Returns the times sequence.
        Parameters
        ----------
        None
        Returns
        -------
        Numpy array
            Time series times
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a.times()
        array([  1. ,   1.5,   2. ,   2.5,  10. ])
        '''
        return self.timesseq

    def values(self):
        '''
        Returns the values sequence.
        Parameters
        ----------
        None
        Returns
        -------
        Numpy array
            Time series values
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a.values()
        array([ 0. ,  2. , -1. ,  0.5,  0. ])
        '''
        return self.valuesseq

    def items(self):
        '''
        Returns sequence of (time, value) tuples.
        Parameters
        ----------
        None
        Returns
        -------
        Numpy array of tuples
            Time series time-value pairs
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a.items()
        [(1.0, 0.0), (1.5, 2.0), (2.0, -1.0), (2.5, 0.5), (10.0, 0.0)]
        '''
        return [(time, self[time]) for time in self.__timesseq]



    def __len__(self):

        '''
        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> a = TimeSeries(t, v)
        >>> len(a)
        5
        >>> len(TimeSeries([], []))
        0
        '''
        return len(self.timesseq)


    def __getitem__(self, time):
        '''
        Takes key as input and returns corresponding item in sequence.
        Parameters
        ----------
        time : int or float
            A potential time series time
        Returns
        -------
        float
            Time series value associated with the given time
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a[2.5]
        0.5
        '''
        try:
            return self.__valuesseq[self.times_to_index[float(time)]]
        except KeyError:  # not present
            raise KeyError(str(time) + ' is not present in the TimeSeries.')


    def __setitem__(self, time, value):
        '''
        
        ----------
        time : int or float
            A time series time
        value : int or float
            A time series value
        Returns
        -------
        Modified in-place
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a[1] = 12.0
        >>> a[1]
        12.0
        >>> a[5] = 9.0
        >>> a[5]
        9.0
        '''
        try:
            self.__valuesseq[self.times_to_index[float(time)]] = float(value)
        except KeyError:  # not present
            times = list(self.timesseq) + [time]
            values = list(self.valuesseq) + [value]
            self.__init__(times, values)



    def __str__(self):
       '''
       Printable representation of sequence

        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> a = TimeSeries(t, v)  # less than 6
        >>> str(a)
        'Time Series Length: 5 [1.0, 3.0, 0.0, 1.5, 1.0]'
        >>> t = [1.5, 2, 2.5, 3, 10.5, 13, 16]
        >>> v = [1, 3, 0, 1.5, 1, 2, 9]
        >>> a = TimeSeries(t, v)  # longer than 6
        >>> str(a)
        'Length: 7 [1.0, 3.0, ..., 9.0]'
       '''
       
        n = len(self)
        if n > 6:
            return('Time Series Length: {} [{},{},...,{}]'.format(
            n, self[self.__timesseq[0]], self[self.__timesseq[1]], self[self.__timesseq[-1]]))
        else:
            list_time = ', '.join([v for v in self])
            return('Time Series Length: {} [{}]'.format(n, list_time))





    def __repr__(self):
        class_name = type(self).__name__
        myrepr = reprlib.aRepr
        myrepr.maxlist = 100 # More than 100 then replace with ellipses
        components = myrepr.repr(self._timeseries)
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)   



    def __contains__(self, time):
        '''
        Takes a time and returns true if it is in the times array.
        Parameters
        ----------
        time : int or float
            A time series time
        Returns
        -------
        bool
            Whether the time is present in the time series
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> 1 in a
        True
        >>> 3 in a
        False
        '''
        return float(time) in self.times_to_index.keys()
    


    def __iter__(self):
        '''
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> for val in a:
        ...     print(val)
        0.0
        2.0
        -1.0
        0.5
        0.0
        '''
        for v in self.__valuesseq:
            return v


     def itertimes(self):
        '''
        Iterates over the times array.
        Parameters
        ----------
        None
        Returns
        -------
        float(s)
            Iterator of time series times
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> for val in a.itertimes():
        ...     print(val)
        1.0
        1.5
        2.0
        2.5
        10.0
        '''
        for t in self.__timesseq:
            yield t

    def itervalues(self):
        '''
        Iterates over the values array.
        Parameters
        ----------
        None
        Returns
        -------
        float(s)
            Iterator of time series values
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> for val in a.itervalues():
        ...     print(val)
        0.0
        2.0
        -1.0
        0.5
        0.0
        '''
        for v in self.__valuesseq:
            yield v

    def iteritems(self):
        '''
        Iterates over the time-values pairs.
        Parameters
        ----------
        None
        Returns
        -------
        tuple(s) of floats
            Iterator of time series time-value pairs
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> for val in a.iteritems():
        ...     print(val)
        (1.0, 0.0)
        (1.5, 2.0)
        (2.0, -1.0)
        (2.5, 0.5)
        (10.0, 0.0)
        '''
        for t, v in zip(self.__timesseq, self.__valuesseq):
            yield t, v





