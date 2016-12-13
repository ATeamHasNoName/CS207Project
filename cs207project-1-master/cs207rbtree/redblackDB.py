import pickle
import os
import struct
import portalocker

class ValueRef(object):
    """
    A class that stores a reference to a string value on disk

    Parameters
    ----------
    referent : string
        The value to store. Optional.
    address : int
        Address to store at; defaults to 0. Optional.

    Notes
    -----
    PRE:
    WARNINGS:
    """
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
        """
        Read bytes for value from disk.

        Parameters:
        -----------
        storage : storage object to read from.
        """
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        """
        Store bytes for value to disk.

        Parameters:
        -----------
        storage : storage object to write to.
        """
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))

class RedBlackNodeRef(ValueRef):
    """
    A class that stores a reference to a red black node on disk.

    Parameters
    ----------

    Notes
    -----
    PRE:
    WARNINGS:
    """
    
    def prepare_to_store(self, storage):
        """
        Have a node store its refs.
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """
        Use pickle to convert node to bytes.
        """
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'color': referent.color
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        Unpickle bytes to get a node object.
        """
        d = pickle.loads(string)
        return RedBlackNode(
            RedBlackNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            RedBlackNodeRef(address=d['right']),
            d['color']
        )
    
class RedBlackNode:
    """
    A red black node.

    Parameters
    ----------
    left_ref : pointer
        To left node.
    key : int
        The key should have a notion of less/greater than.
    value_ref : pointer
        To value.
    right_ref : int
        To right node.      
    color : 0,1
        Respectively 0=RED 1=BLACK.     

    Notes
    -----
    PRE:
    WARNINGS:
    """

    def __init__(self, left_ref, key, value_ref, right_ref, color):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color = color

    @classmethod
    def from_node(cls, node, **kwargs):
        """
        Clone a node with some changes from another one.
        """
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            color=kwargs.get('color', node.color)
        )

    def store_refs(self, storage):
        """
        Method for a node to store all of its stuff.
        """
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)

    def blacken(self):
        """
        Set color of a node to black.
        """
        if self.is_red():
            return self.from_node(
                self,
                color=Color.BLACK,
            )
        return self

    def is_black(self):
        """
        Check if color of a node is black.
        """
        return self.color == Color.BLACK

    def is_red(self):
        """
        Check if color of a node is red.
        """
        return self.color == Color.RED

class Color:
    RED = 0
    BLACK = 1

