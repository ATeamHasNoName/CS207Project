import unittest
import numpy as np
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
from test_TimeSeries import TimeSeriesTest
# from MS1.TimeSeries import TimeSeries
# from MS1.ArrayTimeSeries import ArrayTimeSeries
# from MS1.test_TimeSeries import TimeSeriesTest

# py.test --doctest-modules --cov --cov-report term-missing ArrayTimeSeries.py test_ArrayTimeSeries.py

# Test cases for the ArrayTimeSeries class
class ArrayTimeSeriesTest(TimeSeriesTest):

	# Override setUp
	def setUp(self):
		self.singleseries = ArrayTimeSeries(values=[1], times=[1])
		self.series = ArrayTimeSeries(values=[1, 3, 0, -1.5, -1], times=[1.5, 2, 2.5, 10.5, 3])

	# Override setUp
	def tearDown(self):
		del self.singleseries
		del self.series

	'''Override some tests to increase coverage'''

	def test_add(self):
		_s1 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 + _s2, ArrayTimeSeries(values=[2,4,6], times=[0,5,10]))

	def test_add_constant(self):
		_s1 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 + 5.2, ArrayTimeSeries(values=[6.2,7.2,8.2], times=[0,5,10]))

	def test_sub(self):
		_s1 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 - _s2, ArrayTimeSeries(values=[0,0,0], times=[0,5,10]))

	def test_sub_constant(self):
		_s1 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 - 3, ArrayTimeSeries(values=[-2,-1,0], times=[0,5,10]))

	def test_mul(self):
		_s1 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 * _s2, ArrayTimeSeries(values=[1,4,9], times=[0,5,10]))

	def test_mul_constant(self):
		_s1 = ArrayTimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 * 0, ArrayTimeSeries(values=[0,0,0], times=[0,5,10]))

	def test_interpolate_single1(self):
		a = ArrayTimeSeries(values=[1, 2, 3],times=[0, 5, 10])
		b = ArrayTimeSeries(values=[100, -100],times=[2.5, 7.5])
		self.assertEqual(a.interpolate([1]), ArrayTimeSeries(values=[1.2],times=[1]))

	def test_interpolate_single2(self):
		a = ArrayTimeSeries(values=[1, 2, 3],times=[0, 5, 10])
		b = ArrayTimeSeries(values=[100, -100],times=[2.5, 7.5])
		self.assertEqual(a.interpolate(list(b.itertimes())), ArrayTimeSeries(values=[1.5, 2.5], times=[2.5,7.5]) )

	def test_interpolate_boundary(self):
		a = ArrayTimeSeries(values=[1, 2, 3],times=[0, 5, 10])
		b = ArrayTimeSeries(values=[100, -100],times=[2.5, 7.5])
		self.assertEqual(a.interpolate([-100, 100]), ArrayTimeSeries(values=[1,3],times=[-100,100]))

	'''Override some tests to prevent crashes'''

	def test_values(self):
		self.assertEqual(self.series.values().tolist(), [1, 3, 0, -1, -1.5])

	def test_times(self):
		self.assertEqual(self.series.times().tolist(), [1.5, 2, 2.5, 3, 10.5])

	def test_str(self):
		self.assertEqual(str(self.series), 'ArrayTimeSeries\nLength: 5\nFirst (oldest): 1.0, Last (newest): -1.5')

	def test_repr(self):
		self.assertEqual(repr(self.series), "ArrayTimeSeries([(1.5, 1.0), (2.0, 3.0), (2.5, 0.0), (3.0, -1.0), (10.5, -1.5)])")

	def test_items(self):
		self.assertEqual(self.series.items().tolist(), [[1.5, 1], [2, 3], [2.5, 0], [3, -1], [10.5, -1.5]])

	def test_iteritems(self):
		ind = 0
		for tv in self.series.iteritems():
			self.assertEqual(tv[0], self.series.items().tolist()[ind][0])
			self.assertEqual(tv[1], self.series.items().tolist()[ind][1])
			ind = ind + 1
