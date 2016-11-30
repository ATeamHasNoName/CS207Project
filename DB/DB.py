class ValueRef(object):
    """
    A reference to a string value on disk.
    """
    def __init__(self, referent=None, address=0):
        """
        Initializes a value reference that takes in a referent (BinaryNode) and the address in disk.

        Parameters
        ----------
        referent: Node
        address: Address of the stored node

        Returns
        -------
        None
        
        >>> ref = ValueRef()
        >>> type(ref)
        <class 'DB.ValueRef'>
        """
        self._referent = referent #value to store
        self._address = address # address to store at
        
    @property
    def address(self):
        """
        Address on disk for this value.
        """
        return self._address
    
    def prepare_to_store(self, storage):
        """
        Used in subclass BinaryNodeRef to store refs in provided Storage.
        """
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """
        Converts referent data (as a utf-8 string) to bytes.

        Parameters
        ----------
        referent: Node

        Returns
        -------
        Bytes
        
        >>> ref = ValueRef()
        >>> referent = '1'
        >>> ref.referent_to_bytes(referent)
        b'1'
        """
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        """
        Converts byte data to utf-8 string.

        Parameters
        ----------
        referent: Node

        Returns
        -------
        Bytes
        
        >>> ref = ValueRef()
        >>> referent = '1'
        >>> bytes = ref.referent_to_bytes(referent)
        >>> ref.bytes_to_referent(bytes)
        '1'
        """
        return bytes.decode('utf-8')

    def get(self, storage):
        """
        Get bytes from storage at this ref's address and convert the bytes to a utf-8 string.

        Parameters
        ----------
        storage

        Returns
        -------
        utf-8 string
        
        >>> ref = ValueRef()
        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> ref._referent = '123'
        >>> ref.store(storage)
        >>> ref.get(storage)
        '123'
        >>> os.remove('test.dbdb')
        """
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        """
        Get utf-8 string from this ref's referent and convert to bytes to store in storage.

        Parameters
        ----------
        storage

        Returns
        -------
        None
        
        >>> ref = ValueRef()
        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> ref._referent = ''
        >>> ref.store(storage)
        >>> ref.get(storage)
        ''
        >>> os.remove('test.dbdb')
        """
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


import pickle
class BinaryNodeRef(ValueRef):
    """
    A reference to a btree node on disk. Subclass of ValueRef.
    """
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        """
        Have a node store its refs, similar functionality as ValueRef's store

        Parameters
        ----------
        storage

        Returns
        -------
        None
        
        >>> ref = BinaryNodeRef()
        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> ref._referent = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef())
        >>> ref.prepare_to_store(storage)
        >>> node = ref.get(storage)
        >>> type(node)
        <class 'DB.BinaryNode'>
        >>> node.key
        '1'
        >>> os.remove('test.dbdb')
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """
        Override superclass referent_to_bytes to convert a BinaryNode referent to bytes using pickle

        Parameters
        ----------
        referent

        Returns
        -------
        Bytes
        
        >>> ref = BinaryNodeRef()
        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> referent = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef())
        >>> type(ref.referent_to_bytes(referent))
        <class 'bytes'>
        >>> os.remove('test.dbdb')
        """

        "use pickle to convert node to bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        Override superclass bytes_to_referent to convert bytes to a BinaryNode using pickle

        Parameters
        ----------
        referent

        Returns
        -------
        BinaryNode
        
        >>> ref = BinaryNodeRef()
        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> referent = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef())
        >>> bytes = ref.referent_to_bytes(referent)
        >>> node = ref.bytes_to_referent(bytes)
        >>> type(node)
        <class 'DB.BinaryNode'>
        >>> node.key
        '1'
        >>> os.remove('test.dbdb')
        """
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )

class Color(object):
    """
    Color class for BinaryNode in Red Black Tree. Color can either be RED or BLACK.
    """
    RED = 0
    BLACK = 1
    
