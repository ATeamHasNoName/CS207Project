import abc
class TimeSeriesInterface(abc.ABC):
    """
    This is the interface for the Time Series. The clients for this interface will be sub-interfaces
    SizedContainerTimeSeriesInterface and StreamTimeSeriesInterface.
    """
    @abc.abstractmethod
    def __iter__(self):
        """
        iterates over the values of the TimeSeries.
        """
        
    @abc.abstractmethod
    def itertimes(self):
        """
        iterates over the times of the TimeSeries. If there are no times provided, this iteration will
        return None.
        """
        
    @abc.abstractmethod
    def itervalues(self):
        """
        iterates over the values of the TimeSeries. This is identical to the default __iter__.
        """
        
    @abc.abstractmethod
    def iteritems(self):
        """
        iterates over the (time, value) tuple of the TimeSeries. If there are no times provided, this will 
        iterate over the (index, value) tuple of the TimeSeries, where index is the index of the value in the 
        underlying data structure.
        """