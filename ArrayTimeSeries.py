import numpy as np
import numbers
from TimeSeries import TimeSeries

class ArrayTimeSeries(TimeSeries):
    """
    AbsFun: two numpy arrays, one for times and one for values represent the sized container time series. 
    The list of times is optional and if it is not provided, times are treated as the indexes of the values 
    list. There cannot be duplicate times as there should only be one value recorded at each time.
    
    RepInv: Times and values must only include numbers, and must be same length.
    """
    def __init__(self, times, values):
        """
        Extends from TimeSeries to represent data internally with a numpy array.
        NOTE: The times and values arguments are flipped order from the superclass TimeSeries.
        
        >>> t = [1.5, 2, 2.5, 3, 10.5]
        >>> v = [1, 3, 0, 1.5, 1]
        >>> z = ArrayTimeSeries(t, v)
        >>> z[3]
        1.5
        """
        TimeSeries.__init__(self, values=values, times=times)
        times, values = (list(x) for x in zip(*sorted(zip(times, values), key=lambda pair: pair[0])))
        # Represent data now as numpy array
        self.__timesseq = np.array(times, dtype=float)
        self.__valuesseq = np.array(values, dtype=float)
        self.__times_to_index = {t: i for i, t in enumerate(times)}

    # Override
    @property
    def timesseq(self):
        """
        Returns numpy array of times
        """
        return self.__timesseq

    # Override
    @property
    def valuesseq(self):
        """
        Returns numpy array of values
        """
        return self.__valuesseq

    # Override
    @property
    def times_to_index(self):
        """
        map time index with integer index of the array
        Private property - can't be called directly
        """
        return self.__times_to_index
    
    # Override to return items as a numpy array, as times and values are already returned as numpy arrays
    def items(self):
        """
        Returns sequence of (time, value) tuples.
        If time is not provided, returns sequence of (index, value) tuples.
        Override to return numpy array instead of list.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        numpy array of (time, val) tuples.
        
        >>> t = [1, 1.5, 2, 2.5, 10]
        >>> v = [0, 2, -1, 0.5, 0]
        >>> a = ArrayTimeSeries(t, v)
        >>> a.items()
        array([[  1. ,   0. ],
               [  1.5,   2. ],
               [  2. ,  -1. ],
               [  2.5,   0.5],
               [ 10. ,   0. ]])
        """
        self.repOK(self.timesseq, self.valuesseq)
        return np.asarray(list(zip(self.timesseq, self.valuesseq)))
    
    # Override to return an ArrayTimeSeries
    def __add__(self, other):
        """
        Adds the values of the two TimeSeries and returns a new ArrayTimeSeries.
    
        Parameters
        ----------
        other: Another TimeSeries/ArrayTimeSeries object

        Returns
        -------
        A new ArrayTimeSeries with the summed values of the two provided TimeSeries.

        Notes
        -----
        PRE: 
            - The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
            
        >>> t = [3., 1., 2.]
        >>> v = [4., 5., 6.]
        >>> z = ArrayTimeSeries(t, v)
        >>> t2 = [3., 2., 1.]
        >>> v2 = [4., 6., 5.]
        >>> z2 = ArrayTimeSeries(t2, v2)
        >>> z2 + z
        ArrayTimeSeries([(1.0, 10.0), (2.0, 12.0), (3.0, 8.0)])
        """
        other_values, self_values, self_times = self._valuesSortedByTime(other)
        if isinstance(other, numbers.Real):
            return ArrayTimeSeries(self_times, [self_values[i] + other for i in range(0, len(self_values))])    
        return ArrayTimeSeries(self_times, [self_values[i] + other_values[i] for i in range(0, len(self_values))])
    
    # Override to return an ArrayTimeSeries
    def __sub__(self, other):
        """
        Subtract the values of the other TimeSeries fom self, and returns a new ArrayTimeSeries.
    
        Parameters
        ----------
        other: Another TimeSeries object

        Returns
        -------
        A new ArrayTimeSeries with subtracted values of other from self (self - other)

        Notes
        -----
        PRE: 
            - The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
            
        >>> t = [3., 1., 2.]
        >>> v = [4., 5., 6.]
        >>> z = ArrayTimeSeries(t, v)
        >>> t2 = [3., 2., 1.]
        >>> v2 = [4., 6., 5.]
        >>> z2 = ArrayTimeSeries(t2, v2)
        >>> z2 - z
        ArrayTimeSeries([(1.0, 0.0), (2.0, 0.0), (3.0, 0.0)])
        """
        other_values, self_values, self_times = self._valuesSortedByTime(other)
        if isinstance(other, numbers.Real):
            return ArrayTimeSeries(self_times, [self_values[i] - other for i in range(0, len(self_values))]) 
        return ArrayTimeSeries(self_times, [self_values[i] - other_values[i] for i in range(0, len(self_values))])
    
    # Override to return an ArrayTimeSeries
    def __mul__(self, other):
        """
        Multiplies the values of the two TimeSeries and returns a new ArrayTimeSeries.
    
        Parameters
        ----------
        other: Another TimeSeries object

        Returns
        -------
        A new ArrayTimeSeries with the multiplied values from both TimeSeries

        Notes
        -----
        PRE: 
            - The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
            
        >>> t = [3., 1., 2.]
        >>> v = [4., 5., 6.]
        >>> z = ArrayTimeSeries(t, v)
        >>> t2 = [3., 2., 1.]
        >>> v2 = [4., 6., 5.]
        >>> z2 = ArrayTimeSeries(t2, v2)
        >>> z2 * z
        ArrayTimeSeries([(1.0, 25.0), (2.0, 36.0), (3.0, 16.0)])
        """
        other_values, self_values, self_times = self._valuesSortedByTime(other)
        if isinstance(other, numbers.Real):
            return ArrayTimeSeries(self_times, [self_values[i] * other for i in range(0, len(self_values))]) 
        return ArrayTimeSeries(self_times, [self_values[i] * other_values[i] for i in range(0, len(self_values))])

    # Override to return ArrayTimeSeries
    def interpolate(self, tseq):
        """
        Returns a TimeSeries object containing the elements
        of a new sequence tseq and interpolated values in the TimeSeries.
        This method assume the times in timesseq are monotonically
        increasing; otherwise, results may not be as expected.
        Parameters
        ----------
        tseq : list of ints or floats
            Time series times to interpolate
        Returns
        -------
        TimeSeries
            Time series object with all the interpolated values for the
            given times.
        >>> a = TimeSeries([1, 2, 3],[0, 5, 10])
        >>> b = TimeSeries([100, -100],[2.5, 7.5])
        >>> a.interpolate([-100, 100])
        TimeSeries([(-100, 1), (100, 3)])
<<<<<<< HEAD
        """
=======
        '''
>>>>>>> fef514fa1e44a29aacb6603513ca3292b9620035
        valseq = [self._get_interpolated(t, self.timesseq) for t in tseq]
        return ArrayTimeSeries(times=tseq, values=valseq)
    