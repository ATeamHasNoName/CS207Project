import unittest
from pytest import raises
import numpy as np
from timeseries import TimeSeries

class MyTest(unittest.TestCase):

	def test_getitem(self):
		key = 3
		series = TimeSeries(range(1000))
		self.assertEqual(series[key], 3)


suite = unittest.TestLoader().loadTestsFromModule(MyTest())
unittest.TextTestRunner().run(suite)
