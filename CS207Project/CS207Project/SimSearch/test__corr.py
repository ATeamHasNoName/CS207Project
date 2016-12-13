import sys
import os
import numpy as np
import random
from _corr import *
import unittest
from scipy.stats import norm
#from Distance_from_known_ts import tsmaker

def test_stand():
	ts1 = stand(tsmaker(0.5, 0.1, random.uniform(0,10)))
	ts2 = stand(tsmaker(1, 0.5, random.uniform(0,10)))
	assert(round(ts1.std()) == 1)
	assert(round(ts2.mean()) == 0)

def test_kernel_corr():
	ts1 = stand(tsmaker(0.5, 0.1, random.uniform(0,10)))
	ts2 = stand(tsmaker(1, 0.5, random.uniform(0,10)))
	assert(kernel_corr(ts2, ts2) == 1)


def test_kernel_dist():
	ts1 = stand(tsmaker(0.5, 0.1, random.uniform(0,10)))
	ts2 = stand(tsmaker(1, 0.5, random.uniform(0,10)))
	assert(kernel_dist(ts1, ts1) == 0)










