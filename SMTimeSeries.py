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
		"""
		self.key = key
		self.DB = WrappedDB("SM_DB.dbdb")
		self.DB.storeKeyAndTimeSeries(key,self, TimeSeries(values, times))
 

	def from_db(self, key):
		"""
		Looks up a Time Series with identifier key and returns it.
		"""
		self.DB = WrappedDB("SM_DB.dbdb")
		
		# Check if SMTimeSeries is in database:
		if (self.DB.getTimeSeriesSize(key) == -1):
			print('SMTimeSeries with key = {0:%i} is not in Database.'.format(key))
			raise KeyError
		else:
			return self.DB.getTimeSeries(key)

#	def repOK(self, times, values, id):
#		assert self._hasOnlyNumbers(times), "Times should only include numbers"
#		assert self._hasOnlyNumbers(values), "Values should only include numbers"	
#		assert len(times) == len(values), "Length of times and values must be the same"
#		assert len(times) == len(set(times)), "Times cannot be duplicated, i.e. there can only be one unique value for each time"

	def _hasOnlyNumbers(self, arr):
		"""
		Private function to test if the input array consists of only numbers

		Parameters
		----------
		arr: A sequences of any value type

		Returns
		-------
		Boolen value if all elements in the array are numeric

		>>> t = [1.5, 2, 2.5, 3, 10.5]
		>>> v = [1, 3, 0, 1.5, 1]
		>>> z = SMTimeSeries(v, t)
		>>> z._hasOnlyNumbers(t)
		True
		"""
		for i in arr:
			try:
				int(i)
			except ValueError:
				return False
		return True
