from DB import *
import os


dbname = 'binarytreetest.dbdb'
try:
    f = open(dbname, 'r+b')
except IOError:
    fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
    f = os.fdopen(fd, 'r+b')

storage = Storage(f)

# Utility functions to test tree
def getNodeFromRef(tree, ref):
	return tree._follow(ref)

def printTree(btree, ref, parent, relationship):
	if ref is None:
		return
	node = getNodeFromRef(btree, ref)
	if node is None:
		return
	key = "%s" % node.key
	value = "%s" % getNodeFromRef(btree, node.value_ref)
	print('%s of Parent Key: %s \t Key: %s, Value: %s' % (relationship, parent, key, value))
	printTree(btree, node.left_ref, key, "left")
	printTree(btree, node.right_ref, key, "right")

def height(node):
	if node is None:
		return 0
	leftNode = node.left_ref._referent
	rightNode = node.right_ref._referent
	return max(height(leftNode) + 1, height(rightNode) + 1)

def heightMin(node):
	if node is None:
		return 0
	leftNode = node.left_ref._referent
	rightNode = node.right_ref._referent
	return min(heightMin(leftNode) + 1, heightMin(rightNode) + 1)

def is_validly_balanced(node):
	# The height of the longest path to leaf cannot be more than 2x larger than the height of the shortest path to leaf
	return height(node) <= 2*heightMin(node)


def is_balanced(node):
	if node is None:
		return True
	leftNode = node.left_ref._referent
	rightNode = node.right_ref._referent
	# Is balanced if absolute height difference is less than or equal to 1
	isBalanced = abs(height(leftNode) - height(rightNode)) <= 1
	return (isBalanced and is_balanced(leftNode) and is_balanced(rightNode))

# Test btree
btree = BinaryTree(storage)

# btree.set(2, "99")
# btree.set(4, "101")
# btree.set(1, "98")
# btree.set(3, "100")
# btree.set(5, "102")
# btree.set(6, "103")
# btree.set(7, "104")
# btree.set(8, "105")
# btree.set(10, "105")
# btree.set(11, "105")
# btree.set(12, "105")
# btree.set(0, "105")
#
btree.set(0, "99")
btree.set(1, "100")
btree.set(2, "101")
btree.set(3, "102")
btree.set(4, "103")
btree.set(5, "104")
# btree.set(6, "105")
# btree.set(7, "106")
root = getNodeFromRef(btree, btree._tree_ref)
print(heightMin(root))
print(is_validly_balanced(root))
printTree(btree, btree._tree_ref, "-1", "none")


# os.remove(dbname)

# from WrappedDB import WrappedDB
# import sys
# sys.path.append('../')
# from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
# from TimeSeries import TimeSeries
# # Test storage
# wdb = WrappedDB('testwdb.dbdb', cacheSize=0)

# ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])

# key1 = wdb.storeKeyAndTimeSeries(key="2", timeSeries=ts)
# key2 = wdb.storeKeyAndTimeSeries(key="1", timeSeries=ts)
# # print(wdb.getTimeSeries("2").values())


# os.remove('testwdb.dbdb')