import unittest
import os
from DB import *
import sys
sys.path.append('../')
from TimeSeries import TimeSeries

# py.test --doctest-modules  --cov --cov-report term-missing DB.py test_DB.py

# Test cases for the DB class

class DBTest(unittest.TestCase):

	# Test caching
	# Test encode and decode directly

	def setUp(self):
		dbname = 'binarytreetest.dbdb'
		try:
			f = open(dbname, 'r+b')
		except IOError:
			fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
			f = os.fdopen(fd, 'r+b')

		self.storage = Storage(f)

		self.ts = TimeSeries(values=[1, 3, 0, 1.5, 1], times=[1.5, 2, 2.5, 3, 10.5])
		self.ts_notime = TimeSeries(values=[2, 3, 4], times=None)
		self.ts_single = TimeSeries(values=[-2], times=[1])

	def tearDown(self):
		del self.storage
		del self.ts
		del self.ts_notime
		del self.ts_single

	# Test store, get size, get time series
	
	def test_storeAndGetWithKey(self):
		btree = BinaryTree(self.storage)
		btree.set(2, "99")
		btree.set(4, "101")
		btree.set(1, "98")
		btree.set(3, "100")
		btree.set(5, "102")
		btree.set(6, "103")
		btree.set(7, "104")
		btree.set(8, "105")
		print(type(btree._tree_ref))
		self.assertTrue(isinstance(btree, BinaryTree))

"""
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
		self.assertEquals(sorted(list(self.wdb.cache.keys())), ['2', '3'])
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

	def test_encode(self):
		timeSeriesString = self.wdb._encode(timeSeries=self.ts)
		self.assertEqual(timeSeriesString, '(1.5,1);(2,3);(2.5,0);(3,1.5);(10.5,1)')

	def test_decode(self):
		timeSeriesString = '(1.5,1);(2,3);(2.5,0);(3,1.5);(10.5,1)'
		timeSeries = self.wdb._decode(encodedTimeSeries=timeSeriesString)
		self.assertEqual(timeSeries, self.ts)

	def test_decode_malformed1(self):
		timeSeriesString = '(1.51);(2,3);(2.5,0);(3,1.5);(10.5,1)'
		with self.assertRaises(ValueError):
			timeSeries = self.wdb._decode(encodedTimeSeries=timeSeriesString)

	def test_decode_malformed2(self):
		timeSeriesString = '(1.5,1;(2,3);(2.5,0);(3,1.5);(10.5,1)'
		with self.assertRaises(ValueError):
			timeSeries = self.wdb._decode(encodedTimeSeries=timeSeriesString)

"""
