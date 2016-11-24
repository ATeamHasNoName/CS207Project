from DB import DB
import sys
sys.path.append('../')
from TimeSeries import TimeSeries

# READ: Setup for DB
# Download the .zip for portalocker here: https://github.com/WoLpH/portalocker and store it anywhere
# Run python setup.py install

class WrappedDB:

	def __init__(self, filename):
		self.db = DB.connect(filename)

	# Stores a (key, value) pair in the DB
	# Note that value must be a primitive data type
	def storeKeyAndValue(self, key, value):
		self.db.set(key, value)
		self.db.commit()

	# Gets a value by key from the DB
	def getValue(self, key):
		return self.db.get(key)

	# Stores a time series by key in the DB
	def storeKeyAndTimeSeries(self, key, timeSeries):
		if type(timeSeries) is not TimeSeries:
			raise ValueError('Input class is not time series')
		self.db.set(key, self._encode(timeSeries))
		self._storeKeyAndTimeSeriesSize(key, timeSeries)
		self.db.commit()

	# Also stores time series' size in the DB
	def _storeKeyAndTimeSeriesSize(self, key, timeSeries):
		if type(timeSeries) is not TimeSeries:
			raise ValueError('Input class is not time series')
		# Note that it is not committed here, and must be committed in the caller function
		self.db.set(key + ':size', len(timeSeries))

	# Get the size of the time series' from its key
	def getTimeSeriesSize(self, key):
		return int(self.db.get(key + ':size'))

	# Gets a time series object by key from the DB
	def getTimeSeries(self, key):
		return self._decode(self.db.get(key))

	# Takes in time series object and transforms it into a string
	def _encode(self, timeSeries):
		items = timeSeries.items()
		encodedTimeSeries = []
		for (time, value) in items:
			encodedTimeSeries.append("(" + str(time) + "," + str(value) + ")")
		return ';'.join(encodedTimeSeries)

	# Takes in encoded time series and transforms it into a TimeSeries object
	# Raise ValueError whenever improper
	def _decode(self, encodedTimeSeries):
		itemStrings = encodedTimeSeries.split(';')
		t = []
		v = []
		for itemString in itemStrings:
			timeValuePair = itemString.split(',')

			if len(timeValuePair) != 2:
				raise ValueError('Time series string is malformed')

			time = timeValuePair[0]
			value = timeValuePair[1]
			if len(time) < 2 or len(value) < 2:
				raise ValueError('Time series string is malformed')			
			
			time = time[1:]
			value = value[:-1]

			# This might throw ValueError if time and value could not be converted to floats
			t.append(float(time))
			v.append(float(value))

		if len(v) == 0 or len(t) == 0:
			raise ValueError('Empty time series passed in')

		z = TimeSeries(values=v, times=t)
		return z