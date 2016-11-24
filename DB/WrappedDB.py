from DB import DB
import sys
sys.path.append('../')
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from TimeSeries import TimeSeries

# READ: Setup for DB
# Download the .zip for portalocker here: https://github.com/WoLpH/portalocker and store it anywhere
# Run python setup.py install

class WrappedDB:

	def __init__(self, filename):
		self.db = DB.connect(filename)
		
		# Stores the highest key in the database:
		self.highestKey = 0


	# Stores a time series by key in the DB
	def storeKeyAndTimeSeries(self, key, timeSeries):
		if not isinstance(timeSeries, SizedContainerTimeSeriesInterface):
			raise ValueError('Input class is not time series')

		# If no key is set then the key is automatically set one number above the highest
		# current key in the database:
		if (key == None):
			self.highestKey += 1
			key = self.highestKey

		elif (key > self.highestKey):
			self.highestKey = key
		else:
			if (self.getTimeSeriesSize(key) != -1):
				# Key is in database. Use highestKey + 1
				self.highestKey += 1
				key = self.higestKey

		self.db.set(str(key), self._encode(timeSeries))
		self._storeKeyAndTimeSeriesSize(str(key), timeSeries)
		self.db.commit()


	# Also stores time series' size in the DB
	def _storeKeyAndTimeSeriesSize(self, key, timeSeries):
		if not isinstance(timeSeries, SizedContainerTimeSeriesInterface):
			raise ValueError('Input class is not time series')
		# Note that it is not committed here, and must be committed in the caller function
		self.db.set(str(key) + ':size', str(len(timeSeries)))

	# Get the size of the time series' from its key
	# Returns -1 when time series key does not exist
	def getTimeSeriesSize(self, key):
		try:
			size = self.db.get(str(key) + ':size')
		except KeyError:
			return -1
		return int(self.db.get(str(key) + ':size'))

	# Gets a time series object by key from the DB
	# Returns None when time series key does not exist
	def getTimeSeries(self, key):
		try:
			timeSeriesString = self.db.get(str(key))
		except KeyError:
			return None
		return self._decode(self.db.get(str(key)))

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
