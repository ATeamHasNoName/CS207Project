from streamtimeseriesinterface import StreamTimeSeriesInterface
import math

class SimulatedTimeSeries(StreamTimeSeriesInterface):
	"""
	Description
	-----------
	Implements a Time Series without a fixed storage.
	Uses generators to produce a streaming effect.

	Parameters
	----------
	times_gen: generator
		lazily evaluated generator representing time values
	values: generator
		lazily evaluated generator representing data values
	"""
	def __init__(self, times_gen, values_gen):
		super(SimulatedTimeSeries, self).__init__()
		self.times = times_gen
		self.values = values_gen

	def produce(self, chunk=1):
		"""
		Description
		-----------
		Produces `chunk` new values of the time series

		Parameters
		----------
		self: SimulatedTimeSeries instance
		chunk: int
			"chunk size", i.e. number of values to produce

		Returns
		-------
		list consisting of `chunk` (time, ts_value) pairs
		"""

		try:
			produced = [(next(self.times), next(self.values)) for _ in range(chunk)]

		except StopIteration:
			# not sure what the optimal error type is here
			raise IndexError("Make sure you don't produce more values than the generator has!")

		return produced

	def online_mean(self):
		"""
		Description
		-----------
		Produces a SimulatedTimeSeries object of online means.

		WARNING: When produce is called on the output, it will destructively
			alter self.values in the input

		Parameters
		----------
		self: Takes a SimulatedTimeSeries instance for which we would like to
			compute the online mean

		Returns
		-------
		A new SimulatedTimeSeries consisting of the input's time dimension
			and the associated online mean
		"""
		def __gen():
			n = 0
			mu = 0
			for value in self.values:
				n += 1
				delta = value - mu
				mu = mu + delta/n
				yield mu
		return SimulatedTimeSeries(self.times, __gen())

	def online_std(self):
		"""
		Description
		-----------
		Produces a SimulatedTimeSeries object of online standard deviations.

		WARNING: When produce is called on the output, it will destructively
			alter self.values in the input

		Parameters
		----------
		self: Takes a SimulatedTimeSeries instance for which we would like to
			compute the online standard deviation

		Returns
		-------
		A new SimulatedTimeSeries consisting of the input's time dimension
			and the associated online standard deviation
		"""
		def __gen():
			n = 0
			mu = 0
			dev_accum = 0
			stddev = 0
			
			for value in self.values:
				n += 1
				delta = value - mu
				if n > 1:
					# update stdev
					dev_accum = dev_accum + delta * (value - mu - delta/n)
					stddev = math.sqrt(dev_accum/(n-1))
				# update mu
				mu = mu + delta/n
				yield stddev
		return SimulatedTimeSeries(self.times, __gen())
