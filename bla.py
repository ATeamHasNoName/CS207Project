import unittest
import numpy as np
from TimeSeries import TimeSeries
from lazy import *

# py.test --cov --cov-report term-missing TimeSeries.py test_TimeSeries.py

# Test cases for the TimeSeries class
class TimeSeriesTest(unittest.TestCase):

	def setUp(self):
		self.singleseries = TimeSeries(values=[1], times=[1])
		self.series = TimeSeries(values=[1, 3, 0, -1.5, -1], times=[1.5, 2, 2.5, 10.5, 3])
		
	def tearDown(self):
		del self.singleseries
		del self.series

	def test_lazy_equal(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = a.lazy
		self.assertTrue(a == b.eval())

	def test_lazy_not_equal(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([1, 2, 4],[0, 5, 10])
		c = b.lazy
		self.assertFalse(a == c.eval())

	def test_lazyAdd(self):
		thunk = lazy_mul(1,2)
		self.assertTrue(thunk.eval() == 2)

	def test_lazy_len(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = a.lazy
		print(b)
		length = len(b)
		self.assertTrue(length == 2)

	def test_lazy_instance(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		self.assertTrue(isinstance(a.lazy.eval(), TimeSeries)==True)
