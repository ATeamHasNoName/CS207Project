import unittest
from TimeSeries import TimeSeries
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
		
	def tearDown(self):
		os.remove('fsm1.dbdb')

	def test_storeAndGetBasic(self):
		t1 = [1.5, 2, 2.5, 3, 10.5]
		v1 = [1, 3, 0, 1.5, 1]
		ts1 = TimeSeries(values=v1, times=t1)
		key = "1'"
		self.fsm1.store(key, ts1)
		# Retrieve
		ts1_retrieved = self.fsm1.get(key)
		self.assertTrue(type(ts1_retrieved) is TimeSeries)
		# self.assertEqual(self.series[1.5], 1)
		# items = ts1_retrivev
		



# t2 = [2]
# v2 = [3]
# z2 = TimeSeries(values=v2, times=t2)

# db1 = WrappedDB("exampleDB.dbdb")
# db1.storeKeyAndTimeSeries("1", z1)
# db1.storeKeyAndTimeSeries("2", z2)
# print(db1.getTimeSeries("1"))
# print(db1.getTimeSeries("2"))