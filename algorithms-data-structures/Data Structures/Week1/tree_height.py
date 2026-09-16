# python3
import sys
import threading

# Task. You are given a description of a rooted tree. Your task is to compute and output its height. Recall
# that the height of a (rooted) tree is the maximum depth of a node, or the maximum distance from a
# leaf to the root. You are given an arbitrary tree, not necessarily a binary tree.
# Input Format. The first line contains the number of nodes n. The second line contains n integer numbers
# from −1 to n-1 — parents of nodes. If the i-th one of them (0 <= i <= n − 1) is −1, node i is the root,
# otherwise it’s 0-based index of the parent of i-th node. It is guaranteed that there is exactly one root.
# It is guaranteed that the input represents a tree.
# Output Format. Output the height of the tree.


class node:  # Standard implementation of tree & node
    def __init__(self):
        self.child = []
        self.parent = None
        self.key = None


class tree:
    def __init__(self):
        self.root = None
        self.node = []


def get_height(tree, t_node):  # Standard implementation of tree height calculation
    if t_node.child == []:
        return 0
    return 1 + max(
        [get_height(tree, tree.node[t_node.child[i]]) for i in range(len(t_node.child))]
    )


def fast_compute_height(n, parents):  # It takes O(n) because there are two for-loops
    # First, we need to construct the nodes and the link the nodes to their parents
    t = tree()  # It's an empty tree
    for i in range(n):
        t_node = node()  # Create an empty node
        t_node.key = i  # Set the key in ascending order
        t_node.parent = parents[
            i
        ]  # parents is a given array, parents[index] return the parent of child with key index
        if (
            t_node.parent == -1
        ):  # If parents[index] == -1, then this node is the root of the tree
            t.root = t_node
            t.node.append(t.root)
        else:
            t.node.append(t_node)
    # Second, we need to link the parents with their children nodes
    for i in range(n):
        parent_index = t.node[i].parent
        if parent_index != -1:
            parent_node = t.node[parent_index]
            parent_node.child.append(i)
    return (
        get_height(t, t.root) + 1
    )  # At last, the tree is passed to standard implementation of tree height function


def main():
    n = int(input())
    parents = list(map(int, input().split()))
    print(fast_compute_height(n, parents))


# In Python, the default limit on recursion depth is rather low,
# so raise it here for this problem. Note that to take advantage
# of bigger stack, we have to launch the computation in a new thread.
sys.setrecursionlimit(10**7)  # max depth of recursion
threading.stack_size(2**30)  # new thread will get stack of such size
threading.Thread(target=main).start()
