from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
from arraytimeseries import ArrayTimeSeries
from filestoragemanager import FileStorageManagerSingleton
import numbers
import numpy as np

class SMTimeSeries(SizedContainerTimeSeriesInterface):
	"""
	A subclass of SizedContainerTimeSeriesInterface
	that stores ArrayTimeSeries instances on disk.

	Attributes:
	----------
		_values : sequence-like
			Actual data points for SMTimeSeries.
			Any user-provided sequence-like object. Mandatory.
		_times : sequence-like
			Time values for SMTimeSeries. Mandatory

	Notes
	-----
		PRE: 
		 - `values` is sorted in non-decreasing order
		 - _times are mandatory elements that must represent a montonic sequence.

	INVARIANTS: values and times must be sequences.

	WARNINGS: 
		- User must provide times and values.
		- Does not maintain an accurate time series if `input data` is unsorted.

	"""
	def __init__(self, times, values, id=None):
		"""
		Parameters:
		----------
			values : sequence-like
				Actual data points for SMTimeSeries.
				Any user-provided sequence-like object. Mandatory.
			times : sequence-like
				Time values for SMTimeSeries. Mandatory

		Notes
		-----
			PRE: _times are mandatory elements that must represent a montonic sequence.

		Examples:
		---------
		>>> ts = SMTimeSeries(times= [1,2,3], values= [100,200,300])
		"""
		self.__class__.is_sequence(times)
		self.__class__.is_sequence(values)
		self._times = (list(times))

		if isinstance(values, dict):
			self._values = (list(values.values()))
		else:
			self._values = (list(values))

		# if no id is provided, create a new and unique one
		if id==None:
			id = FileStorageManagerSingleton.get_unique_id()

		# store the time series on disk
		FileStorageManagerSingleton.store(str(id), ArrayTimeSeries(self._times, self._values))
		self._id = str(id)

	@classmethod
	def from_db(cls, id):
		"""
		A method with an id to look up and fetch from the storage manager,
		having the manager allocate the time series in memory.

		Parameters:
		----------
			id : int
				the id used to get the time series from the database.

		Returns:
		-------
		SMTimeSeries : an in memory instance of the time series associated with the 
		provided id.
		"""
		return FileStorageManagerSingleton.get(id)

	def __len__(self):
		"""
		Method used to determine the length of the SMTimeSeries

		Returns:
		--------
		length : int
			The length of the ArrayTimeSeries based on the ._values field.
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return len(ts.values())

	def __eq__(self, rhs):
		"""
		Method used to test if two SizedContainerTimeSeriesInterface instances have the same times and values

		Parameters:
		-----------
		rhs : instance of SizedContainerTimeSeriesInterface
			rhs will be compared to the time series sequence represented by self

		Returns:
		--------
		bool : True if the series are equivalent
		"""
		ts1 = FileStorageManagerSingleton.get(self._id)
		ts2 = FileStorageManagerSingleton.get(rhs._id)
		return ts1==ts2

	def __add__(self, rhs):
		"""
			The rhs argument will be added to each element of the time series if it is an instance of numbers.Real.
			If the rhs argument is an instance of SMTimeSeries, it will do the add element-wise. 

			Parameters: 
			-----------
			rhs : instance of SizedContainerTimeSeriesInterface
				used to perform the add on the SMTimeSeries represented by self

			Raises:
			-------
				TypeError : if an attempt to add a list instance to the SMTimeSeries is made

		"""
		try: 
			if isinstance(rhs, list):
				raise "Cannot compare list to SMTimeSeries!"
			if isinstance(rhs, numbers.Real):
				ts1 = FileStorageManagerSingleton.get(self._id)
				product = ts1 + rhs
				return SMTimeSeries(product.times(), product.values())
			else:
				ts1 = FileStorageManagerSingleton.get(self._id)
				ts2 = FileStorageManagerSingleton.get(rhs._id)
				product = ts1 + ts2
				return SMTimeSeries(product.times(), product.values())
		except TypeError:
			raise NotImplemented

	def __sub__(self, rhs):
		"""
			The rhs argument will be subtracted from each element of the time series if it is an instance of numbers.Real.
			If the rhs argument is an instance of SMTimeSeries, it will do the subtraction element-wise.

			Parameters:
			-----------
			rhs : instance of SizedContainerTimeSeriesInterface
				used to perform the sub on the SMTimeSeries represented by self

			Raises:
			-------
				TypeError : if an attempt to sub from a list instance to the SMTimeSeries is made

		"""
		try: 
			if isinstance(rhs, list):
				raise "Cannot compare list to SMTimeSeries!"
			if isinstance(rhs, numbers.Real):
				ts1 = FileStorageManagerSingleton.get(self._id)
				product = ts1 - rhs
				return SMTimeSeries(product.times(), product.values())
			else:
				ts1 = FileStorageManagerSingleton.get(self._id)
				ts2 = FileStorageManagerSingleton.get(rhs._id)
				product = ts1 - ts2
				return SMTimeSeries(product.times(), product.values())
		except TypeError:
			raise NotImplemented

	def __mul__(self, rhs):
		"""
			The rhs argument will be multiplied with each element of the time series if it is an instance of numbers.Real.
			If the rhs argument is an instance of SMTimeSeries, it will do the multiplication element-wise.

			Parameters:
			-----------
			rhs : instance of SizedContainerTimeSeriesInterface
				used to perform the multiplication on the SMTimeSeries represented by self

			Raises:
			-------
				TypeError : if an attempt to multiply with a list instance to the SMTimeSeries is made

		"""
		try: 
			if isinstance(rhs, list):
				raise "Cannot compare list to SMTimeSeries!"
			if isinstance(rhs, numbers.Real):
				ts1 = FileStorageManagerSingleton.get(self._id)
				product = ts1 * rhs
				return SMTimeSeries(product.times(), product.values())
			else:
				ts1 = FileStorageManagerSingleton.get(self._id)
				ts2 = FileStorageManagerSingleton.get(rhs._id)
				product = ts1 * ts2
				return SMTimeSeries(product.times(), product.values())
		except TypeError:
			raise NotImplemented

	def __neg__(self):
		"""
			Used to return a time series instance with each value being negative of the original. 
			The times are left untouched.

			Returns:
			-------
				self : an instance of self with negated values but no change to the times
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return SMTimeSeries(ts.times(), -ts.values())

	def __pos__(self):
		"""
			Used to return a time series instance with each value's sign preserved

			Returns:
			-------
				self : an instance of self with each value's sign preserved
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return SMTimeSeries(ts.times(), ts.values())

	def __iter__(self):
		"""
		Description
		-----------
		Iterates over `self._values`.
		Equivalent to calling iter() on the instance.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return iter(ts)

	def itertimes(self):
		"""
		Description
		------------
		Iterates over the times in `self._times`

		Parameters
		----------
		self: instance of subclass of SizedTimeSeriesInterface

		Returns
		-------
		Yields values from `self._times`
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts.itertimes()

	def itervalues(self):
		"""
		Description
		------------
		Iterates over the values of the time eries

		Parameters
		----------
		self: instance of subclass of SizedTimeSeriesInterface

		Returns
		-------
		Yields values from `self._values`

		Notes
		-----
		Identical to iter(self)
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts.itervalues()

	def iteritems(self):
		"""
			Description
			------------
			Iterates over (time, value) tuples of the time series

			Parameters
			----------
			self: instance of subclass of SizedTimeSeriesInterface

			Returns
			-------
			Yields (time, value) tuples
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts.iteritems()

	def __getitem__(self, index):
		"""
		Description
		-----------
		Instance method for indexing into a fixed-size Time Series.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		The value of `self._values` located at index `index`.
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts[index]

	def __setitem__(self, index, value):
		"""
		Description
		-----------
		Sets the element of `self._values`
		at index `index` equal to `value`.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface
		index: int
			index to change the value at
		value : float
			the new value to be set
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		ts[index] = value
		FileStorageManagerSingleton.store(self._id, ts)

	def __contains__(self, needle):
		"""
		Description
		-----------
		Checks if `needle` is contained in `self._values`

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface
		needle: float
			Time series value to search for

		Returns
		-------
		True if `needle` found in `self._values`, else False
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return (needle in ts)

	def __repr__(self):
		"""
		Description
		-----------
		Internal String representation for all subclasses of
		SizedContainerTimeSeriesInstance
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return repr(ts)

	def __str__(self):
		"""
		Description
		-----------
		Instance method for pretty-printing the time series contents.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		pretty_printed: string
			an end-user-friendly printout of the time series.
			If `len(self._values) > MAX_LENGTH`, printout abbreviated
			using an ellipsis: `['1.0','2.0','3.0', ..., '8.0','9.0','10.0']`.
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return str(ts)

	def __abs__(self):
		"""
		Description
		-----------
		Returns the L2-norm of `self._values`

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		L2-norm as a float

		Notes
		-----
		Casts `self._values` into a np-array for fasted norm calcualtion.
		This won't impact the final return value, as it is a float.
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return abs(ts)

	def __bool__(self):
		"""
		Description
		-----------
		Checks if `self._values` is empty.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		True/False
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return bool(abs(ts))

	def values(self):
		"""Return values for use in unit tests"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts.values()

	def times(self):
		"""Return times for use in unit tests"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts.times()

	def items(self):
		"""Returns list of zipped time-value tuples for use in unit tests"""
		ts = FileStorageManagerSingleton.get(self._id)
		return ts.items()

	def interpolate(self, newTimes):
		"""
		Returns new SMTimeSeries instance with piecewise-linear-interpolated values
		for submitted time-times.If called times are outside of the domain of the existing
		SM Time Series, the minimum or maximum values are returned.

		Parameters
		----------
		self: TimeSeries instance
		ts_to_interpolate: list or other sequence of times to be interpolated

		"""
		ts = FileStorageManagerSingleton.get(self._id)
		arrayinterpolate = ts.interpolate(newTimes)
		return SMTimeSeries(arrayinterpolate.times(), arrayinterpolate.values())

	def mean(self, chunk = None):
		"""
		Method used to calculate the mean of the time series. 

		Parameters:
		-----------
		chunk = an optional subset of the time series to do the calculation on 

		Returns: 
		--------
		np.mean : the mean of the time series
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return np.mean(ts._values)

	def std(self, chunk = None):
		"""
		Method used to calculate the standard deviation of the time series. 

		Parameters:
		-----------
		chunk = an optional subset of the time series to do the calculation on

		Returns:
		--------
		np.std : the standard deviation of the time series 
		"""
		ts = FileStorageManagerSingleton.get(self._id)
		return np.std(ts._values, ddof=1)