import abc
from TimeSeriesInterface import TimeSeriesInterface

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
    """
    This is the interface for container based Time Series. This extends from the more general 
    TimeSeriesInterface. The clients for this interface are the classes TimeSeries and ArrayTimeSeries.
    """
    @abc.abstractmethod
    def times(self):
        '''
        Returns the times sequence, or None if there are no times provided.
        '''
        
    @abc.abstractmethod
    def values(self):
        '''
        Returns the values sequence.
        '''
        
    @abc.abstractmethod
    def items(self):
        '''
        Returns sequence of (time, value) tuples.
        If time is not provided, returns sequence of (index, value) tuples.
        '''
        
    @abc.abstractmethod
    def __len__(self):
        '''
        Returns length of the sequence. This length is specifically the length of the values.
        '''
        
    @abc.abstractmethod
    def __getitem__(self, time):
        '''
        Returns the value at the specified time. If times are not initialized in constructor, then this 
        time input will serve as the index in the values array. If item is not found, raise an IndexError.
        '''
        
    @abc.abstractmethod
    def __setitem__(self, time, value):
        '''
        Changes the value at specified time to input value. 
        This does not allow us to extend the sequence. It only modifies an existing time's value.
        If times are not initialized in constructor, then this time input will serve as the index in 
        the values array. If item is not found, raise an IndexError.
        '''