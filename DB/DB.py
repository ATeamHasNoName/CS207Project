class ValueRef(object):
    " a reference to a string value on disk"
    def __init__(self, referent=None, address=0):
        self._referent = referent #value to store
        self._address = address #address to store at
        
    @property
    def address(self):
        return self._address
    
    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_bytes(referent):
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        return bytes.decode('utf-8')

    
    def get(self, storage):
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


import pickle
class BinaryNodeRef(ValueRef):
    "reference to a btree node on disk"
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        "have a node store its refs"
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        "use pickle to convert node to bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )

class Color(object):
    RED = 0
    BLACK = 1
    
class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color=kwargs.get('color', node.color)
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color=Color.RED):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color = color

    def is_red(self):
        return self.color == Color.RED

    def is_black(self):
        return self.color == Color.BLACK

    # If node is red, returns a black version of the node
    def blacken(self):
        if self.is_red():
            return BinaryNode.from_node(self, color=Color.BLACK)
        else:
            return self
            # return BinaryNode(self.left_ref, self.key, self.value_ref, self.right_ref, color=Color.BLACK)

    # TODO: Have to handle cases where right_ref or left_ref are None
    
    def rotate_left(self):
        # Rotate around right node
        rightNode = self.right_ref._referent
        # Get new left ref
        leftNode = BinaryNode(self.left_ref, self.key, self.value_ref, rightNode.left_ref, color=self.color)
        newLeftRef = BinaryNodeRef(referent=leftNode)#, address=self.value_ref.address)
        return BinaryNode(newLeftRef, rightNode.key, rightNode.value_ref, rightNode.right_ref, color=rightNode.color)

    def rotate_right(self):
        # Rotate around left node
        leftNode = self.left_ref._referent
        # Get new right ref
        rightNode = BinaryNode(leftNode.right_ref, self.key, self.value_ref, self.right_ref, color=self.color)
        newRightRef = BinaryNodeRef(referent=rightNode)#, address=self.value_ref.address)
        return BinaryNode(leftNode.left_ref, leftNode.key, leftNode.value_ref, newRightRef, color=leftNode.color)

    def recolored(self):
        # Blacken left and right nodes
        leftNode = self.left_ref._referent.blacken()
        rightNode = self.right_ref._referent.blacken()
        leftRef = self.left_ref
        rightRef = self.right_ref
        if leftNode is not None:
            leftRef = BinaryNodeRef(referent=leftNode)#, address=self.left_ref.address)
        if rightNode is not None:
            rightRef = BinaryNodeRef(referent=rightNode)#, address=self.right_ref.address)
        return BinaryNode(leftRef, self.key, self.value_ref, rightRef, color=Color.RED)

    def balance(self):
        # If red, no need to rebalance
        # print('balancing\n========================')
        if self.is_red():
            # print("self is red")
            return self
        # Get all nodes first
        leftNode = self.left_ref._referent
        rightNode = self.right_ref._referent
        leftOfLeftNode = rightOfLeftNode = leftOfRightNode = rightOfRightNode = None
        if leftNode is not None:
            leftOfLeftNode = leftNode.left_ref._referent
            rightOfLeftNode = leftNode.right_ref._referent
        if rightNode is not None:
            leftOfRightNode = rightNode.left_ref._referent
            rightOfRightNode = rightNode.right_ref._referent


        # print('leftNode: ', leftNode)
        # print('rightNode: ', rightNode)
        # print('leftOfLeftNode: ', leftOfLeftNode)
        # print('rightOfLeftNode: ', rightOfLeftNode)
        # print('leftOfRightNode: ', leftOfRightNode)
        # print('rightOfRightNode: ', rightOfRightNode)

        # Perform the rebalancing
        
        # On the left node
        if leftNode is not None and leftNode.is_red():
            if rightNode is not None and rightNode.is_red():
                return self.recolored()
            if leftOfLeftNode is not None and leftOfLeftNode.is_red():
                return self.rotate_right().recolored()
            if rightOfLeftNode is not None and rightOfLeftNode.is_red():
                newLeftNode = leftNode.rotate_left()
                newLeftRef = BinaryNodeRef(referent=newLeftNode)#, address=newLeftNode.value_ref.address)
                return BinaryNode(newLeftRef, self.key, self.value_ref, self.right_ref, color=self.color).rotate_right().recolored()
            return self

        # On the right node
        if rightNode is not None and rightNode.is_red():
            if rightOfRightNode is not None and rightOfRightNode.is_red():
                return self.rotate_left().recolored()
            if leftOfLeftNode is not None and leftOfRightNode.is_red():
                newRightNode = rightNode.rotate_right()
                newRightRef = BinaryNodeRef(referent=newRightNode)#, address=newRightNode.value_ref.address)
                return BinaryNode(self.left_ref, self.key, self.value_ref, newRightRef, color=self.color).rotate_left().recolored()

        # print('return self without balancing!!!')
        return self

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class BinaryTree(object):
    "Immutable Binary Tree class. Constructs new tree on changes"
    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        "changes are final only when committed"
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        "get value for a key"
        #your code here
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        "set a new value in the tree. will cause a new tree"
        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        #insert and get new tree ref
        
        
        self._tree_ref = self._insert(node, key, value_ref)
        treeNode = self._tree_ref._referent
        balancedTreeNode = treeNode.blacken()
        self._tree_ref = BinaryNodeRef(referent=balancedTreeNode)
        # Balance the tree
        
    
    def _insert(self, node, key, value_ref):
        "insert a new node creating a new path from root"
        #create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                BinaryNodeRef(), key, value_ref, BinaryNodeRef(), color=Color.RED)
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref)).balance()
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref)).balance()
        else: #create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref, key=key)
            new_node = new_node.balance()
            
        return BinaryNodeRef(referent=new_node)

    def _follow(self, ref):
        "get a node from a reference"
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node

import os
import struct

import portalocker

class Storage(object):
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        "guarantee that the next write will start on a sector boundary"
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "if not locked, lock the file for writing"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "go to beginning of file which is on sec boundary"
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        "write data to disk, returning the adress at which you wrote it"
        #first lock, get to end, get address to return, write size
        #write data, unlock <==WRONG, dont want to unlock here
        #your code here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        self.lock()
        self._f.flush()
        #make sure you write root address at position 0
        self._seek_superblock()
        #write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        #read the first integer in the file
        #your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        return self._f.closed

class DBDB(object):

    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        self._storage.close()

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        self._assert_not_closed()
        return self._tree.delete(key)

import os
class DB(object):
    def connect(dbname):
        try:
            f = open(dbname, 'r+b')
        except IOError:
            fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, 'r+b')
        return DBDB(f)