class BinaryNode(object):
    """
    Binary node in a Red Black Tree. 
    Node has a left_ref, key, value_ref, right_ref and a default color of RED.
    """

    @classmethod
    def from_node(cls, node, **kwargs):
        """
        Alternative way to initialize a BinaryNode from another node, while changing some parameters.
        """
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color=kwargs.get('color', node.color)
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color=Color.RED):
        """
        Initializes a BinaryNode

        Parameters
        ----------
        left_ref: BinaryNodeRef with key lesser than this node's key
        key: string
        value_ref: ValueRef containing string value referent
        right_ref: BinaryNodeRef with key greater than this node's key
        color: Color of Red Black Tree node, either RED or BLACK. Defaults to RED.

        Returns
        -------
        None
        
        >>> node = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef())
        >>> type(node)
        <class 'DB.BinaryNode'>
        >>> node.key
        '1'
        """
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color = color

    def is_red(self):
        """
        Returns true if the node is red, else false

        Parameters
        ----------
        None

        Returns
        -------
        True if node is red, else false
        
        >>> node = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef(), color=Color.RED)
        >>> node.is_red()
        True
        """
        return self.color == Color.RED

    def is_black(self):
        """
        Returns true if the node is black, else false

        Parameters
        ----------
        None

        Returns
        -------
        True if node is black, else false
        
        >>> node = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef(), color=Color.BLACK)
        >>> node.is_black()
        True
        """
        return self.color == Color.BLACK

    # If node is red, returns a black version of the node
    def blacken(self):
        """
        If node is red, returns a black version of the node, otherwise just return self

        Parameters
        ----------
        None

        Returns
        -------
        True if node is black, else false
        
        >>> node = BinaryNode(ValueRef(), '1', ValueRef(), ValueRef(), color=Color.RED)
        >>> node = node.blacken()
        >>> node.color
        1
        """
        if self.is_red():
            return BinaryNode.from_node(self, color=Color.BLACK)
        else:
            return self
    
    def rotate_left(self):
        """
        Rotates a node along its left axis.

        Parameters
        ----------
        None

        Returns
        -------
        self, that has been rotated along the left axis

        >>> leftRef = BinaryNodeRef(referent=BinaryNode(ValueRef(), '1', ValueRef(), ValueRef(), color=Color.RED))
        >>> rightRef = BinaryNodeRef(referent=BinaryNode(ValueRef(), '3', ValueRef(), ValueRef(), color=Color.RED))
        >>> node = BinaryNode(leftRef, '2', ValueRef(), rightRef, color=Color.RED)
        >>> node = node.rotate_left()
        >>> node.key
        '3'
        """
        # Rotate around right node
        rightNode = self.right_ref._referent
        # Get new left ref
        leftNode = BinaryNode(self.left_ref, self.key, self.value_ref, rightNode.left_ref, color=self.color)
        newLeftRef = BinaryNodeRef(referent=leftNode)
        return BinaryNode(newLeftRef, rightNode.key, rightNode.value_ref, rightNode.right_ref, color=rightNode.color)

    def rotate_right(self):
        """
        Rotates a node along its right axis.

        Parameters
        ----------
        None

        Returns
        -------
        self, that has been rotated along the right axis

        >>> leftRef = BinaryNodeRef(referent=BinaryNode(ValueRef(), '1', ValueRef(), ValueRef(), color=Color.RED))
        >>> rightRef = BinaryNodeRef(referent=BinaryNode(ValueRef(), '3', ValueRef(), ValueRef(), color=Color.RED))
        >>> node = BinaryNode(leftRef, '2', ValueRef(), rightRef, color=Color.RED)
        >>> node = node.rotate_right()
        >>> node.key
        '1'
        """
        # Rotate around left node
        leftNode = self.left_ref._referent
        # Get new right ref
        rightNode = BinaryNode(leftNode.right_ref, self.key, self.value_ref, self.right_ref, color=self.color)
        newRightRef = BinaryNodeRef(referent=rightNode)
        return BinaryNode(leftNode.left_ref, leftNode.key, leftNode.value_ref, newRightRef, color=leftNode.color)

    def recolored(self):
        """
        Blacken left and right nodes, while setting own color to be red.

        Parameters
        ----------
        None

        Returns
        -------
        self, that has both left and right node blackened, and own color set to red.

        >>> leftRef = BinaryNodeRef(referent=BinaryNode(ValueRef(), '1', ValueRef(), ValueRef(), color=Color.RED))
        >>> rightRef = BinaryNodeRef(referent=BinaryNode(ValueRef(), '3', ValueRef(), ValueRef(), color=Color.RED))
        >>> node = BinaryNode(leftRef, '2', ValueRef(), rightRef, color=Color.RED)
        >>> node = node.recolored()
        >>> leftNode = node.left_ref._referent
        >>> leftNode.color
        1
        >>> rightNode = node.right_ref._referent
        >>> rightNode.color
        1
        """
        # Blacken left and right nodes
        leftNode = self.left_ref._referent
        rightNode = self.right_ref._referent
        leftRef = self.left_ref
        rightRef = self.right_ref
        if leftNode is not None:
            leftRef = BinaryNodeRef(referent=leftNode.blacken())
        if rightNode is not None:
            rightRef = BinaryNodeRef(referent=rightNode.blacken())
        return BinaryNode(leftRef, self.key, self.value_ref, rightRef, color=Color.RED)

    def balance(self):
        """
        Balances the subtree rooted at this node, using its Red Black Tree property.

        Parameters
        ----------
        None

        Returns
        -------
        self, that has been balanced.
        """
        # If red, no need to rebalance
        if self.is_red():
            return self

        # Get all the necessary nodes first
        leftNode = self.left_ref._referent
        rightNode = self.right_ref._referent
        leftOfLeftNode = rightOfLeftNode = leftOfRightNode = rightOfRightNode = None
        if leftNode is not None:
            leftOfLeftNode = leftNode.left_ref._referent
            rightOfLeftNode = leftNode.right_ref._referent
        if rightNode is not None:
            leftOfRightNode = rightNode.left_ref._referent
            rightOfRightNode = rightNode.right_ref._referent

        # Perform the rebalancing
        
        # On the left node
        if leftNode is not None and leftNode.is_red():
            if rightNode is not None and rightNode.is_red():
                return self.recolored()
            if leftOfLeftNode is not None and leftOfLeftNode.is_red():
                return self.rotate_right().recolored()
            if rightOfLeftNode is not None and rightOfLeftNode.is_red():
                newLeftNode = leftNode.rotate_left()
                newLeftRef = BinaryNodeRef(referent=newLeftNode)
                return BinaryNode(newLeftRef, self.key, self.value_ref, self.right_ref, color=self.color).rotate_right().recolored()
            return self

        # On the right node
        if rightNode is not None and rightNode.is_red():
            if rightOfRightNode is not None and rightOfRightNode.is_red():
                return self.rotate_left().recolored()
            if leftOfRightNode is not None and leftOfRightNode.is_red():
                newRightNode = rightNode.rotate_right()
                newRightRef = BinaryNodeRef(referent=newRightNode)
                return BinaryNode(self.left_ref, self.key, self.value_ref, newRightRef, color=self.color).rotate_left().recolored()

        # No balancing needed, just return self
        return self

    def store_refs(self, storage):
        """
        Method for node to store its all refs into provided storage.
        Store calls the ref's prepare_to_store which recursively stores the whole tree.

        Parameters
        ----------
        None

        Returns
        -------
        self, that has both left and right node blackened, and own color set to red.

        >>> ref = ValueRef()
        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> ref._referent = '123'
        >>> node = BinaryNode(ValueRef(), '1', ref, ValueRef())
        >>> node.store_refs(storage)
        >>> node.value_ref.get(storage)
        '123'
        >>> os.remove('test.dbdb')
        """
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class BinaryTree(object):
    """
    Immutable Binary Tree class, where a new tree is constructed on changes.
    """
    def __init__(self, storage):
        """
        Initializes a binary tree from a provided storage. This tree is also a Red Black Tree, and is balanced.

        Parameters
        ----------
        storage

        Returns
        -------
        None

        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> btree = BinaryTree(storage)
        >>> type(btree)
        <class 'DB.BinaryTree'>
        >>> os.remove('test.dbdb')
        """
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        """
        Changes are persisted after commit is called. This stores the root into disk.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        # Make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        """
        Get reference to new tree if it has changed.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        """
        Returns the node with the input key

        Parameters
        ----------
        key: String key

        Returns
        -------
        BinaryNode with that key

        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> btree = BinaryTree(storage)
        >>> btree.set('1', '2')
        >>> btree.get('1')
        '2'
        """
        # If tree is not locked by another writer
        # Refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        # Get the top level node
        node = self._follow(self._tree_ref)
        # Traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        print("Key is not in Database\n")
        return KeyError

    def set(self, key, value):
        """
        Sets a new value in the tree with associated key.
        Balancing is also done upon set.

        Parameters
        ----------
        key: String key
        value: String value

        Returns
        -------
        None

        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> btree = BinaryTree(storage)
        >>> btree.set('1', '2')
        >>> btree.set('2', '3')
        >>> btree.get('2')
        '3'
        """
        # Lock the tree and make sure updates from any other process is not lost
        if self._storage.lock():
            self._refresh_tree_ref()

        # Get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        self._tree_ref = self._insert(node, key, value_ref)

        # Blacken tree node
        treeNode = self._tree_ref._referent
        balancedTreeNode = treeNode.blacken()
        self._tree_ref = BinaryNodeRef(referent=balancedTreeNode, address=self._tree_ref.address)
        
    def _insert(self, node, key, value_ref):
        """
        Recursive helper function that inserts key and value_ref into the tree.
        Used by set.
        Does balancing along the way.

        Parameters
        ----------
        node: current BinaryNode 
        key: String key
        value_ref: BinaryNodeRef encapsulating value

        Returns
        -------
        BinaryNodeRef with node after insertion

        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> btree = BinaryTree(storage)
        >>> root = btree._follow(btree._tree_ref)
        >>> value_ref = ValueRef('2')
        >>> btree._tree_ref = btree._insert(root, '1', value_ref)
        >>> btree._tree_ref._referent.key
        '1'
        """
        #create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                BinaryNodeRef(), key, value_ref, BinaryNodeRef(), color=Color.RED)
        elif key < node.key:
            leftNode = self._follow(node.left_ref)
            if leftNode is not None:
                leftNode = leftNode.balance()
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(leftNode, key, value_ref)
                )
        elif key > node.key:
            rightNode = self._follow(node.right_ref)
            if rightNode is not None:
                rightNode = rightNode.balance()
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(rightNode, key, value_ref)
                )
        else: #create a new node to represent this data
            new_node = BinaryNode.from_node(node.balance(), value_ref=value_ref, key=key)
            
        return BinaryNodeRef(referent=new_node.balance())

    def _follow(self, ref):
        """
        Private helper function that gets a node from the reference, from storage by calling BinaryNodeRef's get.

        Parameters
        ----------
        ref: BinaryNodeRef

        Returns
        -------
        BinaryNode from storage

        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> btree = BinaryTree(storage)
        >>> btree.set('1', '2')
        >>> btree.set('2', '3')
        >>> root = btree._follow(btree._tree_ref)
        >>> root.key
        '1'
        """
        return ref.get(self._storage)
    
    def _find_max(self, node):
        """
        Find the max value in the subtree of the input node, by traversing to the right most child

        Parameters
        ----------
        ref: BinaryNodeRef

        Returns
        -------
        BinaryNode from storage

        >>> dbdb = DB.connect('test.dbdb')
        >>> storage = dbdb._storage
        >>> btree = BinaryTree(storage)
        >>> btree.set('1', '2')
        >>> btree.set('2', '3')
        >>> btree.set('3', '4')
        >>> root = btree._follow(btree._tree_ref)
        >>> maxNode = btree._find_max(root)
        >>> maxNode.key
        '3'
        """
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node

