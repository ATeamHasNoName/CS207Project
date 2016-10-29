import pytest
import types
import numpy as np
from timeseries import TimeSeries

def test_init():
	t = [1, 3, 4.5, 6, 9]
	v = [0, 4, 1, 1.5, 2]
	z = TimeSeries(t,v)
	assert z[4.5] == 1.5
	assert z[1] != 1
	z[1.5] = 2.5
	assert a[1.5] == 2.5
	print("hi")

def test_len():
	t = [1, 3, 4.5, 6, 9]
	v = [0, 4, 1, 1.5, 2]
	a = TimeSeries(t, v)
    assert len(a) == 5
    a = TimeSeries([], [])
    assert len(a) == 0

def test_iters():

    t = [1, 1.5, 2, 2.5, 10]
    v = [0, 2, -1, 0.5, 0]
    a = TimeSeries(t, v)

    assert list(a.times()) == t
    assert list(a.values()) == v



