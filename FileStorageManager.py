import numpy as np
from TimeSeries import TimeSeries
from StorageManagerInterface import StorageManagerInterface
import sys
import os
sys.path.append('./DB/')
from WrappedDB import WrappedDB

class FileStorageManager(StorageManagerInterface):
	"""
	File Storage Manager class. This class stores 2-d numpy arrays as 64 bit floats for the times and the values of the TimeSeries onto the disk.
	Essentially we wrote our own encode function in WrappedDB that encodes TimeSeries objects in their String representations before storing them.
	"""

	def __init__(self, filename):
		"""
		Initializes a FileStorageManager instance with a filename to store entries to disk.

		Parameters
		----------
		filename: a String filename that ends with .dbdb

		Returns
		-------
		None
		
		>>> fsm = FileStorageManager('testfsm.dbdb')
		>>> type(fsm)
		<class 'FileStorageManager.FileStorageManager'>
		>>> os.remove('testfsm.dbdb')
		"""
		self.db = WrappedDB(filename)

	def store(self, key, timeSeries):
		"""
		Stores an instance of SizedContainerTimeSeriesInterface using a string or int key.
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface
		timeSeries: Concrete class of SizedContainerTimeSeriesInterface
		
		Returns
		-------
		None
		
		Notes
		-----
		PRE:
			- key has to be string or int
			- timeSeries has to be a valid SizedContainerTimeSeriesInterface concrete class
			
		>>> fsm = FileStorageManager('testfsm.dbdb')
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> fsm.store("1", ts)
		>>> fsm.size("1")
		5
		>>> os.remove('testfsm.dbdb')
		"""
		self.db.storeKeyAndTimeSeries(key, timeSeries)

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
			
		>>> fsm = FileStorageManager('testfsm.dbdb')
		>>> fsm.size("2")
		-1
		>>> os.remove('testfsm.dbdb')
		"""
		return self.db.getTimeSeriesSize(key)

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
			
		>>> fsm = FileStorageManager('testfsm.dbdb')
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> fsm.store("1", ts)
		>>> secondval = fsm.get("1").values()[1]
		>>> secondval
		2.0
		>>> os.remove('testfsm.dbdb')
		"""
		return self.db.getTimeSeries(key)
		