import os
import struct

import portalocker

class Storage(object):
    """
    Storage class that handles locking and storing of times and values on disk.
    """
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        """
        Initializes storage from a file

        Parameters
        ----------
        f: File

        Returns
        -------
        None
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> type(storage)
        <class 'DB.Storage'>
        >>> os.remove('test.dbdb')
        """
        self._f = f
        self.locked = False
        # We ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        """
        Guarantees that the next write will start on a sector boundary

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        """
        If it's not locked, lock the file for writing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> storage.lock()
        True
        """
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        """
        If it's locked, flush and unlock.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> storage.lock()
        True
        >>> storage.unlock()
        >>> storage.locked
        False
        """
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        """
        Go to the end of the file
        """
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        """
        Go to the beginning of the file which is on sec boundary
        """
        if (self.closed == False):
            self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        """
        Convert bytes to integer 

        Parameters
        ----------
        integer_bytes: Bytes

        Returns
        -------
        Integer
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> storage._bytes_to_integer(b'12345678')
        3544952156018063160
        """
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        """
        Convert integer to integer bytes

        Parameters
        ----------
        integer

        Returns
        -------
        Integer bytes
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> integer_bytes = storage._bytes_to_integer(b'12345678')
        >>> storage._integer_to_bytes(integer_bytes)
        b'12345678'
        """
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        """
        Private helper function used by read(address) to read in an integer
        """
        if self.closed == False:
            return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        """
        Private helper function used by write(data) to lock and write an integer
        """
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        """
        Write data to disk, returning the adress at which you wrote it
        First lock, get to end, get address to return, write size

        Parameters
        ----------
        data

        Returns
        -------
        address
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> address = storage.write(b'12345678')
        >>> type(address)
        <class 'int'>
        """
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        """
        Write data to disk, returning the adress at which you wrote it
        First lock, get to end, get address to return, write size

        Parameters
        ----------
        data

        Returns
        -------
        address
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> address = storage.write(b'12345678')
        >>> storage.read(address)
        b'12345678'
        """
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        """
        Lock, write root address at position 0, then unlock.
        Write is atomic because we store the address on a sector boundary.
        """
        self.lock()
        self._f.flush()
        self._seek_superblock()
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        """
        Get root address, which is the first integer in the file
        """
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        """
        Close the storage by unlocking it and closing the disk (file)
        """
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        """
        Returns true if storage is closed, false otherwise

        Parameters
        ----------
        None

        Returns
        -------
        True if storage closed, False otherwise
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> storage = Storage(f)
        >>> storage.closed
        False
        >>> storage.close()
        >>> storage.closed
        True
        """
        return self._f.closed

