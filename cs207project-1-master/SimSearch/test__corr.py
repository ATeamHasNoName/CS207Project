import sys
import os
import numpy as np
import random
import _corr
import unittest
from scipy.stats import norm
#from Distance_from_known_ts import tsmaker

class yihang(unittest.TestCase):

	def setUp(self):
		self.yihang = 1

	def tearDown(self):
		del self.yihang

	def test_dummy(self):
		print("Yihang")
		self.assertEqual(1,2)
		#standts1 = stand(tsmaker(0.5, 0.1, random.uniform(0,10))
	    #standts1 = stand(t1)
	    #standts2 = stand(t2)
		#assertEquals(np.round(standts1.mean(), 10), 0.0)
		#assertEquals(np.round(standts1.std(), 10), 1.0)

	    #idx, mcorr = max_corr_at_phase(standts1, standts2)
	    #assert idx == 2
	    #assert np.round(mcorr, 4) == 0.5207

	    #sumcorr = kernel_corr(standts1, standts2, mult=10)
	    #assert np.round(sumcorr, 4) == 0.0125






