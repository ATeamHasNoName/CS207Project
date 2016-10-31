import unittest
import numpy as np
from TimeSeries import TimeSeries

# Test cases for the TimeSeries class
# py.test --cov --cov-report term-missing TimeSeries.py test_TimeSeries.py

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

	

########## Interpolation ##########
	def test_interpolate_single1(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([100, -100],[2.5, 7.5])
		self.assertEqual(a.interpolate([1]), TimeSeries([1.2],[1]) )
		#self.assertEqual(a.interpolate([-100, 100]),TimeSeries([-100,100],[1,3]))


	def test_interpolate_single2(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([100, -100],[2.5, 7.5])
		self.assertEqual(a.interpolate(list(b.itertimes())), TimeSeries([1.5, 2.5], [2.5,7.5]) )

	def test_interpolate_boundary(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([100, -100],[2.5, 7.5])
		self.assertEqual(a.interpolate([-100, 100]),TimeSeries([1,3],[-100,100]))








