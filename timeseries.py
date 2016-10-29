import itertools
import reprlib
import numpy as np

class TimeSeries(SizedContainerTimeSeriesInterface):
    '''
    AbsFun: two lists, one for times and one for values represent the sized container time series. 
    The list of times is optional and if it is not provided, times are treated as the indexes of the values 
    list. There cannot be duplicate times as there should only be one value recorded at each time.
    
    RepInv: Times and values must only include numbers, and must be same length, if times is included. There 
    cannot be duplicate times.
    '''
    def __init__(self, values, times=None):
        self.repOK(times, values)
        
        # Sort times and values in ascending order of time - It's just neater that way
        if times is not None:
            self.__isTimeNone = False
            times, values = (list(x) for x in zip(*sorted(zip(times, values), key=lambda pair: pair[0])))
            self.__timesseq = list(times)
            self.__valuesseq = list(values)
            self.__times_to_index = {t: i for i, t in enumerate(times)}
        else:
            self.__isTimeNone = True
            self.__timesseq = None
            self.__valuesseq = list(values)
            self.__times_to_index = None
        
    def repOK(self, times, values):
        if times is None:
            assert self._hasOnlyNumbers(values), "Values should only include numbers"
        else:
            assert self._hasOnlyNumbers(times) and self._hasOnlyNumbers(values), "Both times and values should only include numbers"
            assert len(times) == len(values), "Length of times and values must be the same"
            assert len(times) == len(set(times)), "Times cannot be duplicated, i.e. there can only be one unique value for each time"
    
    def _hasOnlyNumbers(self, arr):
        '''
        Private function to test if the input array consists of only numbers
        '''
        for i in arr:
            try:
                int(i)
            except ValueError:
                return False
        return True
        
    @property
    def timesseq(self):
        '''
        Time series index
        Private property - can't be called directly
        '''
        return self.__timesseq

    @property
    def valuesseq(self):
        '''
        Time serires value
        Private property - can't be called directly
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
        Returns the times sequence, or None if there are no times provided in the Constructor.
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
        If time is not provided, returns sequence of (index, value) tuples.
        Parameters
        ----------
        None
        Returns
        -------
        List of tuples of (time, value)
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = TimeSeries(t, v)
        >>> a.items()
        [(1.0, 0.0), (1.5, 2.0), (2.0, -1.0), (2.5, 0.5), (10.0, 0.0)]
        '''
        self.repOK(self.timesseq, self.valuesseq)
        if self.__isTimeNone:
            return [(i, x) for i, x in enumerate(self.valuesseq)]
        else:
            return list(zip(self.timesseq, self.valuesseq))
    
    def __len__(self):
        '''
        Returns length of the sequence. This length is specifically the length of the values.
        
        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> a = TimeSeries(t, v)
        >>> len(a)
        5
        >>> len(TimeSeries([], []))
        0
        '''
        self.repOK(self.timesseq, self.valuesseq)
        return len(self.valuesseq)

    def __getitem__(self, time):
        '''
        Returns the value at the specified time. If times are not initialized in constructor, then this 
        time input will serve as the index in the values array. If item is not found, raise an IndexError.
        
        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> a = TimeSeries(t, v)
        >>> a[2.5]
        0
        '''
        self.repOK(self.timesseq, self.valuesseq)
        
        if self.__isTimeNone:
            if time > len(self):
                raise IndexError('Time does not exist.')
            return self.valuesseq[time]
        else:
            if time not in self.times_to_index:     
                raise IndexError('Time does not exist.')
            return self.valuesseq[self.times_to_index[float(time)]]

    def __setitem__(self, time, value):
        '''
        Changes the value at specified time to input value. 
        This does not allow us to extend the sequence. It only modifies an existing time's value.
        If times are not initialized in constructor, then this time input will serve as the index in 
        the values array. If item is not found, raise an IndexError.
        
        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> a = TimeSeries(t, v)
        >>> a[1] = 12.0
        >>> a[1]
        12.0
        >>> a[5] = 9.0
        >>> a[5]
        9.0
        '''
        indexToInsert = -1
        if self.__isTimeNone:
            if time > len(self):
                raise IndexError('Time does not exist.')
            else:
                indexToInsert = time
        else:
            if time not in self.times_to_index:     
                raise IndexError('Time does not exist.')
            else:
                indexToInsert = self.times_to_index[time]
        if indexToInsert == -1:
            raise ValueError('Error occured while setting item.')
        self.valuesseq[indexToInsert] = value
        self.repOK(self.timesseq, self.valuesseq)
        
    def __iter__(self):
        '''
        Iterates over values.
        
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
        self.repOK(self.timesseq, self.valuesseq)
        for v in self.valuesseq:
            yield v

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
        self.repOK(self.timesseq, self.valuesseq)
        if self.__isTimeNone:
            yield None
        else:
            for t in self.timesseq:
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
        self.repOK(self.timesseq, self.valuesseq)
        for v in self.valuesseq:
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
        self.repOK(self.timesseq, self.valuesseq)
        dictOfItems = {}
        if self.__isTimeNone:
            dictOfItems = [(i, x) for i, x in enumerate(self.valuesseq)]
        else:
            dictOfItems = zip(self.timesseq, self.valuesseq)
        for t, v in dictOfItems:
            yield t, v

    def __repr__(self):
        '''
        Only returns values without times.
        If more than 100 values, the output will be truncated with ellipses.
        '''
        class_name = type(self).__name__
        myrepr = reprlib.aRepr
        myrepr.maxlist = 100 # More than 100 then replace with ellipses
        components = myrepr.repr(self.valuesseq)
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)   
    
    def __str__(self):
        '''
        Only returns values without times.
        Shows the length of the time series, and first and last values.
        '''
        class_name = type(self).__name__
        first = 'N/A'
        last = 'N/A'
        if len(self) > 0:
            first = str(self.valuesseq[0])
            last = str(self.valuesseq[-1])
        return '%s\nLength: %d\nFirst (oldest): %s, Last (newest): %s' % (class_name, len(self), first, last)