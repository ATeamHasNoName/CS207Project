from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from TimeSeries import TimeSeries
import numpy as np
import sys
sys.path.append('./DB/')
from WrappedDB import WrappedDB

class SMTimeSeries(SizedContainerTimeSeriesInterface):
	"""
	Storage Manager class that stores instances of Time Series.
	"""
	
	def __init__(self, values, times, key = None):
		"""
		Initializes a Storage Manager Time Series classwith value and times lists. Accepts an optional id which stores the Time Series into the Storage Manager. 
		
		Parameters
		----------
		times: the times of a timeseries 
		values: the values of a timeseries
		key: a key to store the TimeSeries in the database

		Returns
		-------
		None
	
		>>> smts = SMTimeSeries[1.5, 2, 2.5, 3, 10.5], [1,3,0,1.5,19], "7")
		>>> type(smts)
		<class 'FileStorageManager.FileStorageManager'>
		"""

		self.DB = WrappedDB("SM_DB.dbdb")
		self.timeSeries = TimeSeries(values, times)
		self.key = self.DB.storeKeyAndTimeSeries(self.timeSeries, key)

	def from_db(self, key):
		"""
		Looks up a Time Series with identifier key and returns it.
		"""

		if (key == None):
			return KeyError

		self.key = key
		self.DB = WrappedDB("SM_DB.dbdb")
	
		return self.DB.getTimeSeries(self.key)

	# Required functions according to the SizedContainerTimeSeriesInterface:
	def __getitem__(self, item):
		return self.timeSeries.getitem(item)

	def __iter__(self):
		return self.timeSeries.iter()

	def __len__(self):
		return self.timeSeries.len()

	def __setitem__(self, time, value):
		return self.timeSeries.setitem(time, value)

	def items(self):
		return self.timeSeries.items()

	def iteritems(self):
		return self.timeSeries.iteritems()

	def itertimes(self):
		return self.timeSeries.itertimes()

	def itervalues(self):
		return self.timeSeries.itervalues()

	def mean(self):
		return self.timeSeries.mean()

	def std(self):
		return self.timeSeries.std()

	def times(self):
		return self.timeSeries.times()

	def values(self):
		return self.timeSeries.values()
