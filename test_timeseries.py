mport unittest
from pytest import raises
import numpy as np
from timeseries import TimeSeries

class MyTest(unittest.TestCase):

	def length(self):
		length = len(TimeSeries(range(1000)))
		self.assertEqual(length, 1000)




suite = unittest.TestLoader().loadTestsFromModule(MyTest())
unittest.TextTestRunner().run(suite)