import unittest
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
from SMTimeSeries import SMTimeSeries
import sys
import os
sys.path.append('./DB/')
from WrappedDB import WrappedDB

# py.test --doctest-modules  --cov --cov-report term-missing SMTimeSeries.py test_SMTimeSeries.py

# Test cases for the SMTimeSeries class
class SMTimeSeriesTest(unittest.TestCase):

	def setUp(self):
		self.values=[1, 3, 0, 1.5, 1]
		self.times=[1, 2, 4, 5, 10]
		self.key = "313"
		self.dbname = "SM_DB.dbdb"
		self.DB = WrappedDB(self.dbname)
		self.ts1 = TimeSeries(self.values, self.times)
		self.ts2 = TimeSeries([1, 2, 3],[0, 5, 10])
		self.smt1 = SMTimeSeries(self.values, self.times, self.key)
		self.smt2 = SMTimeSeries([0, 5, 10], [1, 2, 3], "7")
		
	def tearDown(self):
		del self.values
		del self.times
		del self.key
		del self.DB
		del self.ts1
		del self.ts2
		del self.smt1
		del self.smt2
		os.remove(self.dbname)

	# Note that these tests are run in sequential order

	def test_init_SMTimeSeries(self):
		self.assertTrue(type(self.smt1) is SMTimeSeries)

	def test_from_db_with_key(self):
		self.DB.storeKeyAndTimeSeries(key = self.key, timeSeries = self.ts1)
		timeSeriesFromDB = self.smt1.from_db(self.key, self.dbname)
		# Check if the fetched SMTimeSeries is the same class as was instantiated:
		self.assertTrue(timeSeriesFromDB == self.ts1)		

	def test_from_db_without_key(self):
		self.DB.storeKeyAndTimeSeries(key = self.key, timeSeries = self.ts1)
		timeSeriesFromDB = self.smt1.from_db(None, self.dbname)
		# Check if the fetched SMTimeSeries is the same class as was instantiated:
		self.assertRaises(Exception,"Key is not in Database\n")

	"""
	Tests for the delegation methods:
	"""
	def test_getitem(self):
		self.assertEqual(self.smt1[2], 3)

	def test_iter(self):
		index = 0
		for v in self.smt1:
			self.assertEqual(v, self.ts1[self.times[index]])
			index += 1

	def test_len(self):
		self.assertEqual(len(self.smt1), 5)

	def test_setitem(self):
		# Change value at time 1 to 3:
		self.smt1[1] = 3
		self.assertEqual(self.smt1[1], 3)

	def test_items(self):
		self.assertEqual(self.ts1.items(), self.smt1.items())

	def test_iteritems(self):
		# Get iteritems from timeseries:
		tsList = []

		for ts in self.ts1.iteritems():
			tsList.append(ts)

		index = 0
		for v in self.smt1.iteritems():
			self.assertEqual(v, tsList[index])
			index += 1

	def test_itertimes(self):
		tsList = []

		for a in self.ts1.itertimes():
			tsList.append(a)

		index = 0
		for v in self.smt1.itertimes():
			self.assertEqual(v, tsList[index])
			index += 1

	def test_itervalues(self):
		tsList = []

		for a in self.ts1.itervalues():
			tsList.append(a)

		index = 0
		for v in self.smt1.itervalues():
			self.assertEqual(v, tsList[index])
			index += 1

	def test_mean(self):
		self.assertEqual(self.smt2.mean(), 5.0)

	def test_std(self):
		self.assertEqual(self.smt2.std(), 4.0824829046386304)

	def test_times(self):
		self.assertEqual(self.smt1.times(), [1, 2, 4, 5, 10])

	def test_values(self):
		self.assertEqual(self.smt1.values(), [1, 3, 0, 1.5, 1])
