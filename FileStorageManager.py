import numpy as np
from StorageManagerInterface import StorageManagerInterface
import sys
sys.path.append('./DB/')
from WrappedDB import WrappedDB

class FileStorageManager(StorageManagerInterface):
	"""
	File Storage Manager class. This class stores 2-d numpy arrays as 64 bit floats for the times and the values of the TimeSeries onto the disk.
	Essentially we wrote our own encode function in WrappedDB that encodes TimeSeries objects in their String representations before storing them.
	"""

	def __init__(self, filename):
		self.db = WrappedDB(filename)

	def store(self, key, timeSeries):
		"""
		stores a instance of SizedContainerTimeSeriesInterface.
		"""
		self.db.storeKeyAndTimeSeries(key, timeSeries)

	def size(self, key):
		"""
		fetches the size of the SizedContainerTimeSeriesInterface and returns it.
		"""
		return self.db.getTimeSeriesSize(key)

	def get(self, key):
		"""
		returns a instance of SizedContainerTimeSeriesInterface instance.
		"""
		return self.db.getTimeSeries(key)