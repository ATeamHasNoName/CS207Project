from pytest import raises
from simulatedtimeseries import SimulatedTimeSeries
import numpy as np

def test_chunk_out_of_range():
	with raises(IndexError):
		t = iter(range(1,11))
		v = iter([2*x + 1 for x in range(1,11)])
		sts = SimulatedTimeSeries(t, v)
		sts.produce(15) == [(1,3), (2,5), (3,7)]

def test_online_mean():
	times_gen = (t for t in [1,2,3,4])
	values_gen = (v for v in [10,20,30,40])
	ts = SimulatedTimeSeries(times_gen, values_gen)
	ts_mean = ts.online_mean()
	assert ts_mean.produce(chunk=3)==[(1,10),(2,15),(3,20)]
	assert ts_mean.produce(chunk=1)==[(4,25)]

def test_online_std():
	times_gen = (t for t in [1,2,3,4])
	values_gen = (v for v in [10,20,30,40])
	ts = SimulatedTimeSeries(times_gen, values_gen)
	ts_std = ts.online_std()
	assert ts_std.produce(chunk=3)==[(1,0),(2,np.std([10,20],ddof=1)),(3,np.std([10,20,30],ddof=1))]
	assert ts_std.produce(chunk=1)==[(4,np.std([10,20,30,40],ddof=1))]
