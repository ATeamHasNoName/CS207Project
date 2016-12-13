import operator
from pytest import raises
import numpy as np
from lazy import lazy
from lazy import LazyOperation
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries
from simulatedtimeseries import SimulatedTimeSeries
from smtimeseries import SMTimeSeries
import os, glob

def test_sized_container_timeseries():
	"""
	Wrapper function that calls unit-tests defined below on both sized-container-based
	time series classes (TimeSeries and ArrayTimeSeries)
	"""
	for class_name in [TimeSeries, ArrayTimeSeries, SMTimeSeries]:
		correct_length(class_name)
		incompatible_dimensions(class_name)
		index_in_time_series(class_name)
		index_not_in_time_series(class_name)
		interpolate_ts(class_name)
		iterable(class_name)
		method_abs(class_name)
		method_add_int(class_name)
		method_add_two_timeseries(class_name)
		method_bool(class_name)
		method_check_length_helper(class_name)
		method_check_time_domains_helper(class_name)
		method_contains(class_name)
		method_eq(class_name)
		method_getitem(class_name)
		method_items(class_name)
		method_iter(class_name)
		method_iteritems(class_name)
		method_itertimes(class_name)
		method_itervalues(class_name)
		method_len(class_name)
		method_mean(class_name)
		method_mul_int(class_name)
		method_mul_two_timeseries(class_name)
		method_ne(class_name)
		method_neg(class_name)
		method_pos(class_name)
		method_produce()
		method_repr(class_name)
		method_setitem(class_name)
		method_std(class_name)
		method_str(class_name)
		method_sub_int(class_name)
		method_sub_two_timeseries(class_name)
		method_times(class_name)
		method_times_lst(class_name)
		method_values(class_name)
		non_iterable(class_name)
		operator_list_nparray_not_allowed(class_name)
		times_contains_repeats(class_name)
		remove_test_files()

def test_time_series():
	"""Calls tests on list-based timeseries class exclusively"""
	threes_fives(TimeSeries)
	verify_lazy_property_time_series(TimeSeries)
	verify_lazyfied_time_series_check_length(TimeSeries)

def test_sm_time_series():
	"""Calls tests on smtimeseries class exclusively"""
	test_smtimeseries()
	test_from_db()
	remove_test_files()

##############################################################################
## Unit Tests
##############################################################################

def threes_fives(class_name):
	"""
	Check with fizbuzz data
	projecteuler.net/problem=1
	Note: this is decidely *not* the intended purpose of this class.
	"""
	threes = class_name(values=range(0, 1000, 3))
	fives = class_name(values=range(0, 1000, 5))

	s = 0
	for i in range(0, 1000):
		if i in threes or i in fives:
			s += i

	assert s == 233168


def non_iterable(class_name):
	"""
	Confirms we get a type error when we try
	to create time series with non-iterable.
	"""
	with raises(TypeError):
		_ = class_name(values=42, times=42)


def iterable(class_name):
	"""
	Confirms we *don't get a type error when we try
	to create time series with various iterables.
	"""
	class_name(values=[1, 2, 3], times=[1,2,3])
	class_name(values={'a': 1, 'b': 2, 'c': 3}, times=[1,2,3])
	class_name(values=set([1, 2, 3]), times=[1,2,3])


def incompatible_dimensions(class_name):
	"""
	Confirm that we get a value error when times
	is not the same length as initial data.
	"""
	with raises(ValueError):
		class_name(values=[1] * 100, times=range(200))


def times_contains_repeats(class_name):
	"""
	Confirm that we get a value error when times
	contains repeated values.
	"""
	with raises(ValueError):
		class_name(values=[1, 2, 3, 4], times=[1, 2, 2, 3])

	with raises(ValueError):
		class_name(values=[1]*100, times=list(range(100))+[99])

def index_in_time_series(class_name):
	"""Confirm that get_item and set_item work as expected"""
	ts = class_name(values=[1,2,3], times=[1,2,3])
	assert ts[2] == 3
	ts[2] = 10
	assert ts[2] == 10


def index_not_in_time_series(class_name):
	"""
	Confirm that we get a value error when we
	attempt to access or set an non-existing value
	"""
	ts = class_name(values=[1,2,3], times=[1,2,3])

	with raises(IndexError):
		_ = ts[4]

	with raises(IndexError):
		ts[5] = 5

def correct_length(class_name):
	ts = class_name(values=[1] * 100, times=range(100))
	assert len(ts) == 100