class RedBlackTree:
    """
    A red black tree.

    Parameters
    ----------

    Notes
    -----
    PRE:
    WARNINGS:
    """
    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        """
        Changes are final only when committed.
        """
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        """
        Get reference to new tree if it has changed.
        """
        self._tree_ref = RedBlackNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        """
        Get value for a key if tree is not locked by another writer.
        Refresh the references and get new tree if needed

        Parameters:
        -----------
        key : e.g. int, string. Depends on choice of key for RBT.
            Key to fetch.

        Raises:
        -------
            KeyError : if user searches for a key not in the RBT.
        """
        if not self._storage.locked:
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        while node is not None:
            if key < node.key:
                node = self.left(node)
            elif key > node.key:
                node = self.right(node)
            else:
                return self.value(node)
        raise KeyError
    
    def set(self, key, value):
        """
        Set a new value in the tree, causing a new tree.
        Try to lock the tree. If we succeed make sure we dont lose updates from any other process.

        Parameters:
        -----------
        key : e.g. int, string. Depends on choice of key for RBT.
            Key to associate a value.
        value : e.g. int, string. 

        """
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        self._tree_ref = self.insert(node, key, value_ref)

    def value(self, node):
        """
        Get value of node.
        """
        return self._follow(node.value_ref)

    def right(self, node):
        """
        Get node right of node.
        """
        return self._follow(node.right_ref)

    def left(self, node):
        """
        Get node left of node.
        """
        return self._follow(node.left_ref)

    def update(self, node, key, value_ref):
        """
        Setting in the RBT requires we maintain multiple properties.
        i. UPDATE. If key is less go left, if key is greater go right. 
        ii. BALANCE. Minimize worst case depth of the tree. If RBT balance conditions
            are violated, trigger ROTATE_LEFT, ROTATE_RIGHT and RECOLOR as appropriate.

        Parameters:
        -----------

        """
        if node is None:
            return RedBlackNodeRef(self.balance(RedBlackNode(
                RedBlackNodeRef(), 
                key, 
                value_ref, 
                RedBlackNodeRef(), 
                Color.RED)))
        elif key < node.key:
            return RedBlackNodeRef(self.balance(RedBlackNode.from_node(
                node,
                left_ref=self.update(self.left(node), key, value_ref))))
        elif node.key < key:
            return RedBlackNodeRef(self.balance(RedBlackNode.from_node(
                node,
                right_ref=self.update(self.right(node), key, value_ref))))
        elif key==node.key:
            # handling duplicates
            return RedBlackNodeRef(self.balance(RedBlackNode.from_node(
                node, value_ref=value_ref)))

    def rotate_left(self, node):
        """
        Rotation, balancing operation.

        Parameters:
        -----------

        """
        return RedBlackNode(
            RedBlackNodeRef(
                    RedBlackNode.from_node(
                    node,
                    right_ref=self.right(node).left_ref,
                )
            ),
            self.right(node).key,
            self.right(node).value_ref,
            self.right(node).right_ref,
            self.right(node).color,
        )

    def rotate_right(self, node):
        """
        Rotation, balancing operation.

        Parameters:
        -----------

        """
        return RedBlackNode(
            self.left(node).left_ref,
            self.left(node).key, 
            self.left(node).value_ref,
            RedBlackNodeRef(
                    RedBlackNode.from_node(
                    node,
                    left_ref=self.left(node).right_ref,
                )
            ),
            self.left(node).color,
        )

    def recolored(self, node):
        """
        Recoloring, balancing operation.

        Parameters:
        -----------

        """
        return RedBlackNode.from_node(
            node,
            left_ref=RedBlackNodeRef(self.left(node).blacken()),
            color=Color.RED,
            right_ref=RedBlackNodeRef(self.right(node).blacken()),
        )

    def balance(self, node):
        """
        Balance to minimize worst case depth of the tree.

        Parameters:
        -----------

        """
        if node.is_red():
            return node

        if self.left(node) is not None and self.left(node).is_red():
            if self.right(node) is not None and self.right(node).is_red():
                return self.recolored(node)
            if self.left(self.left(node)) is not None and self.left(self.left(node)).is_red():
                return self.recolored(self.rotate_right(node))
            if self.right(self.left(node)) is not None and self.right(self.left(node)).is_red():
                return self.recolored(self.rotate_right(
                    RedBlackNode.from_node(
                        node, 
                        left_ref=RedBlackNodeRef(self.rotate_left(self.left(node))),
                    )))
            return node

        if self.right(node) is not None and self.right(node).is_red():
            if self.right(self.right(node)) is not None and self.right(self.right(node)).is_red():
                return self.recolored(self.rotate_left(node))
            if self.left(self.right(node)) is not None and self.left(self.right(node)).is_red():
                return self.recolored(self.rotate_left(
                    RedBlackNode.from_node(
                        node,
                        right_ref=RedBlackNodeRef(self.rotate_right(self.right(node))),
                    )))
        return node

    def insert(self, node, key, value_ref):
        return RedBlackNodeRef(self._follow(self.update(
            node, 
            key, 
            value_ref)
        ).blacken())

    def _follow(self, ref):
        """
        Get a node from a reference
        """
        return ref.get(self._storage)
            
    def get_min(self):
        """
        Get minimum value in a tree.
        """
        node = self._follow(self._tree_ref)
        while True:
            next_node = self.left(node)
            if next_node is None:
                return self.value(node)
            node = next_node    
            
    def get_left(self, key):
        """
        Implementation parallels get().
        Get key-value pair left of a *key*.
        """
        if not self._storage.locked:
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        while node is not None:
            if key < node.key:
                node = self.left(node)
            elif key > node.key:
                node = self.right(node)
            else:
                node_left = self.left(node)
                return (node_left.key, self.value(node_left))
        raise KeyError

    def get_right(self, key):
        """
        Implementation parallels get().
        Get key-value pair right of a *key*.
        """
        if not self._storage.locked:
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        while node is not None:
            if key < node.key:
                node = self.left(node)
            elif key > node.key:
                node = self.right(node)
            else:
                node_right = self.right(node)
                return (node_right.key, self.value(node_right))
        raise KeyError

    def traverse_in_order(self, node):
        """
        Traverse the children of a node returning visited nodes in a list.

        Parameters:
        -----------
        node : subtree root

        Returns
        -----------
        out_global : list of nodes in subtree
        """
        out_global = []
        def traverse_enclosed(node):
            if node is None:
                return
            traverse_enclosed(self.left(node))
            out_global.append((node.key, self.value(node)))
            traverse_enclosed(self.right(node))
        traverse_enclosed(node)
        return out_global

    def chop(self, chop_key):
        """
        Get all keys less than the chop_key.
        e.g. chopping on 4 returns all nodes with key <=4.

        Returns
        -----------
        out : list of nodes with key less than chop_key
        """
        # returns a list of key-vals with key's less than or equal to chop_key
        nodes_to_expand = []
        if not self._storage.locked:
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            parent_node = node
            if chop_key < node.key:
                node = self.left(node)
            elif chop_key > node.key:
                # take note any time we turn right. we will need to backtrack to these nodes
                if self.right(node) is not None:
                    nodes_to_expand.append(node)
                node = self.right(node)
            else:
                node = None
        # at this point parent_node stores our best approx position of chop_key in tree
        nodes_to_expand.append(parent_node)
        out = []
        # at parent node collect left subtree
        # then backtrack to all instances where we turned right
        for node in nodes_to_expand:
            if node.key<=chop_key:
                out.append((node.key, self.value(node)))
            out = out + self.traverse_in_order(self.left(node))
        return out

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

    # documentation for parallel methods in RedBlackTree() class.
    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = RedBlackTree(self._storage)

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
    
    def get_min(self):
        self._assert_not_closed()
        return self._tree.get_min()
    
    def get_left(self, key):
        self._assert_not_closed()
        return self._tree.get_left(key)

    def get_right(self, key):
        self._assert_not_closed()
        return self._tree.get_right(key)

    def chop(self, chop_key):
        self._assert_not_closed()
        return self._tree.chop(chop_key)

    # METHODS FOR PLOTTING RED BLACK TREE
    def root_key(self):
        """
        Returns key at root
        """
        return self._tree._follow(self._tree._tree_ref).key

    def first_generation_children(self, key):
        """
        Returns a list of the left key-value tuple and the right key-value tuple.
        Returns None if empty node.
        """
        out = []
        try:
            out.append(db.get_left(key))
        except:
            out.append('None')
        try:
            out.append(db.get_right(key))
        except:
            out.append('None')
        return out

    def _print_tree(self):
        """
        DEBUGGING METHOD ONLY
        PRINTS THE TREE IN AN INEFFICIENT FASHION
        """
        root_node = self._tree._follow(self._tree._tree_ref)
        tree_list = self._tree.traverse_in_order(root_node)

        print("root key = "+str(self.root_key())+"\n") 
        for key, val in tree_list:
            print(str(key)+' left: '+str(self.first_generation_children(key)))
            print(str(key)+' right: '+str(self.first_generation_children(key))+"\n")           

def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)
