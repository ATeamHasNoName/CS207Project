import numpy as np
import sys
import os
from WrappedDB import *
sys.path.append('../MS1/')
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from TimeSeries import TimeSeries

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
	
		>>> smts = SMTimeSeries([1.5, 2,6,8,9], [1, 3, 0, 1.5, 10], key = "1")
		>>> type(smts)
		<class 'SMTimeSeries.SMTimeSeries'>
		>>> DB.remove("ts_1.dbdb")
		"""

		self.DB = WrappedDB()
		self.timeSeries = TimeSeries(values, times)
		self.key = self.DB.storeKeyAndTimeSeries(key = key, timeSeries = self.timeSeries)

	def from_db(self, key):
		"""
		Looks up a Time Series with identifier key and returns it.
		
		Parameters
		----------
		key: a key to fetch the TimeSeries from the database

		Returns
		-------
		None
		"""
		self.key = key
		self.DB = WrappedDB()
		return self.DB.getTimeSeries(self.key)

	# Required functions according to the SizedContainerTimeSeriesInterface:
	def __getitem__(self, item):
		return self.timeSeries[item]

	def __iter__(self):
		for v in self.timeSeries:
			yield v

	def __len__(self):
		return len(self.timeSeries)

	def __setitem__(self, time, value):
		self.timeSeries[time] = value 

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
