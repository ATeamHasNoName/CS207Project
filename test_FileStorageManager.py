import unittest
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
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
		self.fsm1.store(timeSeries=self.ts, key=key)
		ts_retrieved = self.fsm1.get(key)
		self.assertTrue(isinstance(ts_retrieved, SizedContainerTimeSeriesInterface))

	def test_intKeyAndGet(self):
		key = 123
		self.fsm1.store(timeSeries=self.ts, key=key)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], 1)

	def test_intKeyAndSetOver(self):
		key = 123
		self.fsm1.store(timeSeries=self.ts_single, key=key)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], -2)

	def test_noTime(self):
		key = "5"
		self.fsm1.store(timeSeries=self.ts_notime, key=key)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], 2)

	def test_negativeKeyAndArrayTimeSeries(self):
		key = -3
		self.fsm1.store(timeSeries=self.ats, key=key)
		ts_retrieved = self.fsm1.get(key)
		values = ts_retrieved.values()
		self.assertEqual(values[0], 1)

	def test_getNonExistentTimeSeries(self):
		key = "191919"
		self.assertEqual(self.fsm1.get(key), None)

	def test_timeSeriesSize(self):
		key = "1"
		self.fsm1.store(timeSeries=self.ts, key=key)
		self.assertEqual(self.fsm1.size(key), 5)

	def test_noTimeSize(self):
		key = "1"
		self.fsm1.store(timeSeries=self.ts_notime, key=key)
		self.assertEqual(self.fsm1.size(key), 3)

	def test_singleSize(self):
		key = "1"
		self.fsm1.store(timeSeries=self.ts_single, key=key)
		self.assertEqual(self.fsm1.size(key), 1)

	def test_atsSize(self):
		key = "1"
		self.fsm1.store(timeSeries=self.ats, key=key)
		self.assertEqual( self.fsm1.size(key), 3)

	def test_getNonExistentSize(self):
		key = 1919
		self.assertEqual(self.fsm1.size(key), -1)
