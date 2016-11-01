import unittest
import numpy as np
from TimeSeries import TimeSeries

# py.test --doctest-modules  --cov --cov-report term-missing TimeSeries.py test_TimeSeries.py

# Test cases for the TimeSeries class
class TimeSeriesTest(unittest.TestCase):

	def setUp(self):
		self.singleseries = TimeSeries(values=[1], times=[1])
		self.series = TimeSeries(values=[1, 3, 0, -1.5, -1], times=[1.5, 2, 2.5, 10.5, 3])
		
	def tearDown(self):
		del self.singleseries
		del self.series

	'''Init/repOK tests'''
	
	def test_init_with_time(self):
		self.assertEqual(self.series[1.5], 1)

	def test_init_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(series_notime[0], 1)		

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

	def test_init_with_emptyvalues(self):
		with self.assertRaises(ValueError):
			TimeSeries(values=[], times=[])

	'''times, values, items tests'''

	def test_times(self):
		# Times should be sorted too
		self.assertEqual(self.series.times(), [1.5, 2, 2.5, 3, 10.5])

	def test_times_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(series_notime.times(), None)
	
	def test_values(self):
		self.assertEqual(self.series.values(), [1, 3, 0, -1, -1.5])

	def test_values_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(series_notime.values(), [1, 3, 0, -1.5, -1])

	def test_items(self):
		# Items are also sorted based on time
		self.assertEqual(self.series.items(), [(1.5, 1), (2, 3), (2.5, 0), (3, -1), (10.5, -1.5)])

	def test_items_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(series_notime.items(), [(0, 1), (1, 3), (2, 0), (3, -1.5), (4, -1)])

	'''__len__, __getitem__, __setitem__ tests'''

	def test_len(self):
		self.assertEqual(len(self.series), 5)

	def test_len_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(len(series_notime), 5)

	def test_len_singleseries(self):
		self.assertEqual(len(self.singleseries), 1)

	def test_getitem(self):
		self.assertEqual(self.series[2.5], 0)

	def test_getitem_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(series_notime[0], 1)

	def test_getitem_singleseries(self):
		self.assertEqual(self.singleseries[1], 1)

	def test_getitem_wrongtime(self):
		with self.assertRaises(IndexError):
			self.series[9999]

	def test_getitem_wrongtime_withouttime(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		with self.assertRaises(IndexError):
			series_notime[9999]

	# In tests for __setitem__ we define the data locally so we don't mutate the class data
	def test_setitem(self):
		_series = TimeSeries(values=[1, 3, 0, -1.5, -1], times=[1.5, 2, 2.5, 10.5, 3])
		self.assertEqual(_series[3], -1)
		_series[3] = 999
		self.assertEqual(_series[3], 999)

	def test_setitem_without_time(self):
		_series = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(_series[0], 1)
		_series[0] = -999
		self.assertEqual(_series[0], -999)	
		
	def test_setitem_wrongtime(self):
		_series = TimeSeries(values=[1, 3, 0, -1.5, -1], times=[1.5, 2, 2.5, 10.5, 3])
		with self.assertRaises(IndexError):
			_series[9999] = 5

	def test_setitem_wrongtime_withouttime(self):
		_series = TimeSeries(values=[1.5, 2, 2.5, 10.5, 3])
		with self.assertRaises(IndexError):
			_series[-1] = 0

	'''__iter__, itertimes, itervalues, iteritems tests'''

	def test_iter(self):
		ind = 0
		for v in self.series:
			self.assertEqual(v, self.series.values()[ind])
			ind = ind + 1

	def test_iter_without_time(self):
		ind = 0
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		for v in series_notime:
			self.assertEqual(v, series_notime.values()[ind])
			ind = ind + 1

	def test_itertimes(self):
		ind = 0
		for t in self.series.itertimes():
			self.assertEqual(t, self.series.times()[ind])
			ind = ind + 1

	def test_itertimes_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		for t in series_notime.itertimes():
			self.assertEqual(t, None)

	def test_itervalues(self):
		ind = 0
		for v in self.series.itervalues():
			self.assertEqual(v, self.series.values()[ind])
			ind = ind + 1

	def test_itervalues_without_time(self):
		ind = 0
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		for v in series_notime.itervalues():
			self.assertEqual(v, series_notime.values()[ind])
			ind = ind + 1

	def test_iteritems(self):
		ind = 0
		for tv in self.series.iteritems():
			self.assertEqual(tv, self.series.items()[ind])
			ind = ind + 1

	def test_iteritems_without_time(self):
		ind = 0
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		for tv in series_notime.iteritems():
			self.assertEqual(tv, series_notime.items()[ind])
			ind = ind + 1

	'''repr, str tests'''

	def test_repr(self):
		self.assertEqual(repr(self.series), "TimeSeries([(1.5, 1), (2, 3), (2.5, 0), (3, -1), (10.5, -1.5)])")

	def test_repr_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(repr(series_notime), "TimeSeries([(0, 1), (1, 3), (2, 0), (3, -1.5), (4, -1)])")

	def test_repr_truncated(self):
		_series = TimeSeries(values=range(0, 10000))
		# This is a long line I know, but I truncated at 100
		self.assertEqual(repr(_series), "TimeSeries([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99), ...])")		

	def test_str(self):
		self.assertEqual(str(self.series), "TimeSeries\nLength: 5\nFirst (oldest): 1, Last (newest): -1.5")

	def test_str_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(str(series_notime), "TimeSeries\nLength: 5\nFirst (oldest): 1, Last (newest): -1")

	'''abs, bool, neg, pos tests'''		

	def test_abs(self):
		self.assertEqual(abs(self.series), [(1.5, 1.0), (2, 3.0), (2.5, 0.0), (3, 1.0), (10.5, 1.5)])

	def test_abs_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(abs(series_notime), [(0, 1.0), (1, 3.0), (2, 0.0), (3, 1.5), (4, 1.0)])

	# In our context, bool will never be false because of the repOK
	def test_bool(self):
		self.assertTrue(bool(self.series))

	def test_bool_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertTrue(bool(series_notime))

	def test_bool_singleseries(self):
		self.assertTrue(bool(self.singleseries))

	def test_neg(self):
		self.assertEqual(-self.series, [(1.5, -1), (2, -3), (2.5, 0), (3, 1), (10.5, 1.5)])

	def test_neg_without_time(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(-series_notime, [(0, -1), (1, -3), (2, 0), (3, 1.5), (4, 1)])

	def test_pos(self):
		self.assertEqual(+self.series, [(1.5, 1), (2, 3), (2.5, 0), (3, -1), (10.5, -1.5)])

	def test_pos_without_time(self):
		# Actually he same to items
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertEqual(+series_notime, series_notime.items())

	'''eq, add, sub, mul tests'''

	def test_eq(self):
		self.assertTrue(self.series == self.series)

	def test_eq_reordered(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = TimeSeries(values=[1,3,2], times=[0,10,5])
		self.assertTrue(_s1 == _s2)

	def test_eq_constant(self):
		with self.assertRaises(NotImplementedError):
			self.series == 4

	def test_neq(self):
		_s1 = TimeSeries(values=[1,2,4], times=[0,5,10])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertFalse(_s1 == _s2)

	def test_eq_notime(self):
		series_notime = TimeSeries(values=[1, 3, 0, -1.5, -1])
		self.assertTrue(series_notime == series_notime)

	def test_neq_notime(self):
		_s1 = TimeSeries(values=[1,-2,-4])
		_s2 = TimeSeries(values=[1,2,3])
		self.assertFalse(_s1 == _s2)

	def test_add(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 + _s2, TimeSeries(values=[2,4,6], times=[0,5,10]))

	def test_add_without_time(self):
		_s1 = TimeSeries(values=[-1,2,-3])
		_s2 = TimeSeries(values=[1,2,3])
		self.assertEqual(_s1 + _s2, TimeSeries(values=[0,4,0]))

	def test_add_reorderedtime(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = TimeSeries(values=[2,1,3], times=[5,0,10])
		self.assertEqual(_s1 + _s2, TimeSeries(values=[2,4,6], times=[0,5,10]))

	def test_add_constant(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 + 5.2, TimeSeries(values=[6.2,7.2,8.2], times=[0,5,10]))

	def test_add_constant_without_time(self):
		_s1 = TimeSeries(values=[1,2,3])
		self.assertEqual(_s1 + 5.2, TimeSeries(values=[6.2,7.2,8.2]))

	def test_sub(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 - _s2, TimeSeries(values=[0,0,0], times=[0,5,10]))

	def test_sub_without_time(self):
		_s1 = TimeSeries(values=[-1,2,-3])
		_s2 = TimeSeries(values=[1,2,3])
		self.assertEqual(_s1 - _s2, TimeSeries(values=[-2,0,-6]))

	def test_sub_constant(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 - 3, TimeSeries(values=[-2,-1,0], times=[0,5,10]))

	def test_sub_constant_without_time(self):
		_s1 = TimeSeries(values=[1,2,3])
		self.assertEqual(_s1 - 3, TimeSeries(values=[-2,-1,0]))

	def test_mul(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 * _s2, TimeSeries(values=[1,4,9], times=[0,5,10]))

	def test_mul_without_time(self):
		_s1 = TimeSeries(values=[-1,2,-3])
		_s2 = TimeSeries(values=[1,2,3])
		self.assertEqual(_s1 * _s2, TimeSeries(values=[-1,4,-9]))

	def test_mul_constant(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,10])
		self.assertEqual(_s1 * 0, TimeSeries(values=[0,0,0], times=[0,5,10]))

	def test_mul_constant_without_time(self):
		_s1 = TimeSeries(values=[1,2,3])
		self.assertEqual(_s1 * -10, TimeSeries(values=[-10,-20,-30]))

	# Run the tests that check for bad conditions across different operators
	
	def test_nontimeseries(self):
		with self.assertRaises(NotImplementedError):
			self.series + [1,2,3]

	def test_differentlengthtime(self):
		_s1 = TimeSeries(values=[1,2,3,4], times=[0,5,10, 12])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		with self.assertRaises(ValueError):
			_s1 + _s2

	def test_differentvaluestime(self):
		_s1 = TimeSeries(values=[1,2,3], times=[0,5,9])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		with self.assertRaises(ValueError):
			_s1 * _s2

	def test_notimeandtime(self):
		_s1 = TimeSeries(values=[1,2,3])
		_s2 = TimeSeries(values=[1,2,3], times=[0,5,10])
		with self.assertRaises(ValueError):
			_s1 - _s2

	'''interpolate, __contains__ tests'''

	def test_interpolate_single1(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([100, -100],[2.5, 7.5])
		self.assertEqual(a.interpolate([1]), TimeSeries([1.2],[1]) )

	def test_interpolate_single2(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([100, -100],[2.5, 7.5])
		self.assertEqual(a.interpolate(list(b.itertimes())), TimeSeries([1.5, 2.5], [2.5,7.5]) )

	def test_interpolate_boundary(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([100, -100],[2.5, 7.5])
		self.assertEqual(a.interpolate([-100, 100]),TimeSeries([1,3],[-100,100]))

	def test_contains(self):
		self.assertTrue(3 in self.series)

	def test_notcontains(self):
		self.assertFalse(-99 in self.series)

	def test_contains_without_time(self):
		_s1 = TimeSeries(values=[1])
		self.assertTrue(1 in _s1)

	def test_notcontains_without_time(self):
		_s1 = TimeSeries(values=range(0, 10000))
		self.assertFalse(-1 in _s1)

	''' Lazy tests '''

	def test_lazy_equal(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = a.lazy
		self.assertTrue(a == b.eval())

	def test_lazy_not_equal(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = TimeSeries([1, 2, 4],[0, 5, 10])
		c = b.lazy
		self.assertFalse(a == c.eval())

	def test_lazy_printing(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = a.lazy
		self.assertFalse(str(a) == str(b))

	def test_lazy_len(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		b = a.lazy
		length = len(b)
		self.assertTrue(length == 2)

	def test_lazy_instance(self):
		a = TimeSeries([1, 2, 3],[0, 5, 10])
		self.assertTrue(isinstance(a.lazy.eval(), TimeSeries)==True)