def interpolate_ts(class_name):
	"""
	Test piece-wise linear interpolate function with values both
	inside and outside the domain of time values.
	"""

	a = class_name(values=[1,2,3], times=[0,5,10])
	b = class_name(values=[100, -100], times=[2.5,7.5])

	c_times=[5,10,15,20]
	c = class_name(values=[i*2 for i in c_times], times=c_times)

	# Confirm that if we try to interpolate a value that actually already exists
	# in the time series, we just return it

	assert a.interpolate([5]) == class_name(times=[5],values=[2]), \
		"Interpolate not returning existing value when present"

	# Interpolating between 2 existing points
	# time delta is 5,value delta is 1, so (.2 * 1) +1 = 1.2

	assert a.interpolate([1]) == class_name(times=[1], values=[1.2]), \
		"Interpolate not returning correct value between 2 known points"

	# Confirm that interpolate returns end points when we seek values
	# outside of the existing domain of values
	assert b.interpolate([-100,100]) == \
		class_name(times=[-100,100], values=[100,-100]), \
		"Interpolate not returning endpoints for times outside of existing domain"

	# Check both endpoints and imterolated mid-values
	assert c.interpolate([2,6,11,17,25]) == \
		class_name(times=[2,6,11,17,25], values=[10,12,22,34,40])

def verify_lazy_property_time_series(class_name):
	ts = class_name([1,2,3,4,5],[1,2,3,4,5])

	# verify that TimeSeries.lazy is a LazyOperation
	assert isinstance(ts.lazy, LazyOperation) == True

	# verify that ts and ts.lazy.eval() give identical results
	assert ts == ts.lazy.eval()

def verify_lazyfied_time_series_check_length(class_name):
	"""A check length method to verify the lazy property method in the TimeSeries class."""
	@lazy
	def check_length(a,b):
		return len(a)==len(b)
	thunk = check_length(class_name(range(0,4),range(1,5)), class_name(range(1,5),range(2,6)))
	assert thunk.eval()==True

def operator_list_nparray_not_allowed(class_name):
	"""
		It should fail when we try to add a numpy array or list to a TimeSeries instance

		Parameters
		----------
		class_name : time series class
			The class to run the tests on.
		operator : operator
			The operator to use for the mathematical expression
	"""
	operators = [operator.add, operator.mul, operator.sub]
	# N: we are checking if an operation is attemped on TimeSeries with a list or np array type
	for op in operators:
		if (class_name is TimeSeries):
			ts = class_name(values=[1,2,3] , times=[1,2,3])
			with raises(TypeError):
				rhs = np.array([1,2,3])
				op(ts, rhs)

		# N: we are only checking if an operation is attemped on ArrayTimeSeries with a list type
		ts = class_name(values=[1,2,3] , times=[1,2,3])
		with raises(TypeError):
			rhs = list([1,2,3])
			op(ts, rhs)

def test_smtimeseries():
	ts = SMTimeSeries(range(5),range(5),1)
	assert len(ts) == 5
	remove_test_files()

def test_from_db():
	ts = SMTimeSeries(range(5),range(5),1)
	ts.from_db(1)

	# verify that from_db returns the SMTimeSeries
	assert isinstance(ts, SMTimeSeries)
	# and that the length is correct
	assert len(ts) == 5
	remove_test_files()

def remove_test_files():
	test_files = ['1.npy', 'id_length_map.json']
	for i in test_files:
		if os.path.exists(i):
			os.remove(i)

	for filename in glob.glob("ts_datafile*"):
		os.remove(filename)

