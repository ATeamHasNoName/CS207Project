from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from TimeSeries import TimeSeries
import numpy as np
import os
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
	
		>>> smts = SMTimeSeries([1.5, 2,6,8,9], [1, 3, 0, 1.5, 10])
		>>> type(smts)
		<class 'SMTimeSeries.SMTimeSeries'>
		"""

		self.DB = WrappedDB("SM_DB.dbdb")
		self.timeSeries = TimeSeries(values, times)
		self.key = self.DB.storeKeyAndTimeSeries(key = key, timeSeries = self.timeSeries)

	def from_db(self, key, database):
		"""
		Looks up a Time Series with identifier key and returns it.
		
		Parameters
		----------
		key: a key to fetch the TimeSeries from the database

		Returns
		-------
		None

		>>> DB = WrappedDB("SM_DB.dbdb")
		>>> key = "7"
		>>> values = [1.5, 2, 2.5, 3, 10.5];
		>>> times = [1,3,0,1.5,19];
		>>> ts = TimeSeries(values, times)
		>>> smts = SMTimeSeries(values, times, key)
		>>> key = DB.storeKeyAndTimeSeries(key = key, timeSeries = ts)
		>>> timeSeriesFromDB = smts.from_db(key, "SM_DB.dbdb")
		>>> timeSeriesFromDB
		TimeSeries([(0.0, 2.5), (1.0, 1.5), (1.5, 3.0), (3.0, 2.0), (19.0, 10.5)])
		>>> os.remove("SM_DB.dbdb")
		"""

		if (key == None):
			print("Key is not in Database\n")
			return KeyError

		self.key = key
		self.DB = WrappedDB(database)
	
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
