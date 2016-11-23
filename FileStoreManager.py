import numpy as np
from StorageManagerInterface import StorageManagerInterface

class FileStorageManager(StorageManagerInterface) {
	"""
	File Storage Manager class. This class stores 2-d numpy arrays as 64 bit floats for the times and the values of the TimeSeries onto the disk.
	"""

	def store(self, id, t):
		"""
        	stores a instance of SizedContainerTimeSeriesInterface.
        	"""

	def size(self, id):
        	"""
        	fetches the size of the SizedContainerTimeSeriesInterface and returns it.
        	"""

	def get(self, id):
		"""
        	returns a instance of SizedContainerTimeSeriesInterface instance.
        	"""
}
