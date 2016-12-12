# Implements the TimeSeriesInterface ABC

import abc

class TimeSeriesInterface(abc.ABC):
    """
    Interface for TimeSeries

    """

    ##############################################################################
    ## GLOBAL CONSTANT FOR ALL TIMESERIES
    ##############################################################################
    MAX_LENGTH = 10

    ##############################################################################
    ## ABSTRACT METHODS TO BE IMPLEMENTED BY ALL TIMESERIES OF FIXED LENGTH
    ##############################################################################

    @abc.abstractmethod
    def __iter__(self):
        """
        Description
        -----------
        Fixed size or not, each TimeSeries needs to support iteration.
        """

    @abc.abstractmethod
    def __neg__(self):
        """
        Description
        -----------
        All TimeSeries, fixed or not, should support unary `-` operator
        """

    @abc.abstractmethod
    def __pos__(self):
        """
        Description
        -----------
        Obviously all TimeSeries need to suppport opposite of __neg__ as well.
        """


    # J: I'm assuming these methods can be implemented lazily,
    # so including them at the top of the hierarchy...

    @abc.abstractmethod
    def __add__(self, rhs):
        """
        Description
        -----------
        All TimeSeries should support adding a constant to each element
        """

    @abc.abstractmethod
    def __radd__(self, other):
        """
        Description
        -----------
        All TimeSeries should support adding a constant to each element
        """

    @abc.abstractmethod
    def __sub__(self, rhs):
        """
        Description
        -----------
        All TimeSeries should support subtracting a constant from each element
        """

    @abc.abstractmethod
    def __rsub__(self, other):
        """
        """

    @abc.abstractmethod
    def __mul__(self, rhs):
        """
        Description
        -----------
        All TimeSeries must support multiplication by a constant
        """


    @abc.abstractmethod
    def __rmul__(self):
        """
        """

    @abc.abstractmethod
    def mean(self, chunk = None):
        """
        Description
        -----------
        All TimeSeries should support the ability to calculate the mean of values present in an instance.

        Parameters
        ----------
        chunk : int
            Can be used for subclass instances with no storage. Represents the size of the values within a TimeSeries instance.
        """


    @abc.abstractmethod
    def std(self, chunk = None):
        """
        Description
        -----------
        All TimeSeries should support the ability to calculate the standard deviation of values present in an instance.

        Parameters
        ----------
        chunk : int
            Can be used for subclass instances with no storage. Represents the size of the values within a TimeSeries instance.
        """
