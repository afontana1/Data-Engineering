# python3
from sys import stdin

# Task. Implement a data structure that stores a set S of integers with the following allowed operations:
# 1. add(i) — add integer i into the set S (if it was there already, the set doesn’t change).
# 2. del(i) — remove integer i from the set S (if there was no such element, nothing happens).
# 3. find(i) — check whether i is in the set S or not.
# 4. sum(l, r) — output the sum of all elements v in S such that l <= v <= r.

# Splay tree implementation
# Vertex of a splay tree
class Vertex:
    def __init__(self, key, sum, left, right, parent):
        # Each vertex has several fields
        # self.key stores the value, self.sum stores the sum, self.left points to its left child
        # self.right points to its right child, self.parent points to its parent
        (self.key, self.sum, self.left, self.right, self.parent) = (
            key,
            sum,
            left,
            right,
            parent,
        )


# Function of splay tree
def update(v):
    # This function updates v.sum, v.left.parent and v.right.parent
    if v == None:  # Make sure v is not a null vertex
        return
    # sum of v = key associated with v + sum of left child + sum of right child
    # If v is a leaf, then v.sum = v.key
    v.sum = (
        v.key
        + (v.left.sum if v.left != None else 0)
        + (v.right.sum if v.right != None else 0)
    )
    if v.left != None:
        v.left.parent = v
    if v.right != None:
        v.right.parent = v


def smallRotation(v):
    # Zig
    parent = v.parent
    if parent == None:  # If it's a root, nothing to rotate
        return
    grandparent = v.parent.parent
    if parent.left == v:  # Case 1: v is a left child
        # Swap position between parent and v but maintain the BST condition
        #           parent
        #          /
        #         v
        #        / \
        #           m
        #
        #       v
        #      / \
        #       parent
        #       /
        #      m
        m = v.right
        v.right = parent
        parent.left = m
    else:  # Case 2: v is a right child
        # Swap position between parent and v but maintain the BST condition
        m = v.left
        v.left = parent
        parent.right = m
    update(parent)
    update(v)
    # Update the grandparent relationship after swapping v with its parent
    v.parent = grandparent
    if grandparent != None:
        if grandparent.left == parent:
            grandparent.left = v
        else:
            grandparent.right = v


def bigRotation(v):
    # bigRotation and smallRotation bring query node, v, close to the root
    if v.parent.left == v and v.parent.parent.left == v.parent:
        # Zig-zig if v is a left child and parent of v is also a left child
        # New order: v is a right child of v.parent, and v.parent.parent is a right child of v
        smallRotation(v.parent)
        smallRotation(v)
    elif v.parent.right == v and v.parent.parent.right == v.parent:
        # Zig-zig as well but opposite direction
        smallRotation(v.parent)
        smallRotation(v)
    else:
        # Zig-zag
        smallRotation(v)  # v.left = v.parent or v.right = v.parent
        smallRotation(v)  # v.left = v.parent.parent or v.right = v.parent.parent


# Makes splay of the given vertex and makes
# it the new root.
def splay(v):
    if v == None:  # trivial case
        return None
    while v.parent != None:  # If v is not the root
        if (
            v.parent.parent == None
        ):  # If v has no grandparent, swap v and v.parent and finish
            smallRotation(v)
            break
        bigRotation(v)  # Otherwise, swap v and v.parent and v.parent.parent
    return v


def find(
    root, key
):  # Given root and key, return the node with that key / smallest bigger key and root
    v = root
    last = root
    next = None  # If the given key is bigger than all key in the tree, return None
    while (
        v != None
    ):  # Terminate the node if v.right or v.left does not exist but v = v.right / v = v.left is called
        if v.key >= key and (next == None or v.key < next.key):
            # First iteration with v.key >= key, or not first iteration but next.key > v.key >= key
            next = v  # next is then the smallest bigger key
        last = v  # Last accessed node is v
        if v.key == key:  # If the key is found, done
            break
        if (
            v.key < key
        ):  # If v.key < key, search right subtree of v. Otherwise, search left subtree of v
            v = v.right
        else:
            v = v.left
    root = splay(last)  # splay the last accessed node (and maintain BST condition)
    return (next, root)


def split(
    root, key
):  # Given root and key, split the splay tree into 2 at the node with given key
    (result, root) = find(root, key)
    if (
        result == None
    ):  # If the given key is greater than all keys in the tree, left tree = current tree, right tree = None
        return (root, None)
    right = splay(result)  # Splay the results up to the root, split the tree at result
    left = (
        right.left
    )  # left tree has the root equal right.left, Right tree has the root equal result
    right.left = None
    if left != None:  # Remove the parent of the root of left tree
        left.parent = None
    update(left)  # Update sum and parent of left tree
    update(right)  # Update sum and parent of right tree
    return (left, right)


def merge(left, right):  # Given roots of two trees, merge them into a bigger tree
    if left == None:  # Trivial case
        return right
    if right == None:  # Trivial case
        return left
    while (
        right.left != None
    ):  # If the root of right tree has left child, define the root to be its leftmost child
        right = right.left
    right = splay(
        right
    )  # splay the the root of right tree (in case previous while loop has executed)
    right.left = left  # merge two tree (Note that right has no left child), and update sum and children nodes
    update(right)
    return right


root = None  # Initialize the root be None


def insert(x):  # add(i)
    global root
    (left, right) = split(root, x)
    new_vertex = None
    if right == None or right.key != x:  # Define a new node for give key
        new_vertex = Vertex(x, x, None, None, None)
    root = merge(merge(left, new_vertex), right)  # Update the root


def erase(x):  # First function to be implemented in assignment: del(i)
    global root
    (next, root) = find(root, x)  # Search for the node given key
    if next == None or next.key != x:  # Early stopping if there is no such node
        return
    (left, middle) = split(root, x)  # mid has key x or key larger than x
    (middle, right) = split(
        middle, x + 1
    )  # mid has key less than x + 1. There may be multiple nodes of the same key
    root = merge(left, right)


def search(x):  # Second function to be implemented in assignment: find(i)
    global root
    (next, root) = find(root, x)  # Search for the node given key
    if (
        next != None and next.key == x
    ):  # Return true only if the node has the same key as the given key
        return True
    return False  # Otherwise, return false


def sum(fr, to):  # Third function to be implemented in assignment: sum(l, r)
    global root
    (left, middle) = split(root, fr)  # The smallest element of middle >= from
    (middle, right) = split(middle, to + 1)  # The largest element of middle <= to
    ans = 0  # Default is 0
    if middle != None:
        ans = middle.sum  # If there exists node between fr and to, update the sum
    root = merge(merge(left, middle), right)  # Merge back the subtrees into a full tree
    return ans


MODULO = 1000000001
n = int(stdin.readline())
last_sum_result = 0
for i in range(n):
    line = stdin.readline().split()
    if line[0] == "+":
        x = int(line[1])
        insert((x + last_sum_result) % MODULO)
    elif line[0] == "-":
        x = int(line[1])
        erase((x + last_sum_result) % MODULO)
    elif line[0] == "?":
        x = int(line[1])
        print("Found" if search((x + last_sum_result) % MODULO) else "Not found")
    elif line[0] == "s":
        l = int(line[1])
        r = int(line[2])
        res = sum((l + last_sum_result) % MODULO, (r + last_sum_result) % MODULO)
        print(res)
        last_sum_result = res % MODULO
