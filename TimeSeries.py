import itertools
import reprlib
import numpy as np
import numbers
from lazy import LazyOperation
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface

class TimeSeries(SizedContainerTimeSeriesInterface):
	""" 
	AbsFun: two lists, one for times and one for values represent the sized container time series. 
	The list of times is optional and if it is not provided, times are treated as the indexes of the values 
	list. There cannot be duplicate times as there should only be one value recorded at each time.
	
	RepInv: Times and values must only include numbers, and must be same length, if times is included. There 
	cannot be duplicate times.
	"""
	def __init__(self, values, times=None):
		"""
		Initializes a TimeSeries instance with value list and optional times list
		Represents data internally as lists.

		Parameters
		----------
		values : list of ints or floats (A sequence of numerical values)
		times : list of ints or floats  (A sequence of numerical times)

		Returns
		-------
		TimeSeries
			A time series object with times and values equal to the parameters
		
		>>> t = [1.5, 2, 2.5, 3, 10.5]
		>>> v = [1, 3, 0, 1.5, 1]
		>>> z = TimeSeries(v, t)
		>>> z[3]
		1.5
		"""
		if (len(values) == 0):
			raise ValueError('Empty values passed in')

		self.repOK(times, values)
		
		# Sort times and values in ascending order of time - It's just neater that way
		if times is not None:
			self.__isTimeNone = False
			times, values = (list(x) for x in zip(*sorted(zip(times, values), key=lambda pair: pair[0])))
			self.__timesseq = list(times)
			self.__valuesseq = list(values)
			self.__times_to_index = {t: i for i, t in enumerate(times)}
		else:
			self.__isTimeNone = True
			self.__timesseq = None
			self.__valuesseq = list(values)
			self.__times_to_index = None
		
	def repOK(self, times, values):
		if times is None:
			assert self._hasOnlyNumbers(values), "Values should only include numbers"
		else:
			assert self._hasOnlyNumbers(times) and self._hasOnlyNumbers(values), "Both times and values should only include numbers"
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
	
	def _tupleWithVals(self, vals):
		"""
		Private helper function uses to form a list of tuples based on the input values.
		Note that vals must be sorted in the same order as self.timesseq
		Considers if times are provided or not.
		"""
		if self.__isTimeNone:
			return [(i, x) for i, x in enumerate(vals)]
		else:
			return list(zip(self.timesseq, vals))

	@property
	def lazy(self, function=None, *args):
		"""
		>>> x = TimeSeries([1,2,3,4],[1,4,9,16])
		>>> print(x)
		TimeSeries
		Length: 4
		First (oldest): 1, Last (newest): 4
		>>> y = x.lazy
		>>> print(y)
		LazyOperation : Function = <class 'TimeSeries.TimeSeries'>, Args = ([1, 2, 3, 4], [1, 4, 9, 16]), Kwargs = {}
		>>> print(y.eval())
		TimeSeries
		Length: 4
		First (oldest): 1, Last (newest): 4
		"""
		def identity(arg):
			return arg

		if function==None:
			return LazyOperation(identity(TimeSeries), self.__valuesseq, self.__timesseq)		
		return LazyOperation(function,*args)	

	@property
	def timesseq(self):
		"""
		Time series index
		Private property - can't be called directly
		"""
		return self.__timesseq

	@property
	def valuesseq(self):
		"""
		Time serires value
		Private property - can't be called directly
		"""
		return self.__valuesseq

	@property
	def times_to_index(self):
		"""
		map time index with integer index of the array
		Priviate property - can't be called directly
		"""
		return self.__times_to_index
	
	def times(self):
		"""
		Returns the times sequence, or None if there are no times provided in the Constructor.
		
		Parameters
		----------
		None
		
		Returns
		-------
		times
		
		Notes
		-----
		POST:
			- times could be returned as a list or numpy array depending on which time series class.

		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> a.times()
		[1, 1.5, 2, 2.5, 10]
		"""
		return self.timesseq

	def values(self):
		"""
		Returns the values sequence.
		
		Parameters
		----------
		None
		
		Returns
		-------
		vals
		
		Notes
		-----
		POST:
			- vals could be returned as a list or numpy array depending on which time series class.
			
		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> a.values()
		[0, 2, -1, 0.5, 0]

		"""
		return self.valuesseq

	def items(self):
		"""
		Returns sequence of (time, value) tuples.
		If time is not provided, returns sequence of (index, value) tuples.
		
		Parameters
		----------
		None
		
		Returns
		-------
		list of (time, val) tuple or (index, val) if times are not provided.

		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> a.items()
		[(1, 0), (1.5, 2), (2, -1), (2.5, 0.5), (10, 0)]
		"""
		self.repOK(self.timesseq, self.valuesseq)
		if self.__isTimeNone:
			return [(i, x) for i, x in enumerate(self.valuesseq)]
		else:
			return list(zip(self.timesseq, self.valuesseq))
	
	def __len__(self):
		"""
		Returns length of the sequence. This length is specifically the length of the values.
		
		Parameters
		----------
		None
		
		Returns
		-------
		length
		
		>>> t = [1.5, 2, 2.5, 3, 10.5]
		>>> v = [1, 3, 0, 1.5, 1]
		>>> a = TimeSeries(v, t)
		>>> len(a)
		5
		"""
		self.repOK(self.timesseq, self.valuesseq)
		return len(self.valuesseq)

	def __getitem__(self, time):
		"""
		Returns the value at the specified time. If times are not initialized in constructor, then this 
		time input will serve as the index in the values array. If item is not found, raise an IndexError.
		
		Parameters
		----------
		time
		
		Returns
		-------
		value, or throws an IndexError if value is not found
		
		Notes
		-----
		PRE: 
			- Time must exist in the timesseq, or is indexed. If not, throw an IndexError.
		
		>>> t = [1.5, 2, 2.5, 3, 10.5]
		>>> v = [1, 3, 0, 1.5, 1]
		>>> a = TimeSeries(v, t)
		>>> a[2.5]
		0
		"""
		self.repOK(self.timesseq, self.valuesseq)
		
		if self.__isTimeNone:
			if time >= len(self):
				raise IndexError('Time does not exist.')
			return self.valuesseq[time]
		else:
			if time not in self.times_to_index:     
				raise IndexError('Time does not exist.')
			return self.valuesseq[self.times_to_index[float(time)]]

	def __setitem__(self, time, value):
		"""
		Changes the value at specified time to input value. 
		This does not allow us to extend the sequence. It only modifies an existing time's value.
		If times are not initialized in constructor, then this time input will serve as the index in 
		the values array. If item is not found, throw an IndexError.
		
		Parameters
		----------
		time : int or float
		value : int or float
		
		Returns
		-------
		Modified the value specified by 
		
		Notes
		-----
		PRE: 
			- Time must exist in the timesseq, or is indexed. If not, throw an IndexError.
		POST:
			- Value is modified at the time specified. We are not allowed to extend the sequence.
		
		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> a[1] = 12.0
		>>> a[1]
		12.0
		>>> a[2.5] = 3.0
		>>> a[2.5]
		3.0

		"""
		indexToInsert = -1
		if self.__isTimeNone:
			if time < 0 or time >= len(self):
				raise IndexError('Time does not exist.')
			else:
				indexToInsert = time
		else:
			if time not in self.times_to_index:     
				raise IndexError('Time does not exist.')
			else:
				indexToInsert = self.times_to_index[time]
		self.valuesseq[indexToInsert] = value
		self.repOK(self.timesseq, self.valuesseq)
		
	def __iter__(self):
		"""
		Iterates over values.
		
		Parameters
		----------
		None
		
		Returns
		-------
		Iterator of val
		
		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> for val in a:
		...     print(val)
		0
		2
		-1
		0.5
		0
		"""
		self.repOK(self.timesseq, self.valuesseq)
		for v in self.valuesseq:
			yield v

	def itertimes(self):
		"""
		Iterates over times.
		
		Parameters
		----------
		None
		
		Returns
		-------
		Iterator of time
		
		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> for val in a.itertimes():
		...     print(val)
		1
		1.5
		2
		2.5
		10
		"""
		self.repOK(self.timesseq, self.valuesseq)
		if self.__isTimeNone:
			yield None
		else:
			for t in self.timesseq:
				yield t

	def itervalues(self):
		"""
		Iterates over values.
		
		Parameters
		----------
		None
		
		Returns
		-------
		Iterator of val
		
		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> for val in a.itervalues():
		...     print(val)
		0
		2
		-1
		0.5
		0
		"""        
		self.repOK(self.timesseq, self.valuesseq)
		for v in self.valuesseq:
			yield v

	def iteritems(self):
		"""
		Iterates over the time-values tuples.
		
		Parameters
		----------
		None
		
		Returns
		-------
		Iterator of (time, val)
		
		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> for val in a.iteritems():
		...     print(val)
		(1, 0)
		(1.5, 2)
		(2, -1)
		(2.5, 0.5)
		(10, 0)
		"""        
		self.repOK(self.timesseq, self.valuesseq)
		dictOfItems = {}
		if self.__isTimeNone:
			dictOfItems = [(i, x) for i, x in enumerate(self.valuesseq)]
		else:
			dictOfItems = zip(self.timesseq, self.valuesseq)
		for t, v in dictOfItems:
			yield t, v

	def __repr__(self):
		"""
		Returns all tuples in the format (time, val) in a String form.
		If more than 100 values, the output will be truncated with ellipses.
	
		Parameters
		----------
		None

		Returns
		-------
		String of tuples.
		"""
		class_name = type(self).__name__
		myrepr = reprlib.aRepr
		myrepr.maxlist = 100 # More than 100 then replace with ellipses
		components = myrepr.repr(self._tupleWithVals(self.valuesseq))
		components = components[components.find('['):]
		return '{}({})'.format(class_name, components)
	
	def __str__(self):
		"""
		Only returns values without times.
		Shows the length of the time series, and first and last values.
	
		Parameters
		----------
		None

		Returns
		-------
		Length, First and Last values.
		"""
		class_name = type(self).__name__
		first = 'N/A'
		last = 'N/A'
		if len(self) > 0:
			first = str(self.valuesseq[0])
			last = str(self.valuesseq[-1])
		return '%s\nLength: %d\nFirst (oldest): %s, Last (newest): %s' % (class_name, len(self), first, last)
	
	def __abs__(self):
		"""
		Unary function that absolutes all the values and returns them as tuples.
	
		Parameters
		----------
		None

		Returns
		-------
		List of (time, val)
		
		>>> t = [3., 1., 2.]
		>>> v = [4., -5., -6.]
		>>> z = TimeSeries(v, t)
		>>> abs(z)
		[(1.0, 5.0), (2.0, 6.0), (3.0, 4.0)]
		"""
		abs_vals = np.sqrt([vi * vi for vi in self.valuesseq])
		return self._tupleWithVals(abs_vals)
		
	def __bool__(self):
		"""
		Unary function that returns boolean value of self. 
	
		Parameters
		----------
		None

		Returns
		-------
		True if self exists, False otherwise.
		
		>>> t = [3., 1., 2.]
		>>> v = [4., -5., -6.]
		>>> z = TimeSeries(v, t)
		>>> bool(z)
		True
		"""
		return bool(abs(self))
	
	def __neg__(self):
		"""
		Unary function that returns values as tuples after applying a -1 multiplier to them.
	
		Parameters
		----------
		None

		Returns
		-------
		List of (time, val)
		
		>>> t = [3., 1., 2.]
		>>> v = [4., 5., 6.]
		>>> z = TimeSeries(v, t)
		>>> -z
		[(1.0, -5.0), (2.0, -6.0), (3.0, -4.0)]
		"""
		neg_vals = [-vi for vi in self.valuesseq]
		return self._tupleWithVals(neg_vals)
		
	def __pos__(self):
		"""
		Unary function that returns values as they are (without applying a negative multiplier).
	
		Parameters
		----------
		None

		Returns
		-------
		List of (time, val)

		>>> t = [3., 1., 2.]
		>>> v = [4., 5., 6.]
		>>> z = TimeSeries(v, t)
		>>> +z
		[(1.0, 5.0), (2.0, 6.0), (3.0, 4.0)]
		"""
		return self._tupleWithVals(self.valuesseq)
	
	def _valuesSortedByTime(self, other):
		"""
		Private helper function that returns the values sequence of the other TimeSeries, followed by self's 
		values sequence.
		
		Raises a NotImplementedError when the other object is not a TimeSeries.
		Raises a ValueError when the time sequence of both TimeSeries are not identical.
		"""
		if isinstance(other, numbers.Real): # Adding a constant
			self_times, self_values = (list(x) for x in zip(*sorted(zip(self.itertimes(), self.itervalues()), key=lambda pair: pair[0])))
			return other, self_values, self_times
		if not isinstance(other, TimeSeries): # Not adding a constant or a TimeSeries, throws error
			raise NotImplementedError('Unable to compare TimeSeries with a non-TimeSeries class')
		# Sort both sequences based on time
		other_times, other_values = (list(x) for x in zip(*sorted(zip(other.itertimes(), other.itervalues()), key=lambda pair: pair[0])))
		self_times, self_values = (list(x) for x in zip(*sorted(zip(self.itertimes(), self.itervalues()), key=lambda pair: pair[0])))
		if (other_times != self_times):
			raise ValueError('Time sequence of both TimeSeries must be identical, i.e. same length and same times')
		return other_values, self_values, self_times
	
	def __eq__(self, other):
		"""
		Compares with another TimeSeries, and returns True if all the values are equal, False otherwise.
	
		Parameters
		----------
		other: Another TimeSeries object

		Returns
		-------
		True when values are equal, False otherwise

		Notes
		-----
		PRE: 
			- The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
			- If both sequences do not have times, just directly compare values in unsorted form.
			
		>>> t = [3., 1., 2.]
		>>> v = [4., 5., 6.]
		>>> z = TimeSeries(v,t)
		>>> t2 = [3., 2., 1.]
		>>> v2 = [4., 6., 5.]
		>>> z2 = TimeSeries(v2,t2)
		>>> z2 == z   
		True
		>>> z2[1] = 99
		>>> z2 == z
		False
		>>> z = TimeSeries(v)
		>>> z2 = TimeSeries(v2)
		>>> z2 == z
		False
		"""
		other_values, self_values, _ = self._valuesSortedByTime(other)
		if isinstance(other, numbers.Real):
			raise NotImplementedError('Unable to compare TimeSeries with a non-TimeSeries class')
		if self.__isTimeNone:
			return self.values() == other.values()
		return other_values == self_values
	
	def __add__(self, other):
		"""
		Adds the values of the two TimeSeries (or constant) and returns a new TimeSeries.
	
		Parameters
		----------
		other: Another TimeSeries object, or constant

		Returns
		-------
		A new TimeSeries with the summed values of the two provided TimeSeries (or constant).

		Notes
		-----
		PRE: 
			- The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
			
		>>> t = [3., 1., 2.]
		>>> v = [4., 5., 6.]
		>>> z = TimeSeries(v, t)
		>>> t2 = [3., 2., 1.]
		>>> v2 = [99., 6., 5.]
		>>> z2 = TimeSeries(v2, t)
		>>> z2 + z
		TimeSeries([(1.0, 11.0), (2.0, 11.0), (3.0, 103.0)])
		>>> z = TimeSeries(v)
		>>> z2 = TimeSeries(v2)
		>>> z2 + z
		TimeSeries([(0, 103.0), (1, 11.0), (2, 11.0)])
		"""
		other_values, self_values, self_times = self._valuesSortedByTime(other)
		if self.__isTimeNone:
			if isinstance(other, numbers.Real):
				return TimeSeries([self.values()[i] + other for i in range(0, len(self.values()))])
			else:
				return TimeSeries([self.values()[i] + other.values()[i] for i in range(0, len(self.values()))])
		if isinstance(other, numbers.Real):
			return TimeSeries([self_values[i] + other for i in range(0, len(self_values))], self_times)
		else:
			return TimeSeries([self_values[i] + other_values[i] for i in range(0, len(self_values))], self_times)
	
	def __sub__(self, other):
		"""
		Subtract the values of the other TimeSeries (or constant) fom self, and returns a new TimeSeries.
	
		Parameters
		----------
		other: Another TimeSeries object, or constant

		Returns
		-------
		A new TimeSeries with subtracted values of other from self (self - other)

		Notes
		-----
		PRE: 
			- The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
			
		>>> t = [3., 1., 2.]
		>>> v = [4., 5., 6.]
		>>> z = TimeSeries(v, t)
		>>> t2 = [3., 2., 1.]
		>>> v2 = [99., 6., 5.]
		>>> z2 = TimeSeries(v2, t)
		>>> z2 - z
		TimeSeries([(1.0, 1.0), (2.0, -1.0), (3.0, 95.0)])
		>>> z = TimeSeries(v)
		>>> z2 = TimeSeries(v2)
		>>> z2 - z
		TimeSeries([(0, 95.0), (1, 1.0), (2, -1.0)])
		"""
		other_values, self_values, self_times = self._valuesSortedByTime(other)
		if self.__isTimeNone:
			if isinstance(other, numbers.Real):
				return TimeSeries([self.values()[i] - other for i in range(0, len(self.values()))])
			else:
				return TimeSeries([self.values()[i] - other.values()[i] for i in range(0, len(self.values()))])
		if isinstance(other, numbers.Real):
			return TimeSeries([self_values[i] - other for i in range(0, len(self_values))], self_times)
		else:
			return TimeSeries([self_values[i] - other_values[i] for i in range(0, len(self_values))], self_times)
	
	def __mul__(self, other):
		"""
		Multiplies the values of the two TimeSeries (or constant) and returns a new TimeSeries.
	
		Parameters
		----------
		other: Another TimeSeries object, or constant

		Returns
		-------
		A new TimeSeries with the multiplied values from both TimeSeries (or constant)

		Notes
		-----
		PRE: 
			- The times sequence of the other TimeSeries must be identical to the first one, if not ValueError is thrown
			
		>>> t = [3., 1., 2.]
		>>> v = [4., 5., 6.]
		>>> z = TimeSeries(v, t)
		>>> t2 = [3., 2., 1.]
		>>> v2 = [99., 6., 5.]
		>>> z2 = TimeSeries(v2, t)
		>>> z2 * z
		TimeSeries([(1.0, 30.0), (2.0, 30.0), (3.0, 396.0)])
		>>> z = TimeSeries(v)
		>>> z2 = TimeSeries(v2)
		>>> z2 * z
		TimeSeries([(0, 396.0), (1, 30.0), (2, 30.0)])
		"""
		other_values, self_values, self_times = self._valuesSortedByTime(other)
		if self.__isTimeNone:
			if isinstance(other, numbers.Real):
				return TimeSeries([self.values()[i] * other for i in range(0, len(self.values()))])
			else:
				return TimeSeries([self.values()[i] * other.values()[i] for i in range(0, len(self.values()))])
		if isinstance(other, numbers.Real):
			return TimeSeries([self_values[i] * other for i in range(0, len(self_values))], self_times)
		else:
			return TimeSeries([self_values[i] * other_values[i] for i in range(0, len(self_values))], self_times)
	
	
	def _get_interpolated(self, tval, timesToUse):
		"""
		Returns the value in TimeSeries corresponding to a single time tval.
		If tval does not exist, return interpolated value.
		If tval is beyond tval bounds, return value at boundary
		(i.e. do not extrapolate).
		This method assume the times in timesseq are monotonically
		increasing; otherwise, results may not be as expected.

		Parameters
		----------
		tval : int or float
		Time series value

		Returns
		-------
		float
		Either the actual or interpolated value associated with the time

	
		"""
		for i in range(len(self)-1):
			# tval less than smallest time
			if tval <= timesToUse[i]:
				return self[timesToUse[i]]
			# tval within range of time series times
			if (tval > timesToUse[i]) & (tval < timesToUse[i+1]):
				# calculate interpolated value
				time_delta = timesToUse[i+1] - timesToUse[i]
				step = (tval - timesToUse[i]) / time_delta
				v_delta = self.valuesseq[i+1] - self.valuesseq[i]
				return v_delta * step + self.valuesseq[i]
		# tval above range of time series times
		return self[timesToUse[len(self)-1]]
	
	
	def interpolate(self, tseq):
		"""
		Returns a TimeSeries object containing the elements
		of a new sequence tseq and interpolated values in the TimeSeries.
		This method assume the times in timesseq are monotonically
		increasing; otherwise, results may not be as expected.

		Parameters
		----------
		tseq : list of ints or floats
		Time series times to interpolate

		Returns
		-------
		TimeSeries
			Time series object with all the interpolated values for the
			given times.

		>>> a = TimeSeries([1, 2, 3],[0, 5, 10])
		>>> b = TimeSeries([100, -100],[2.5, 7.5])
		>>> a.interpolate([1])
		TimeSeries([(1, 1.2)])
		>>> a.interpolate([-100, 100])
		TimeSeries([(-100, 1), (100, 3)])
		"""
		timesToUse = range(len(self)) if self.__isTimeNone else self.timesseq
		valseq = [self._get_interpolated(t, timesToUse) for t in tseq]
		return TimeSeries(values =valseq , times=tseq)
	
	def __contains__(self, value):
		"""
		Takes a value and returns true if it is in the values array.

		Parameters
		----------
		value : int or float, a time series value

		Returns
		-------
		bool
		Whether the value is present in the value series

		>>> t = [1, 1.5, 2, 2.5, 10]
		>>> v = [0, 2, -1, 0.5, 0]
		>>> a = TimeSeries(v, t)
		>>> -1 in a
		True
		>>> 10 in a
		False
		"""
		return value in self.values()
	
    
