import unittest
import os
from DB import *
import sys
import pickle
import base64
sys.path.append('../')
from TimeSeries import TimeSeries

# py.test --doctest-modules  --cov --cov-report term-missing DB.py test_DB.py

# Test cases for the DB class

class DBTest(unittest.TestCase):
	def getName(self):
		return "Bainn1.dbdb"

	def height(self, node):
		if node is None:
			return 0
		leftNode = node.left_ref._referent
		rightNode = node.right_ref._referent
		return max(self.height(leftNode) + 1, self.height(rightNode) + 1)
	
	def heightMin(self, node):
		if node is None:
			return 0
		leftNode = node.left_ref._referent
		rightNode = node.right_ref._referent
		return min(self.heightMin(leftNode) + 1, self.heightMin(rightNode) + 1)
	
	def is_validly_balanced(self, node):
		# The height of the longest path to leaf cannot be more than 2x larger than the height of the shortest path to leaf
		return self.height(node) <= 2*self.heightMin(node)
	
	
	def setUp(self):
		self.dbname = self.getName()
		try:
			f = open(self.dbname, 'r+b')
		except IOError:
			fd = os.open(self.dbname, os.O_RDWR | os.O_CREAT)

			f = os.fdopen(fd, 'r+b')

		self.storage = Storage(f)
		self.storage.lock()
		self.rbtree = BinaryTree(self.storage)
		self.rbtree.set(2, "99")
		self.rbtree.set(4, "101")
		self.rbtree.set(1, "98")
		self.rbtree.set(3, "100")
		self.rbtree.set(5, "102")
		self.rbtree.set(6, "103")
		self.rbtree.set(7, "104")
		self.rbtree.set(8, "105")
		self.	rbtree.set(2, "99")
		self.	rbtree.set(4444, "101")
		

		"""	
		self.	rbtree.set(4, "101")
		self.	rbtree.set(4, "101")
		self.	rbtree.set(4, "101")
		self.	rbtree.set(4, "101")
		self.	rbtree.set(4, "101")
		self.	rbtree.set(1, "98")
		self.	rbtree.set(3, "100")
		self.	rbtree.set(5, "102")
		self.	rbtree.set(6, "103")
		self.	rbtree.set(7, "104")	
		self.	rbtree.set(8, "105")
		self.	rbtree.set(10, "105")
		self.	rbtree.set(20, "105")
		#self.	rbtree.set(30, "105")
		#self.	rbtree.set(15, "105")
		
		
		self.	rbtree.set(18, "105")
		self.	rbtree.set(50, "105")
		self.	rbtree.set(32, "105")
		self.	rbtree.set(81, "105")
		"""

		self.root = self.rbtree._follow(self.rbtree._tree_ref)
		self.ts = TimeSeries(values=[1, 3, 0, 1.5, 1], times=[1.5, 2, 2.5, 3, 10.5])
		self.ts_notime = TimeSeries(values=[2, 3, 4], times=None)
		self.ts_single = TimeSeries(values=[-2], times=[1])

	def tearDown(self):
		os.remove(self.getName())
		del self.dbname
		del self.storage
		del self.rbtree
		del self.root
		del self.ts
		del self.ts_notime
		del self.ts_single

	def test_isInstance_BinaryTree(self):
		self.assertTrue(isinstance(self.rbtree, BinaryTree))

	def test_rootIsBlack(self):
		self.assertTrue(self.root.color == 1)

	def test_BinaryTree_Root(self):
		self.assertTrue(self.root.key == 4)

	def test_BinaryTree_Left(self):
		left = self.rbtree._follow(self.root.left_ref)
		self.assertTrue(left.key == 2)

	def test_BinaryTree_Right(self):
		right = self.rbtree._follow(self.root.right_ref)
		print (right.value_ref.address)
		self.assertTrue(right.key == 6)

	def test_root_address(self):
		self.assertTrue(self.rbtree._tree_ref.address == 0)

	def test_commit(self):
		self.assertTrue(self.rbtree.commit() == None)

	def test_get_value_binarytree(self):
		value = self.rbtree.get(1)
		print(value)
		self.assertTrue(value == "98")

	def test_lock(self):
		self.storage.unlock()
		value = self.rbtree.get(2)
		print(value)
		self.assertTrue(value == "98")

	# TODO: Fix
	def test_valueRef(self):
		self.root.value_ref._referent = None
		self.root.value_ref._address = 0xff
		valueref = self.root.value_ref.get(self.storage)
		self.assertTrue(valueref == '')

	def test_Big_RBT_Tree(self):
		rbtree = BinaryTree(self.storage)
		rbtree.set(2, "99")
		rbtree.set(4, "101")
		rbtree.set(1, "98")
		rbtree.set(3, "100")
		rbtree.set(5, "102")
		rbtree.set(6, "103")
		rbtree.set(7, "104")
		rbtree.set(8, "105")
		rbtree.set(2, "99")
		rbtree.set(4444, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(1, "98")
		rbtree.set(3, "100")
		rbtree.set(5, "102")
		rbtree.set(6, "103")
		rbtree.set(7, "104")	
		rbtree.set(8, "105")
		rbtree.set(10, "105")
		rbtree.set(20, "105")

		root = rbtree._follow(rbtree._tree_ref)
		self.assertEquals(self.is_validly_balanced(root), 1)
		#self.assertTrue(root.key == 4)


	def test_Big_RBT_Tree2(self):
		rbtree = BinaryTree(self.storage)
		rbtree.set(2234, "99")
		rbtree.set(2344, "101")
		rbtree.set(1, "98")
		rbtree.set(3, "100")
		rbtree.set(5, "102")
		rbtree.set(236, "103")
		rbtree.set(7, "104")
		rbtree.set(2228, "105")
		rbtree.set(2, "99")
		rbtree.set(4444, "101")
		rbtree.set(422, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(774, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "234101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(14, "101")
		rbtree.set(14, "101")
		rbtree.set(444, "101")
		rbtree.set(524, "101")
		rbtree.set(4, "101")
		rbtree.set(4, "101")
		rbtree.set(3456541, "98")
		rbtree.set(3, "100")
		rbtree.set(5, "102")
		rbtree.set(6, "103")
		rbtree.set(57, "104")	
		rbtree.set(8, "105")
		rbtree.set(22310, "105")
		rbtree.set(240, "105")
		root = rbtree._follow(rbtree._tree_ref)
		self.assertEquals(self.is_validly_balanced(root), 1)
		#self.assertTrue(root.key == 7)

	# Unable to test:
	def test_bytes_to_referent_binaryRef(self):
		self.assertTrue(1 == 1)

	def test_if_node_is_black(self):
		self.assertTrue(self.root.is_black() == 1)	

	def test_lock_rbttree(self):
		# Lock storage
		self.storage.lock()
		
		# Get root:
		root = self.rbtree._follow(self.rbtree._tree_ref)
		self.assertTrue(1==1)









"""
		key = 1
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts)
		ts_retrieved = self.wdb.getTimeSeries(key)
		self.assertEquals(ts_retrieved.values()[0], 1)

	def test_storeAndGetWithoutKey(self):
		# Key is randomized here
		key = self.wdb.storeKeyAndTimeSeries(timeSeries=self.ts)
		ts_retrieved = self.wdb.getTimeSeries(key)
		self.assertEquals(ts_retrieved.values()[0], 1)

	def test_storeAndGetSize(self):
		key = self.wdb.storeKeyAndTimeSeries(timeSeries=self.ts)
		self.assertEquals(self.wdb.getTimeSeriesSize(key=key), 5)

	def test_storeAndGetWithKeyNoTime(self):
		key = "2"
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts_notime)
		ts_retrieved = self.wdb.getTimeSeries(key)
		self.assertEquals(ts_retrieved.values()[0], 2)

	def test_storeAndGetSizeSingle(self):
		key = 999
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts_single)
		self.assertEquals(self.wdb.getTimeSeriesSize(key=key), 1)

	def test_inputClassIsNotTimeSeries(self):
		with self.assertRaises(ValueError):
			self.wdb.storeKeyAndTimeSeries(timeSeries=[1,2,3])

	def test_keyIsAlreadyInDB(self):
		key = 1
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts)
		with self.assertRaises(ValueError):
			self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)

	# Test cache
	
	def test_cacheNotFull_getOnce(self):
		key = 1
		self.wdb.storeKeyAndTimeSeries(key=key, timeSeries=self.ts)
		# Not get yet, should not cache
		self.assertEquals(self.wdb.cache, {})
		# Get once, should cache it
		self.wdb.getTimeSeries(key)
		self.assertEquals(self.wdb.cache, {'1': self.ts})
		self.assertEquals(self.wdb.keyToCount, {'1': 1})

	def test_cacheNotFull_getMultiple(self):
		self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		# Not get yet, should not cache
		self.assertEquals(self.wdb.cache, {})
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.assertEquals(self.wdb.cache, {'1': self.ts, '2': self.ts_single})
		self.assertEquals(self.wdb.keyToCount, {'1': 2, '2': 1})

	def test_cacheFull(self):
		self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		self.wdb.storeKeyAndTimeSeries(key=3, timeSeries=self.ts_notime)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(2)
		# key 3 should be replaced by 2
		self.assertEquals(self.wdb.cache, {'1': self.ts, '2': self.ts_single})
		self.assertEquals(self.wdb.keyToCount, {'1': 2, '2': 2, '3': 1})

	def test_cacheFullComplex(self):
		self.wdb.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		self.wdb.storeKeyAndTimeSeries(key=3, timeSeries=self.ts_notime)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(2)
		self.assertEquals(sorted(list(self.wdb.cache.keys())), ['2', '3'])
		self.assertEquals(self.wdb.keyToCount, {'1': 2, '2': 3, '3': 3})

	def test_noCache(self):
		self.wdb_noCache.storeKeyAndTimeSeries(key=1, timeSeries=self.ts)
		self.wdb.storeKeyAndTimeSeries(key=2, timeSeries=self.ts_single)
		self.wdb.storeKeyAndTimeSeries(key=3, timeSeries=self.ts_notime)
		self.wdb.getTimeSeries(3)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(1)
		self.wdb.getTimeSeries(2)
		self.wdb.getTimeSeries(2)
		self.assertEquals(self.wdb_noCache.cache, {})

	# Test encode and decode

	def test_encode(self):
		timeSeriesString = self.wdb._encode(timeSeries=self.ts)
		self.assertEqual(timeSeriesString, '(1.5,1);(2,3);(2.5,0);(3,1.5);(10.5,1)')

	def test_decode(self):
		timeSeriesString = '(1.5,1);(2,3);(2.5,0);(3,1.5);(10.5,1)'
		timeSeries = self.wdb._decode(encodedTimeSeries=timeSeriesString)
		self.assertEqual(timeSeries, self.ts)

	def test_decode_malformed1(self):
		timeSeriesString = '(1.51);(2,3);(2.5,0);(3,1.5);(10.5,1)'
		with self.assertRaises(ValueError):
			timeSeries = self.wdb._decode(encodedTimeSeries=timeSeriesString)

	def test_decode_malformed2(self):
		timeSeriesString = '(1.5,1;(2,3);(2.5,0);(3,1.5);(10.5,1)'
		with self.assertRaises(ValueError):
			timeSeries = self.wdb._decode(encodedTimeSeries=timeSeriesString)

"""
