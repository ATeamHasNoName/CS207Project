from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
import numpy as np
import numbers

class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """
    A subclass that stores two arrays internally, an ordered set
    of numerical data and its time points contiguously as two of `np.array`.

    Attributes:
    ----------
        _values : sequence-like
            Actual data points for ArrayTimeSeries.
            Any user-provided sequence-like object. Mandatory.
        _times : sequence-like
            Time values for ArrayTimeSeries. Mandatory

    Notes
    -----
        PRE: 
         - `values` is sorted in non-decreasing order
         - _times are mandatory elements that must represent a montonic sequence.

    INVARIANTS: inital_data and times must be sequences.

    WARNINGS: 
        - User must provide times and values.
        - Does not maintain an accurate time series if `input data` is unsorted.

    """
    def __init__(self, times, values):
        """
        Parameters:
        ----------
            values : sequence-like
                Actual data points for ArrayTimeSeries.
                Any user-provided sequence-like object. Mandatory.
            times : sequence-like
                Time values for ArrayTimeSeries. Mandatory

        Notes
        -----
            PRE: _times are mandatory elements that must represent a montonic sequence.

        Examples:
        ---------
        >>> ts = ArrayTimeSeries(times= [1,2,3], values= [100,200,300])
        """
        # J: breaking DRY and adding sequenceness checks here, since
        # we don't inherit from TimeSeries anymore and
        # since the upper levels of the inheritance hierarchy
        # are (mostly) abstract things...
        self.__class__.is_sequence(times)
        self.__class__.is_sequence(values)
        self._times = np.array(list(times))
        self._values = np.array(list(values))

        if len(self._times) != len(self._values):
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self._times) != len(set(self._times)):
            raise ValueError("Time data should contain no repeats")

    def __len__(self):
        """
        Method used to determine the length of the ArrayTimeSeries

        Returns:
        --------
        length : int
            The length of the ArrayTimeSeries based on the ._values field.

        WARNINGS: len of np.appry returns and error for arrays of size 1.
        """
        return len(np.atleast_1d(self._values))


    #### ABSTRACT FNS BELOW; REMOVE THIS LATER ######

    def __eq__(self, rhs):
        """
        Method used to test if two SizedContainerTimeSeriesInterface instances have the same times and values

        Parameters:
        -----------
        rhs : instance of SizedContainerTimeSeriesInterface
            rhs will be compared to the time series sequence represented by self

        Raises:
        -------
        TypeError : if rhs is a list

        WARNINGS:
            - if rhs is a list, TypeError is thrown
            - np.array_equal compares both elements and dimensions.
        """
        try:
            if isinstance(rhs, list):
                raise "Cannot compare list to ArrayTimeSeries!"
            self.__class__._check_time_domains_helper(self, rhs)
            return (np.array_equal(self._values,rhs._values) and np.array_equal(self._times,rhs._times))

        except TypeError:
            raise NotImplemented


    def __add__ (self,rhs):
        """
            The rhs argument will be added to each element of the time series if it is an instance of numbers.Real.
            If the rhs argument is an instance of ArrayTimeSeries, it will do the add element-wise. 

            Parameters: 
            -----------
            rhs : instance of SizedContainerTimeSeriesInterface
                used to perform the add on the ArrayTimeSeries represented by self

            Raises:
            -------
                TypeError : if an attempt to add a list instance to the ArrayTimeSeries is made

        """
        # N: Note – currently, we’re adding the value arrays if everything is the same length.
        # N: But it would be possible to have to time series that were the same length but which
        # N: covered different times. Should we address this as well?
        try:
            if isinstance(rhs, list):
                raise "Cannot add a list to a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__(values=(self._values + rhs), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                return self.__class__(values=self._values + rhs._values, times=self._times)
        except TypeError:
            raise NotImplemented

    def __sub__(self, rhs):
        """
            The rhs argument will be subtracted from each element of the time series if it is an instance of numbers.Real.
            If the rhs argument is an instance of ArrayTimeSeries, it will do the subtraction element-wise.

            Parameters:
            -----------
            rhs : instance of SizedContainerTimeSeriesInterface
                used to perform the sub on the ArrayTimeSeries represented by self

            Raises:
            -------
                TypeError : if an attempt to sub from a list instance to the ArrayTimeSeries is made

        """
        try:
            if isinstance(rhs, list):
                raise "Cannot sub a list from a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__(values=(self._values - rhs), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                return self.__class__(values=self._values - rhs._values, times=self._times)
        except TypeError:
            raise NotImplemented

    def __mul__(self, rhs):
        """
            The rhs argument will be multiplied with each element of the time series if it is an instance of numbers.Real.
            If the rhs argument is an instance of ArrayTimeSeries, it will do the multiplication element-wise.

            Parameters:
            -----------
            rhs : instance of SizedContainerTimeSeriesInterface
                used to perform the multiplication on the ArrayTimeSeries represented by self

            Raises:
            -------
                TypeError : if an attempt to multiply with a list instance to the ArrayTimeSeries is made

        """
        try:
            if isinstance(rhs, list):
                raise "Cannot mul a list with a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__(values=(self._values * rhs), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return self.__class__(values=self._values * rhs._values, times=self._times)
        except TypeError:
            raise NotImplemented

    def __neg__(self):
        """
            Used to return a time series instance with each value being negative of the original. The times are left untouched.

            Returns:
            -------
                self : an instance of self with negated values but no change to the times
        """
        return self.__class__(values=((-1)*self._values), times=self._times)

    def __pos__(self):
        """
            Used to return a time series instance with each value's sign preserved

            Returns:
            -------
                self : an instance of self with each value's sign preserved
        """
        return self.__class__(values=self._values, times=self._times)

    def mean(self, chunk = None):
        """
        Method used to calculate the mean of the time series. 

        Parameters:
        -----------
        chunk = an optional subset of the time series to do the calculation on 

        Returns: 
        --------
        np.mean : the mean of the time series
        """
        return np.mean(self._values)

    def std(self, chunk = None):
        """
        Method used to calculate the standard deviation of the time series. 

        Parameters:
        -----------
        chunk = an optional subset of the time series to do the calculation on

        Returns:
        --------
        np.std : the standard deviation of the time series 
        """
        return np.std(self._values, ddof=1)
