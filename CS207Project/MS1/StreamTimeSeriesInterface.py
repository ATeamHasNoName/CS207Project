import abc
from TimeSeriesInterface import TimeSeriesInterface
# from MS1.TimeSeriesInterface import TimeSeriesInterface
class StreamTimeSeriesInterface(TimeSeriesInterface):
	"""
	This is the interface for Stream time interface. 
	"""
	@abc.abstractmethod
	def produce(self,chunk=1):
		"""
		produce method allows us to create the time series using a generator function by adding a chunk of new data.
		The chunk functionality ensures that we can use it for more than one data point at a time.
		"""


