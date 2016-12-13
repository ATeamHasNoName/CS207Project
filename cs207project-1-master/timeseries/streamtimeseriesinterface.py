# Implements StreamTimeSeriesInterface ABC.

from timeseriesinterface import TimeSeriesInterface
import abc

class StreamTimeSeriesInterface(TimeSeriesInterface):
    """
    Abstract Base Class for streaming time series implementations.
    """

    # just making sure that these don't conflict with
    # the @abstractmethods in TimeSeriesInterface

    def __add__(self):
        """
        Description
        -----------
        All StreamingTimeSeries should support adding a constant to each element
        """

    def __iter__(self):
        """
        Description
        -----------
        Fixed size or not, each StreamingTimeSeries needs to support iteration.
        """

    def __mul__(self):
        """
        Description
        -----------
        All StreamingTimeSeries must support multiplication by a constant
        """
    def __neg__(self):
        """
        Description
        -----------
        All StreamingTimeSeries, fixed or not, should support unary `-` operator
        """
    def __pos__(self):
        """
        Description
        -----------
        Obviously all StreamingTimeSeries need to suppport opposite of __neg__ as well.
        """
    def __radd__(self):
        """
        Description
        -----------
        All StreamingTimeSeries should support adding a constant to each element
        """
    def __rmul__(self):
        """"""
    def __rsub__(self):
        """"""
    def __sub__(self):
        """
        Description
        -----------
        All StreamingTimeSeries should support subtracting a constant from each element
        """

    def std(self, chunk = None):
        """
        Description
        -----------
        All StreamingTimeSeries should support the ability to calculate the standard deviation of values present in an instance.

        Parameters
        ----------
        chunk : int
            Can be used for subclass instances with no storage. Represents the size of the values within a StreamingTimeSeries instance.
        """

    def mean(self, chunk = None):
        """
        Description
        -----------
        All StreamingTimeSeries should support the ability to calculate the mean of values present in an instance.

        Parameters
        ----------
        chunk : int
            Can be used for subclass instances with no storage. Represents the size of the values within a StreamingTimeSeries instance.
        """

    def produce(self, chunk=1):
        """
        Description
        -----------
        Produces `chunk` new values of the time series
        """

    def online_mean():
        """
        Description
        -----------
        Generates a stream of online means.
        """

    def online_std():
        """
        Description
        -----------
        Generates a stream of online standard deviations.
        """

    # need a way to represent these objects
    # def __repr__(self):
    #   pass

    # def __str__(self):
    #   pass