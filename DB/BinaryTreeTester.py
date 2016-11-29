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


# Test btree
btree = BinaryTree(storage)

btree.set(2, "99")
btree.set(4, "101")
btree.set(1, "98")
btree.set(3, "100")
btree.set(5, "102")
btree.set(6, "103")
btree.set(7, "104")
btree.set(8, "105")
# print(type(btree.tree_ref))
root = getNodeFromRef(btree, btree._tree_ref)
print(root)
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