def method_getitem(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert threes[1] == 3

def method_setitem(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	threes[0] = 3
	assert threes[0] == 3

def method_contains(class_name):
	x = class_name(values=[5,6], times=[1,2])
	assert 5 in x

def method_iter(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	cum_sum = 0
	for val in threes:
		cum_sum += val
	assert cum_sum==18

def method_values(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert isinstance(threes.values(), np.ndarray)

def method_itervalues(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	cum_sum = 0
	for val in threes.itervalues():
		cum_sum += val
	assert cum_sum==18

def method_times(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert isinstance(threes.times(), np.ndarray)

def method_itertimes(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	cum_sum = 0
	for time in threes.itertimes():
		cum_sum += time
	assert cum_sum==406

def method_items(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert threes.items()==[(100,0),(101,3),(102,6),(103,9)]

def method_iteritems(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	cum_sum_time = 0
	cum_sum_value = 0
	for time, value in threes.iteritems():
		cum_sum_time += time
		cum_sum_value += value
	assert cum_sum_time==406 and cum_sum_value==18

def method_len(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert len(threes)==4

def method_pos(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	posthrees = +threes
	assert posthrees.values_lst() == [0,3,6,9]

def method_neg(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	negthrees = -threes
	assert negthrees.values_lst()==[0,-3,-6,-9]

def method_add_int(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	add_v1 = threes + 5
	add_v2 = 5 + threes
	assert add_v1.values_lst() == [5,8,11,14] and add_v2.values_lst() == [5,8,11,14]

def method_add_two_timeseries(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	fives = class_name(values=range(0, 16, 5), times=range(100,104))
	add_v1 = threes+fives
	add_v2 = fives+threes
	assert add_v1.values_lst()==[0,8,16,24] and add_v2.values_lst()==[0,8,16,24]

def method_sub_int(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	sub_v1 = threes - 5
	sub_v2 = -(5 - threes)
	assert sub_v1.values_lst()==[-5,-2,1,4] and sub_v2.values_lst()==[-5,-2,1,4]

def method_sub_two_timeseries(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	fives = class_name(values=range(0, 16, 5), times=range(100,104))
	sub_v1 = threes-fives
	sub_v2 = -(fives-threes)
	assert sub_v1.values_lst()==[0,-2,-4,-6] and sub_v2.values_lst()==[0,-2,-4,-6]

def method_mul_int(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	mul_v1 = threes * 5
	mul_v2 = 5 * threes
	assert mul_v1.values_lst()==[0,15,30,45] and mul_v2.values_lst()==[0,15,30,45]

def method_mul_two_timeseries(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	fives = class_name(values=range(0, 16, 5), times=range(100,104))
	mul_v1 = threes*fives
	mul_v2 = fives*threes
	assert mul_v1.values_lst()==[0,15,60,135] and mul_v2.values_lst()==[0,15,60,135]

def method_eq(class_name):
	# verify that two instances of the same class are equal
	eq_v1 = class_name(values=range(0, 10, 3), times=range(100,104))
	eq_v2 = class_name(values=range(0, 10, 3), times=range(100,104))
	assert eq_v1==eq_v2

	# verify that attempted comparison between list and ArrayTimeSeries raises TypeError
	with raises(TypeError):
		eq_v1 = list([1,2,3,4])
		eq_v2 = ArrayTimeSeries(values=range(0, 10, 3), times=range(100,104))
		eq_v1==eq_v2

	# verify that attempted comparison between numpy array and TimeSeries raises TypeError
	with raises(TypeError):
		eq_v1 = np.array([1,2,3,4])
		eq_v2 = TimeSeries(values=range(0, 10, 3), times=range(100,104))
		eq_v2==eq_v1

def method_ne(class_name):
	eq_v1 = class_name(values=range(0, 10, 3), times=range(100,104))
	eq_v2 = -eq_v1
	assert eq_v1!=eq_v2

def method_mean(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert threes.mean()==4.5

def method_std(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert threes.std()==3.872983346207417

def method_produce():
	t = iter(range(1,11))
	v = iter([2*x + 1 for x in range(1,11)])
	sts = SimulatedTimeSeries(t, v)
	assert sts.produce(3) == [(1,3), (2,5), (3,7)]

def method_repr(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	repr(threes)

def method_str(class_name):
	ts = class_name(values=range(0, 20), times=range(0,20))
	if class_name is SMTimeSeries:
		assert str(ts) == '[0.0 1.0 2.0, ...]'
	else:
		assert str(ts) == '[0 1 2, ...]'

def method_abs(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	assert abs(threes) == 126

def method_bool(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	zero = class_name(values=[], times=[])
	assert bool(threes) == True
	assert bool(zero) == False

def method_times_lst(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	add_v1 = threes + 5
	add_v2 = 5 + threes
	assert add_v1.times_lst() == [100, 101, 102, 103] and add_v2.times_lst() == [100, 101, 102, 103]

def method_check_length_helper(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	zero = class_name(values=[], times=[])
	with raises(ValueError):
		threes._check_length_helper(threes, zero)

def method_check_time_domains_helper(class_name):
	threes = class_name(values=range(0, 10, 3), times=range(100,104))
	zero = class_name(values=[], times=[])
	with raises(ValueError):
		threes._check_time_domains_helper(threes, zero)