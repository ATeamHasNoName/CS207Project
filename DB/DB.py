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
        leftAddr = None
        if referent.left is not None:
            leftAddr = referent.left.value_ref.address
        rightAddr = None
        if referent.right is not None:
            rightAddr = referent.right.value_ref.address
        print('leftAddr: ', leftAddr)
        print('key: ', referent.key)
        print('value: ', referent.value_ref.address)
        print('rightAddr: ', leftAddr)
        return pickle.dumps({
            'left': leftAddr,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': rightAddr,
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left'])._referent,
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right'])._referent,
        )

class Color(object):
    RED = 0
    BLACK = 1
    
class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left=kwargs.get('left', node.left),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value', node.value_ref),
            right=kwargs.get('right', node.right),
        )

    def __init__(self, left, key, value_ref, right, color=Color.RED):
        self._color = color
        self.left = left
        self.key = key
        self.value_ref = value_ref
        self.right = right

    @property
    def color(self):
        return self._color
    
    # def blacken(self):
    #     if self.is_red():
    #         return BinaryNode(
    #             self.left_ref,
    #             self.key,
    #             self.value_ref
    #             self.right_ref,
    #             color=Color.BLACK,
    #         )
    #     return self

    def is_red(self):
        return self._color == Color.RED

    def is_black(self):
        return self._color == Color.BLACK

    # def rotate_left(self):
    #     rightNode = self.right_ref
    #     newLeftNode = BinaryNode(self.left_ref, self.key, self.value_ref, BinaryTree().update(self.right_ref), color=self.color)
    #     return BinaryNode(
    #         RedBlackTree(
    #             self.left,
    #             self.value,
    #             EmptyRedBlackTree().update(self.right.left),
    #             color=self.color,
    #         ),
    #         self.right.value,
    #         self.right.right,
    #         color=self.right.color,
    #     )

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        
        # TODO: Uncomment this part if necessary
        if self.left is not None:
            self.left.value_ref.store(storage)
        if self.right is not None:
            self.right.value_ref.store(storage)
        # self.left_ref.store(storage)
        # self.right_ref.store(storage)

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

    @property
    def tree_ref(self):
        return self._tree_ref

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
                node = node.left#self._follow(node.left_ref)
            elif key > node.key:
                node = node.right #self._follow(node.right_ref)
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
        # TODO: Not sure if address is correct
        # self._tree_ref = self._insert(node, key, value_ref)
        self._tree_ref = BinaryNodeRef(address= self._storage.get_root_address(), referent=self._insert(node, key, value_ref))
    
    def _insert(self, node, key, value_ref):
        "insert a new node creating a new path from root"
        #create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                None, key, value_ref, None)
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left=self._insert(
                    node.left, key, value_ref))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right=self._insert(
                    node.right, key, value_ref))
        else: #create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return new_node

    def delete(self, key):
        "delete node with key, creating new tree and path"
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)
        
    def _delete(self, node, key):
        "underlying delete implementation"
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left=self._delete(
                    node.left, key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right=self._delete(
                    node.right, key))
        else:
            left = node.left
            right = node.right
            if left and right:
                replacement = self._find_max(left)
                left = self._delete(
                    node.left, replacement.key)
                new_node = BinaryNode(
                    left,
                    replacement.key,
                    replacement.value_ref,
                    node.right,
                )
            elif left:
                return node.left
            else:
                return node.right
        return new_node

    def _follow(self, ref):
        "get a node from a reference"
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        while True:
            next_node = node.right
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