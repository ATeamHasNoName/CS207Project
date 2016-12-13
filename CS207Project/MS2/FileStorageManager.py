import numpy as np
import os
import sys
from StorageManagerInterface import StorageManagerInterface
from WrappedDB import *

class FileStorageManager(StorageManagerInterface):
	"""
	File Storage Manager class. This class stores 2-d numpy arrays as 64 bit floats for the times and the values of the TimeSeries onto the disk.
	Essentially we wrote our own encode function in WrappedDB that encodes TimeSeries objects in their String representations before storing them.
	"""

	def __init__(self):
		"""
		Initializes a FileStorageManager instance with a filename to store entries to disk.
		Cache size can be changed in initializing WrappedDB.

		Parameters
		----------
		None

		Returns
		-------
		None
		
		>>> fsm = FileStorageManager()
		>>> type(fsm)
		<class 'FileStorageManager.FileStorageManager'>
		"""
		# This cache size can be changed. 10 is the default.
		self.db = WrappedDB(cacheSize=10)

	def store(self, timeSeries, key=None):
		"""
		Stores an instance of SizedContainerTimeSeriesInterface using a string or int key.
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface
		timeSeries: Concrete class of SizedContainerTimeSeriesInterface
		
		Returns
		-------
		Key of the timeseries
		
		Notes
		-----
		PRE:
			- key has to be string or int
			- timeSeries has to be a valid SizedContainerTimeSeriesInterface concrete class
			
		>>> fsm = FileStorageManager()
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> key = fsm.store(timeSeries=ts, key="1")
		>>> fsm.size(key)
		5
		>>> DB.remove("ts_" + str(key) + ".dbdb")
		"""
		genKey = self.db.storeKeyAndTimeSeries(timeSeries=timeSeries, key=key)
		return genKey

	def size(self, key):
		"""
		Fetches the size of the SizedContainerTimeSeriesInterface and returns it.
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface
		
		Returns
		-------
		Int size of time series, or -1 if it does not exist
		
		Notes
		-----
		PRE:
			- key has to be string or int
			
		>>> fsm = FileStorageManager()
		>>> fsm.size("2")
		-1
		"""
		return self.db.getTimeSeriesSize(key=key)

	def get(self, key):
		"""
		Returns an instance of the SizedContainerTimeSeriesInterface using the key.
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface
		
		Returns
		-------
		SizedContainerTimeSeriesInterface instance
		
		Notes
		-----
		PRE:
			- key has to be string or int

		POST:
			- SizedContainerTimeSeriesInterface is actually a TimeSeries class (more generic than ArrayTimeSeries)
			
		>>> fsm = FileStorageManager()
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> key = fsm.store(timeSeries=ts)
		>>> secondval = fsm.get(key).values()[1]
		>>> secondval
		2.0
		>>> DB.remove("ts_" + str(key) + ".dbdb")
		"""
		return self.db.getTimeSeries(key=key)
