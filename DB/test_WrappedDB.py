import unittest
import os
from WrappedDB import WrappedDB
import sys
sys.path.append('../')
from TimeSeries import TimeSeries

# py.test --doctest-modules  --cov --cov-report term-missing WrappedDB.py test_WrappedDB.py

# Test cases for the WrappedDB class

# NOTE: Coverage on WrappedDB is not 100% because lines 36-40 where we re-randomize the keys 
# to ensure we get a unique key is impossible to test. However we know the logic is correct by 
# testing the random key generator function before that.
class WrappedDBTest(unittest.TestCase):

	# Test caching
	# Test encode and decode directly

	def setUp(self):
		self.wdb = WrappedDB('wdb.dbdb', cacheSize=2)
		self.wdb_noCache = WrappedDB('wdb_nocache.dbdb', cacheSize=0)
		self.ts = TimeSeries(values=[1, 3, 0, 1.5, 1], times=[1.5, 2, 2.5, 3, 10.5])
		self.ts_notime = TimeSeries(values=[2, 3, 4], times=None)
		self.ts_single = TimeSeries(values=[-2], times=[1])

	def tearDown(self):
		os.remove('wdb.dbdb')
		os.remove('wdb_nocache.dbdb')
		del self.wdb
		del self.wdb_noCache
		del self.ts
		del self.ts_notime
		del self.ts_single

	# Test store, get size, get time series
	
	def test_storeAndGetWithKey(self):
		key = 1
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts)
		ts_retrieved = self.wdb.getTimeSeries(key)
		self.assertEquals(ts_retrieved.values()[0], 1)

	def test_storeAndGetWithoutKey(self):
		# Key is randomized here
		key = self.wdb.storeKeyAndTimeSeries(timeSeries=self.ts)
		ts_retrieved = self.wdb.getTimeSeries(key)
		self.assertEquals(ts_retrieved.values()[0], 1)

	def test_storeAndGetSize(self):
		key = self.wdb.storeKeyAndTimeSeries(timeSeries=self.ts)
		self.assertEquals(self.wdb.getTimeSeriesSize(key=key), 5)

	def test_storeAndGetWithKeyNoTime(self):
		key = "2"
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts_notime)
		ts_retrieved = self.wdb.getTimeSeries(key)
		self.assertEquals(ts_retrieved.values()[0], 2)

	def test_storeAndGetSizeSingle(self):
		key = 999
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts_single)
		self.assertEquals(self.wdb.getTimeSeriesSize(key=key), 1)

	def test_inputClassIsNotTimeSeries(self):
		with self.assertRaises(ValueError):
			self.wdb.storeKeyAndTimeSeries(timeSeries=[1,2,3])

	def test_keyIsAlreadyInDB(self):
		key = 1
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts)
		with self.assertRaises(ValueError):
			self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)

	# Test cache
	
	def test_cacheNotFull_getOnce(self):
		key = 1
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts)
		# Not get yet, should not cache
		self.assertEquals(self.wdb.cache, {})
		# Get once, should cache it
		self.wdb.getTimeSeries(key)
		self.assertEquals(self.wdb.cache, {'1': self.ts})
		self.assertEquals(self.wdb.keyToCount, {'1': 1})

	def test_cacheNotFull_getMultiple(self):
		self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		# Not get yet, should not cache
		self.assertEquals(self.wdb.cache, {})
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.assertEquals(self.wdb.cache, {'1': self.ts, '2': self.ts_single})
		self.assertEquals(self.wdb.keyToCount, {'1': 2, '2': 1})

	def test_cacheFull(self):
		self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		self.wdb.storeKeyAndTimeSeries(key=3, timeSeries=self.ts_notime)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(2)
		# key 3 should be replaced by 2
		self.assertEquals(self.wdb.cache, {'1': self.ts, '2': self.ts_single})
		self.assertEquals(self.wdb.keyToCount, {'1': 2, '2': 2, '3': 1})

	def test_cacheFullComplex(self):
		self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		self.wdb.storeKeyAndTimeSeries(key=3, timeSeries=self.ts_notime)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(2)
		self.assertEquals(list(self.wdb.cache.keys()), ['3', '2'])
		self.assertEquals(self.wdb.keyToCount, {'1': 2, '2': 3, '3': 3})

	def test_noCache(self):
		self.wdb_noCache.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		self.wdb.storeKeyAndTimeSeries(key=3, timeSeries=self.ts_notime)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(2)
		self.assertEquals(self.wdb_noCache.cache, {})

	# Test encode and decode
	
	


