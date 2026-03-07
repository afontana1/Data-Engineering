# python3
import sys
from collections import deque

# Task. You are given a string S and you have to process n queries. Each query is described by three integers
# i, j, k and means to cut substring S[i...j] (i and j are 0-based) from the string and then insert it after the
# k-th symbol of the remaining string (if the symbols are numbered from 1). If k = 0, S[i...j] is inserted
# in the beginning. See the examples for further clarification.
# Input Format. The first line contains the initial string S.
# The second line contains the number of queries q.
# Next q lines contain triples of integers i, j, k.
# Output Format. Output the string after all q queries.


class Vertex:
    def __init__(self, key, size, left, right, parent):
        # Each vertex has several fields
        # self.key stores the index of character, self.size stores the number of nodes of its children, self.left points to its left child
        # self.right points to its right child, self.parent points to its parent
        (self.key, self.size, self.left, self.right, self.parent) = (
            key,
            size,
            left,
            right,
            parent,
        )


# Function of splay tree
def update(v):
    # This function updates v.sum, v.left.parent and v.right.parent
    if v == None:  # Make sure v is not a null vertex
        return
    v.size = (
        1
        + (v.left.size if v.left != None else 0)
        + (v.right.size if v.right != None else 0)
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


def order_stat(
    root, key
):  # Given key, return the order statistic corresponding to the key in a string
    v = root  # Starts at the root
    last = root  # The last accessed node is the root
    next = None  # Initialize with None, next represents the next element
    s = 1  # Number of elements smaller or equal to v (k-th order statistic)
    w = 0  # Number of elements smaller of equal to next
    if v == None:  # If v = None, then root = None, nothing we can search for
        return None, root
    while v != None:
        if (
            v.left != None
        ):  # If it has left child, then k-th order statistic is 1 + k-th order statistic of left child
            s = v.left.size + 1
        else:  # If it has no left child, it is the leftmost element with order statistic 1
            s = 1
        if next != None:  # Same as v
            if next.left != None:
                w = next.left.size + 1
            else:
                w = 1
        if s >= key and (
            next == None or s < w
        ):  # Initialize next variable for first iteration or the case that key <= s < w
            next = v
        last = v  # Update last accessed element in while loop
        if (
            s == key
        ):  # The k-th order statistic is found, break the loop and return the found node
            break
        if (
            s < key
        ):  # If s < k, we should search for the right subtree of v and it becomes (k-s)-th order statistic
            key -= s
            v = v.right
        else:  # If s > k, we should search for the left subtree of v and no change in order statistic
            v = v.left
    root = splay(
        last
    )  # Splay the last accessed node for each loop to maintain splay tree property
    return (next, root)


def split(
    root, key
):  # Given root and key, split the splay tree into 2 at the node with given key
    result, root = order_stat(root, key)
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


def in_order_traversal(
    root, s
):  # An iterative algorithm for in-order traversal of BST: https://www.techiedelight.com/inorder-tree-traversal-iterative-recursive/
    v = root
    stack = deque()
    while v != None or len(stack) > 0:
        if v != None:
            stack.append(v)
            v = v.left
        else:
            v = stack.pop()
            print(
                s[v.key - 1], end=""
            )  # Remember to subtract 1 because python string is 0-based but we are using 1-based index
            v = v.right


root = None  # Initialize the root be None


def insert(x):  # add(i) - see set_range_sum.py
    global root
    (left, right) = split(root, x)
    new_vertex = None
    if right == None or right.key != x:  # Define a new node for give key
        new_vertex = Vertex(x, 1, None, None, None)
    root = merge(merge(left, new_vertex), right)  # Update the root


class Rope:
    def __init__(self, s):
        global root
        self.s = s  # input string
        self.root = root  # default = None
        for ind in range(len(s)):
            insert(
                ind + 1
            )  # 1-based index. Otherwise, the first character will be put to the end when traversing the tree

    def result(self):
        global root
        self.root = root
        in_order_traversal(
            self.root, self.s
        )  # Print the resulting string during traversing. It keeps O(log(n)) running time

    def process(self, i, j, k):
        global root
        middle, right = split(
            root, j + 1 + 1
        )  # Adjust for 1-based index. As we need to extract S[i...j], the root of right tree is at least j + 1
        left, middle = split(
            middle, i + 1
        )  # Adjust for 1-based index. As we need to extract S[i...j], the root of middle tree is at least i
        left, right = split(
            merge(left, right), k + 1
        )  # merge(left, right) gives string with S[i...j] removed. Split it at k so that we can paste before the k-th symbol
        root = merge(
            merge(left, middle), right
        )  # root of right tree is at least k. So, we are now concatenate S[0...k-1]S[i...j]S[k...len(S) - 1] together.
        return


rope = Rope(sys.stdin.readline().strip())
q = int(sys.stdin.readline())
for _ in range(q):
    i, j, k = map(int, sys.stdin.readline().strip().split())
    rope.process(i, j, k)
rope.result()  # Default starting file has print() statement but rope.result() does not return anything. Thus, we don't need print() statement here.
