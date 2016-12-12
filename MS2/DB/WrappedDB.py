from DB import DB
import time
import random
import os
import sys
import operator

try:
	sys.path.append('../MS1/'); 
	from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
	from TimeSeries import TimeSeries
	from ArrayTimeSeries import ArrayTimeSeries
except ImportError:
	sys.path.append('../../MS1/'); from WrappedDB import *
	from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
	from TimeSeries import TimeSeries
	from ArrayTimeSeries import ArrayTimeSeries

# READ: Setup for DB
# Download the .zip for portalocker here: https://github.com/WoLpH/portalocker and store it anywhere
# Run python setup.py install

class WrappedDB:
	"""
	Wraps the DB.py file which contains lab 10 code.
	"""

	def __init__(self, cacheSize=10):
		"""
		Initializes a WrappedDB instance with a filename and cache size to store entries to disk.

		Parameters
		----------
		cacheSize: The number of time series to cache. If set to 0, no caching will be implemented.

		Returns
		-------
		None
		
		>>> wdb = WrappedDB(cacheSize=5)
		>>> type(wdb)
		<class 'WrappedDB.WrappedDB'>
		"""
		# These variables are used for caching
		self.cacheSize = cacheSize
		self.cache = {} # key to TimeSeries dictionary cache
		self.keyToCount = {} # key to number of times TimeSeries has been retrieved

	def _fileNameForKey(self, key):
		"""
		Private helper function that takes in a key and outputs the filename for this key.
		"""
		return "ts_" + str(key) + ".dbdb"

	# Stores a time series by key in the DB
	# Returns the key after storing
	def storeKeyAndTimeSeries(self, timeSeries, key=None):
		"""
		Stores an instance of SizedContainerTimeSeriesInterface using a string or int key.
		If no key is provided it randomly generates a key in the following fashion: TimeStamp+randomNumberBetween0-999. 
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface, or None
		timeSeries: Concrete class of SizedContainerTimeSeriesInterface
		
		Returns
		-------
		key: String of either the input key or our randomly generated key
		
		Notes
		-----
		PRE:
			- timeSeries has to be a valid SizedContainerTimeSeriesInterface concrete class
			
		>>> wdb = WrappedDB(cacheSize=5)
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> key = wdb.storeKeyAndTimeSeries(ts)
		>>> wdb.getTimeSeriesSize(key)
		5
		>>> os.remove('ts_' + str(key) + '.dbdb')
		"""
		if not isinstance(timeSeries, SizedContainerTimeSeriesInterface):
			raise ValueError('Input class is not time series')
		if (key is None):
			# Generate our own key which is current time stamp and a random number from 0 to 999
			key = "{0}-{1}".format(str(time.time())[:10], random.randint(0,999))
			# Check if the autogenerated key was already in the database:
			if (self.getTimeSeriesSize(key) != -1):
				# Generate random keys until we find a key that is not in the database:
				while (true):
					key = "{0}-{1}".format(str(time.time())[:10], random.randint(0,999))
					if (self.getTimeSeriesSize(key == -1)):
						# Unique key found:
							break

		elif (self.getTimeSeriesSize(str(key)) != -1):
			# The key user chose is already in the database. Return Error
			raise ValueError("Key is already in Database")
		else:
			key = str(key)
			
		# Create a new file from the key
		filename = self._fileNameForKey(key)
		newDB = DB.connect(filename)
		newDB.set("timeseries", self._encode(timeSeries))
		newDB.set("size", str(len(timeSeries)))
		newDB.commit()
		return key

	# Get the size of the time series' from its key
	# Returns -1 when time series key does not exist
	def getTimeSeriesSize(self, key):
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
			
		>>> wdb = WrappedDB()
		>>> wdb.getTimeSeriesSize("2")
		-1
		"""

		# Read the file from this key
		filename = self._fileNameForKey(key)
		existingDB = DB.connect(filename)
		try:
			size = existingDB.get("size")
		except KeyError:
			# Timeseries does not exist, delete the filename
			os.remove(filename)
			return - 1
		return int(existingDB.get("size"))

	"""
	Logic for our cache:
	- We cache our top k time series that are accessed (get) the most.
	- We store keyToCounts and cache dicts in memory.
	- Whenever a user calls getTimeSeries, we increment the keyToCounts for that key, 
	and update the cache if this time series being called has now been called more 
	than the least called time series in the cache.
	"""

	def _keyIsInTopCached(self, key):
		"""
		Helper function that returns true if key is in top k cached counts
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface
		
		Returns
		-------
		True if key is in top k cached counts, False otherwise
		"""
		topk_keys = sorted(self.keyToCount, key=self.keyToCount.get, reverse=True)[:self.cacheSize]
		# Also make sure that the key is ACTUALLY in the cache
		return (key in topk_keys) and (key in self.cache)

	def _refreshCache(self, key, timeSeries):
		"""
		Adds time series to the cache, and replace timeseries in the cache if necessary according 
		to logic stated above.
		
		Parameters
		----------
		key: String or int of the key index of the SizedContainerTimeSeriesInterface
		timeSeries: Concrete class of SizedContainerTimeSeriesInterface
		
		Returns
		-------
		None
		"""
		topk_keys = sorted(self.keyToCount, key=self.keyToCount.get, reverse=True)[:self.cacheSize]
		currentKeyCount = self.keyToCount[key] + 1 if key in self.keyToCount else 1
		self.keyToCount[key] = currentKeyCount

		if len(topk_keys) < self.cacheSize:
			# There are less keys in cache than cache size, just store
			self.cache[key] = timeSeries
			return
		
		# Find all the counts in cache, and get the min one
		minKey = ''
		minCount = sys.maxsize
		for k in self.cache:
			if self.keyToCount[k] < minCount:
				minCount = self.keyToCount[k]
				minKey = k

		# Check if the min key's count is less than currentKeyCount
		if currentKeyCount > minCount and not key in self.cache: 
			# Replace the minkey
			del self.cache[minKey]
			self.cache[key] = timeSeries

	# Gets a time series object by key from the DB
	# Returns None when time series key does not exist
	def getTimeSeries(self, key):
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
			
		>>> wdb = WrappedDB()
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> key = wdb.storeKeyAndTimeSeries(key="1", timeSeries=ts)
		>>> wdb.getTimeSeries("1").values()
		[0.0, 2.0, -1.0, 0.5, 0.0]
		>>> os.remove('ts_1.dbdb')
		"""
		key = str(key)

		timeSeries = None
		# First check if time series at this key is cached
		if self._keyIsInTopCached(key):
			# Get from cache
			timeSeries = self.cache[key]
			self._refreshCache(key, timeSeries)
			return timeSeries

		# Grab the file as it is not in cache
		filename = self._fileNameForKey(key)
		try:
			existingDB = DB.connect(filename)
			timeSeriesString = existingDB.get("timeseries")
		except KeyError:
			os.remove(filename)
			return None

		timeSeries = self._decode(timeSeriesString)
		self._refreshCache(key, timeSeries)
		return timeSeries

	def _encode(self, timeSeries):
		"""
		Takes in time series object and transforms it into a string.
		
		Parameters
		----------
		timeSeries: Concrete class of SizedContainerTimeSeriesInterface
		
		Returns
		-------
		String representation of time series object, where each time and value is encoded in 
		"(t,v)" and separated with ";"

		>>> wdb = WrappedDB()
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> wdb._encode(ts)
		'(1,0);(1.5,2);(2,-1);(2.5,0.5);(10,0)'
		"""
		items = timeSeries.items()
		encodedTimeSeries = []
		for (time, value) in items:
			encodedTimeSeries.append("(" + str(time) + "," + str(value) + ")")
		return ';'.join(encodedTimeSeries)

	# Takes in encoded time series and transforms it into a TimeSeries object
	# Raise ValueError whenever improper
	def _decode(self, encodedTimeSeries):
		"""
		Takes in time series string and transforms it into a time series object.
		Raises ValueError when the input string is malformed.
		
		Parameters
		----------
		String representation of time series object, where each time and value is encoded in 
		"(t,v)" and separated with ";"
		
		Returns
		-------
		timeSeries: TimeSeries class

		>>> wdb = WrappedDB()
		>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
		>>> encodedString = wdb._encode(ts)
		>>> wdb._decode(encodedString)
		TimeSeries([(1.0, 0.0), (1.5, 2.0), (2.0, -1.0), (2.5, 0.5), (10.0, 0.0)])
		"""
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

		z = TimeSeries(values=v, times=t)
		return z
