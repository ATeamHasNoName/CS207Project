import numpy as np
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface

class SMTimeSeries(SizedContainerTimeSeriesInterface) {
	"""
	Storage Manager class that stores instances of Time Series.
	"""

	def __init__(self, values, times, id=None)
	"""
	Initializes a Storage Manager Time Series classwith value and times lists. Accepts an optional id which stores the Time Series into the Storage Manager. 
	"""

	def _SMTimeSeries.from_db(self, id):
	"""
	Looks up a Time Series with id id and stores the Time Series into memory.
	"""

	def repOK(self, times, values, id):
		assert self._hasOnlyNumbers(times), "Times should only include numbers"
		assert self._hasOnlyNumbers(values), "Values should only include numbers"	
		assert len(times) == len(values), "Length of times and values must be the same"
		assert len(times) == len(set(times)), "Times cannot be duplicated, i.e. there can only be one unique value for each time"

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
		>>> z = TimeSeries(v, t)
		>>> z._hasOnlyNumbers(t)
		True
		"""
		for i in arr:
			try:
				int(i)
			except ValueError:
				return False
		return True


}
