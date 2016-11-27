from RBT import *

new_tree = EmptyRedBlackTree().insert(10)
assert isinstance(new_tree, RedBlackTree)
new_tree = new_tree.insert(11)
new_tree = new_tree.insert(12)

assert new_tree.value == 11
assert new_tree.left.value == 10
assert new_tree.right.value == 12