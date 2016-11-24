import unittest
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
from FileStorageManager import FileStorageManager
import sys
import os
sys.path.append('./DB/')
from WrappedDB import WrappedDB

# py.test --doctest-modules  --cov --cov-report term-missing FileStorageManager.py test_FileStorageManager.py

# Test cases for the FileStoreManager class
class FileStorageManagerTest(unittest.TestCase):

	def setUp(self):
		self.fsm1 = FileStorageManager('fsm1.dbdb')
		self.ts = TimeSeries(values=[1, 3, 0, 1.5, 1], times=[1.5, 2, 2.5, 3, 10.5])
		self.ts_notime = TimeSeries(values=[2, 3, 4], times=None)
		self.ts_single = TimeSeries(values=[-2], times=[1])
		self.ats = ArrayTimeSeries(values=[1,2,3], times=[4,5,6])
		
	def tearDown(self):
		os.remove('fsm1.dbdb')
		del self.fsm1
		del self.ts
		del self.ts_notime
		del self.ts_single
		del self.ats

	# Note that these tests are run in sequential order
	
	def test_RetrievedObjectIsTimeSeriesClass(self):
		key = "1"
		self.fsm1.store(key, self.ts)
		ts_retrieved = self.fsm1.get(key)
		# Retrieved time series is the right class
		self.assertTrue(type(ts_retrieved) is TimeSeries)

	def test_intKeyAndGet(self):
		key = 123
		self.fsm1.store(key, self.ts)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], 1)

	def test_intKeyAndSetOver(self):
		key = 123
		self.fsm1.store(key, self.ts_single)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], -2)

	def test_noTime(self):
		key = "5"
		self.fsm1.store(key, self.ts_notime)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], 2)

	def test_negativeKeyAndArrayTimeSeries(self):
		key = -3
		self.fsm1.store(key, self.ats)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], 1)

	def test_getNonExistentTimeSeries(self):
		key = "191919"
		self.assertEqual(self.fsm1.get(key), None)

	

# t2 = [2]
# v2 = [3]
# z2 = TimeSeries(values=v2, times=t2)

# db1 = WrappedDB("exampleDB.dbdb")
# db1.storeKeyAndTimeSeries("1", z1)
# db1.storeKeyAndTimeSeries("2", z2)
# print(db1.getTimeSeries("1"))
# print(db1.getTimeSeries("2"))