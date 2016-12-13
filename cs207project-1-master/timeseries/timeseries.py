import numbers
import statistics
import numpy as np
from lazy import LazyOperation
from lazy import lazy
from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface



class TimeSeries(SizedContainerTimeSeriesInterface):
    """
    A class that stores a single, ordered set of numerical data.

    Parameters
    ----------
    values : list
        This can be any object that can be treated like a sequence. Mandatory.
    times : list
        This can be any object that can be treated like a sequence. Optional.
        If it is not supplied, equally spaced integers are used instead.
    position: int
        The index position at which the requested item should be inserted

    Notes
    -----
    PRE: `values` is sorted in non-decreasing order

    WARNINGS:
    - Does not maintain an accurate time series if `input data` is unsorted.
    """

    def __init__(self, values, times=None):
        """
        The TimeSeries class constructor. It must be provided the initial data
        to fill the time series instance with.

        Parameters
        ----------
        values : sequence-like
            Actual data points for TimeSeries.
            Any user-provided sequence-like object. Mandatory.
        times : sequence-like
            Time values for TimeSeries. Optional.
            If None, equally spaced integers are used instead.

        Notes
        -----
        PRE: If times is not provided, `values` must be sorted

        WARNINGS: inital data and times must be sequences.

        Examples:
        ---------
        >>> ts = TimeSeries(times= [1,2,3], values= [100,200,300])

        """
        # First confirm `inital_data` is a sequence.
        # J: all Python sequences implement __iter__(), which we can use here.

        self.__class__.is_sequence(values)
        self._values = list(values)

        if times:
            self.__class__.is_sequence(times)
            self._times = list(times)

        else:
            self._times = list(range(len(self._values)))

        if len(self._times) != len(self._values):
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self._times) != len(set(self._times)):
            raise ValueError("Time data should contain no repeats")

    def __len__(self):
        """
        Method used to determine the length of the TimeSeries

        Returns:
        --------
        length : int
            The length of the ATimeSeries based on the ._values field.
        """
        return len(self._values)


    def __neg__(self):
        """
            Used to return a time series instance with each value being negative of the original. The times are left untouched.

            Returns:
            -------
                self : an instance of self with negated values but no change to the times
        """
        return self.__class__((-x for x in self._values), self._times)

    def __pos__(self):
        """
            Used to return a time series instance with each value's sign preserved

            Returns:
            -------
                self : an instance of self with each value's sign preserved
        """
        return self.__class__((x for x in self._values), self._times)

    def __add__(self, rhs):
        """
            The rhs argument will be added to each element of the time series if it is an instance of numbers.Real.
            If the rhs argument is an instance of TimeSeries, it will do the add element-wise. 

            Parameters:
            -----------
            rhs : instance of SizedContainerTimeSeriesInterface
                used to perform the add on the TimeSeries represented by self

            Raises:
            -------
                TypeError : if an attempt to add a list or np.ndarray instance to the TimeSeries is made

        """
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot add a numpy array to a TimeSeries!"
            if isinstance(rhs, list):
                raise "Cannot add a list to a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                # R: may be worth testing time domains are preserved correctly
                return self.__class__(values=(a + rhs for a in self), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                # R: test me. should fail when the time domains are non congruent
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return self.__class__(values=(a + b for a, b in pairs), times=self._times)
        except TypeError:
            raise NotImplemented # R: test me. should fail when we try to add a numpy array or list

    def __sub__(self, rhs):
        """
            The rhs argument will be subtracted from each element of the time series if it is an instance of numbers.Real.
            If the rhs argument is an instance of TimeSeries, it will do the subtraction element-wise.

            Parameters:
            -----------
            rhs : instance of SizedContainerTimeSeriesInterface
                used to perform the sub on the TimeSeries represented by self

            Raises:
            -------
                TypeError : if an attempt to sub from a list or np.ndarray instance to the TimeSeries is made

        """
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot sub a numpy array from a TimeSeries!"
            if isinstance(rhs, list):
                raise "Cannot sub a list from a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__((a - rhs for a in self), self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return self.__class__((a - b for a, b in pairs), self._times)
        except TypeError:
            raise NotImplemented


    def __mul__(self, rhs):
        """
            The rhs argument will be multiplied with each element of the time series if it is an instance of numbers.Real.
            If the rhs argument is an instance of TimeSeries, it will do the multiplication element-wise.

            Parameters:
            -----------
            rhs : instance of SizedContainerTimeSeriesInterface
                used to perform the multiplication on the TimeSeries represented by self

            Raises:
            -------
                TypeError : if an attempt to multiply with a list or np.ndarray instance to the TimeSeries is made

        """
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot mul a numpy array with a TimeSeries!"
            if isinstance(rhs, list):
                raise "Cannot mul a list with a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return TimeSeries((a * rhs for a in self), self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return TimeSeries((a * b for a, b in pairs), self._times)
        except TypeError:
            raise NotImplemented


    def __eq__(self, rhs):
        """
        Method used to test if two SizedContainerTimeSeriesInterface instances have the same times and values

        Parameters:
        -----------
        rhs : instance of SizedContainerTimeSeriesInterface
            rhs will be compared to the time series sequence represented by self

        Raises:
        -------
        TypeError : if rhs is a np.ndarray type

        WARNINGS:
            - if rhs is a list, TypeError is thrown
            - np.array_equal compares both elements and dimensions.
        """
        # R: leverages self._values is a list. Will have to change when we relax this.
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot compare numpy array to TimeSeries!"
            self._check_length_helper(self, rhs)
            self._check_time_domains_helper(self, rhs)
            return self._values==rhs._values
        except TypeError:
            raise NotImplemented

    @lazy
    def identity(self):
        """
            An identity function with one argument that just returns the argument - self is the only argument

            Returns
            -------
            self : the instance to identify
        """
        return self

    @property
    def lazy(self):
        """
            A lazy property method that returns a new LazyOperation instance using the TimeSeries.identity() method

            Returns
            -------
            self.identity() : an instance of LazyOperation
        """
        return self.identity()

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
        return statistics.mean(self._values)

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
        return statistics.stdev(self._values)
