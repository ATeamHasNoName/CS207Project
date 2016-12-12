import unittest
import os
from DB import *
import sys
import pickle
import base64
sys.path.append('../../MS1/')
from TimeSeries import TimeSeries

# py.test --doctest-modules  --cov --cov-report term-missing DB.py test_DB.py

# Test cases for the DB class

class DBTest(unittest.TestCase):

	def getName(self):
		return "dbtest.dbdb"

	def _height(self, node):
		"""
		Private helper function that finds the longest path to a leaf node and returns it as an integer
		"""
		if node is None:
			return 0
		leftNode = node.left_ref._referent
		rightNode = node.right_ref._referent
		return max(self._height(leftNode) + 1, self._height(rightNode) + 1)
	
	def _heightMin(self, node):
		"""
		Private helper function that finds the shortest path to a leaf node and returns it as an integer
		"""
		if node is None:
			return 0
		leftNode = node.left_ref._referent
		rightNode = node.right_ref._referent
		return min(self._heightMin(leftNode) + 1, self._heightMin(rightNode) + 1)
	
	def is_validly_balanced(self, node):
		"""
		The height of the longest path to leaf cannot be more than 2x larger than the 
		height of the shortest path to leaf for it to be validly balanced as an RBT.
		"""
		return self._height(node) <= 2*self._heightMin(node)
	
	def setUp(self):
		self.dbname = self.getName()
		try:
			f = open(self.dbname, 'r+b')
		except IOError:
			fd = os.open(self.dbname, os.O_RDWR | os.O_CREAT)

			f = os.fdopen(fd, 'r+b')

		self.storage = Storage(f)
		self.rbtree = BinaryTree(self.storage)
		self.rbtree.set(2, "99")
		self.rbtree.set(4, "101")
		self.rbtree.set(1, "98")
		self.rbtree.set(3, "100")
		self.rbtree.set(5, "102")
		self.rbtree.set(6, "103")
		self.rbtree.set(7, "104")
		self.rbtree.set(8, "105")
		self.rbtree.set(2, "99")
		self.rbtree.set(4444, "101")
		self.root = self.rbtree._follow(self.rbtree._tree_ref)

	def tearDown(self):
		os.remove(self.getName())
		del self.dbname
		del self.storage
		del self.rbtree
		del self.root

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
		self.assertTrue(right.key == 6)

	def test_root_address(self):
		self.assertTrue(self.rbtree._tree_ref.address == 0)

	def test_commit(self):
		self.assertTrue(self.rbtree.commit() == None)

	def test_get_value_binarytree(self):
		value = self.rbtree.get(1)
		self.assertTrue(value == "98")

	def test_get_none(self):
		ref = ValueRef()
		dbdb = DB.connect('test.dbdb')
		storage = dbdb._storage
		ref._referent = None
		ref._address = 428
		referent = ref.get(storage)
		self.assertEquals(referent, '')
		os.remove('test.dbdb')
	
	def test_DBDB_not_closed(self):
		dbdb = DB.connect('dd.dbdb')
		dbdb.close()
		dbdb.set(5,'5')
		with self.assertRaises(KeyError):
			val = dbdb.get(5)	
		os.remove('dd.dbdb')
	
	def test_DBDB_commit(self):
		dbdb = DB.connect('dd.dbdb')
		dbdb.set(5,'5')
		val = dbdb.get(5)
		commitRes = dbdb.commit()
		self.assertTrue(commitRes == None)
		os.remove('dd.dbdb')

	def test_balanced_one_node(self):
		rbtree = BinaryTree(self.storage)
		rbtree.set(9, "99")
		root = rbtree._follow(rbtree._tree_ref)
		self.assertTrue(self.is_validly_balanced(root),1)

	def test_balanced_right_insert(self):
		rbtree = BinaryTree(self.storage)
		rbtree.set(0, "99")
		rbtree.set(1, "101")
		rbtree.set(2, "98")
		rbtree.set(3, "10")
		rbtree.set(4, "12")
		rbtree.set(5, "152")
		root = rbtree._follow(rbtree._tree_ref)
		self.assertTrue(self.is_validly_balanced(root),1)

	def test_balanced_left_insert(self):
		rbtree = BinaryTree(self.storage)
		rbtree.set(9, "99")
		rbtree.set(8, "101")
		rbtree.set(7, "98")
		rbtree.set(6, "10")
		rbtree.set(5, "12")
		rbtree.set(4, "152")
		root = rbtree._follow(rbtree._tree_ref)
		self.assertTrue(self.is_validly_balanced(root),1)

	def test_balanced_random_insertions(self):
		rbtree = BinaryTree(self.storage)
		rbtree.set(9, "99")
		rbtree.set(1, "101")
		rbtree.set(70, "98")
		rbtree.set(6, "10")
		rbtree.set(50, "12")
		rbtree.set(4, "152")
		rbtree.set(40, "152")
		rbtree.set(3, "152")
		rbtree.set(30, "152")
		rbtree.set(2, "152")
		rbtree.set(20, "152")
		root = rbtree._follow(rbtree._tree_ref)
		self.assertTrue(self.is_validly_balanced(root),1)

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

	def test_if_node_is_black(self):
		self.assertTrue(self.root.is_black() == 1)		