class DBDB(object):
    """
    DBDB class which contains both the tree and its associated storage (disk)
    Functions are just wrappers around both tree and storage.
    """

    def __init__(self, f):
        """
        Initializes DBDB with a file, then creates the tree and its associated storage

        Parameters
        ----------
        f: File

        Returns
        -------
        None
        
        >>> try:
        ...     f = open('test.dbdb', 'r+b')
        ... except IOError:
        ...     fd = os.open('test.dbdb', os.O_RDWR | os.O_CREAT)
        ...     f = os.fdopen(fd, 'r+b')
        >>> dbdb = DBDB(f)
        >>> type(dbdb)
        <class 'DB.DBDB'>
        """
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        """
        Raises an error when associated storage is closed
        """
        if self._storage.closed:
            return ValueError('Database closed.')

    def close(self):
        """
        Closes associated storage
        """
        self._storage.close()

    def commit(self):
        """
        Commits changes to the tree
        """
        self._assert_not_closed()
        #if self._storage.closed != False:
        self._tree.commit()

    def get(self, key):
        """
        Get the value associated at the key from the tree
        """
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        """
        Set the valye at the associated key in the tree
        """
        self._assert_not_closed()
        if self._storage.closed:
            return
        return self._tree.set(key, value)

import os
class DB(object):
    """
    Class that connects to the db (filename) and returns a DBDB object that has both the tree and its 
    associated storage.
    """
    def connect(dbname):
        try:
            f = open(dbname, 'r+b')
        except IOError:
            fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, 'r+b')
        return DBDB(f)
