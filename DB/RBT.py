import uuid


class Color(object):
    RED = 0
    BLACK = 1


class RedBlackTree(object):

    def __init__(self, left, value, right, color=Color.RED):
        self._color = color
        self._left = left
        self._right = right
        self._value = value
        self._count = 1 + len(left) + len(right)
        self._node_uuid = uuid.uuid4()

    def __len__(self):
        return self._count

    @property
    def uuid(self):
        return self._node_uuid

    @property
    def color(self):
        return self._color

    @property
    def value(self):
        return self._value

    @property
    def right(self):
        return self._right

    @property
    def left(self):
        return self._left

    def blacken(self):
        if self.is_red():
            return RedBlackTree(
                self.left,
                self.value,
                self.right,
                color=Color.BLACK,
            )
        return self

    def is_empty(self):
        return False

    def is_black(self):
        return self._color == Color.BLACK

    def is_red(self):
        return self._color == Color.RED

    def rotate_left(self):
        return RedBlackTree(
            RedBlackTree(
                self.left,
                self.value,
                EmptyRedBlackTree().update(self.right.left),
                color=self.color,
            ),
            self.right.value,
            self.right.right,
            color=self.right.color,
        )

    def rotate_right(self):
        return RedBlackTree(
            self.left.left,
            self.left.value,
            RedBlackTree(
                EmptyRedBlackTree().update(self.left.right),
                self.value,
                self.right,
                color=self.color,
            ),
            color=self.left.color,
        )

    def recolored(self):
        return RedBlackTree(
            self.left.blacken(),
            self.value,
            self.right.blacken(),
            color=Color.RED,
        )

    def balance(self):
        if self.is_red():
            return self

        if self.left.is_red():
            if self.right.is_red():
                return self.recolored()
            if self.left.left.is_red():
                return self.rotate_right().recolored()
            if self.left.right.is_red():
                return RedBlackTree(
                    self.left.rotate_left(),
                    self.value,
                    self.right,
                    color=self.color,
                ).rotate_right().recolored()
            return self

        if self.right.is_red():
            if self.right.right.is_red():
                return self.rotate_left().recolored()
            if self.right.left.is_red():
                return RedBlackTree(
                    self.left,
                    self.value,
                    self.right.rotate_right(),
                    color=self.color,
                ).rotate_left().recolored()
        return self

    def update(self, node):
        if node.is_empty():
            return self
        if node.value < self.value:
            return RedBlackTree(
                self.left.update(node).balance(),
                self.value,
                self.right,
                color=self.color,
            ).balance()
        return RedBlackTree(
            self.left,
            self.value,
            self.right.update(node).balance(),
            color=self.color,
        ).balance()

    def insert(self, value):
        return self.update(
            RedBlackTree(
                EmptyRedBlackTree(),
                value,
                EmptyRedBlackTree(),
                color=Color.RED,
            )
        ).blacken()

    def is_member(self, value):
        if value < self._value:
            return self.left.is_member(value)
        if value > self._value:
            return self.right.is_member(value)
        return True


class EmptyRedBlackTree(RedBlackTree):

    def __init__(self, storage):
        self._color = Color.BLACK
        self._storage = storage

    def is_empty(self):
        return True

    def insert(self, value):
        return RedBlackTree(
            EmptyRedBlackTree(),
            value,
            EmptyRedBlackTree(),
            color=Color.RED,
        )

    def update(self, node):
        return node

    def is_member(self, value):
        return False

    @property
    def left(self):
        return EmptyRedBlackTree()

    @property
    def right(self):
        return EmptyRedBlackTree()

    def __len__(self):
        return 0


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
        self._tree = EmptyRedBlackTree(self._storage)

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