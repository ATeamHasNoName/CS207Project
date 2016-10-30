import unittest
import numpy as np
from TimeSeries import TimeSeries

# Test cases for the TimeSeries class
class TimeSeriesTest(unittest.TestCase):

	def setUp(self):
		self.series = TimeSeries(values=[1, 3, 0, -1.5, -1], times=[1.5, 2, 2.5, 3, 10.5])
		self.series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])

	def tearDown(self):
		del self.series
		del self.series_notime

	def test_init_with_time(self):
		self.assertEqual(self.series[1.5], 1)

	def test_init_without_time(self):
		self.assertEqual(self.series_notime[0], 1)		

	def test_init_withduptime(self):
		with self.assertRaises(AssertionError):
			TimeSeries(values=[1, 3, 0, -1.5, -1, 1], times=[1.5, 2, 2.5, 3, 10.5, 10.5])

	def test_init_withunequallengths(self):
		with self.assertRaises(AssertionError):
			TimeSeries(values=[1], times=[1.5, 2, 2.5, 3, 10.5, 10.5])

	def test_init_withnonnumber(self):
		with self.assertRaises(AssertionError):
			TimeSeries(values=[1, 3, 0, -1.5, -1, 1], times=[1.5, 2, 2.5, 3, 10.5, "hi"])

	def test_init_without_time_withnonnumber(self):
		with self.assertRaises(AssertionError):
			TimeSeries(values=[1, 3, 0, -1.5, "haha", 1])



