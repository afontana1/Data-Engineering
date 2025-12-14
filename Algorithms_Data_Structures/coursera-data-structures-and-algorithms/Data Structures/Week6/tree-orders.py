# python3
import sys, threading

sys.setrecursionlimit(10**6)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size
# Task. You are given a rooted binary tree. Build and output its in-order, pre-order and post-order traversals.
# Input Format. The first line contains the number of vertices n. The vertices of the tree are numbered
# from 0 to n − 1. Vertex 0 is the root.
# The next n lines contain information about vertices 0, 1, ..., n−1 in order. Each of these lines contains
# three integers key[i], left[i] and right[i] — key[i] is the key of the i-th vertex, left[i] is the index of the left
# child of the i-th vertex, and right[i] is the index of the right child of the i-th vertex. If i doesn’t have
# left or right child (or both), the corresponding left[i] or right[i] (or both) will be equal to −1.
# Output Format. Print three lines. The first line should contain the keys of the vertices in the in-order
# traversal of the tree. The second line should contain the keys of the vertices in the pre-order traversal
# of the tree. The third line should contain the keys of the vertices in the post-order traversal of the tree.


class TreeOrders:
    def read(self):  # Read input and build a binary tree
        self.n = int(sys.stdin.readline())  # Number of vertices - n
        self.key = [0 for i in range(self.n)]  # Key of each vertex
        self.left = [0 for i in range(self.n)]  # Left child index of each vertex
        self.right = [0 for i in range(self.n)]  # Right child index of each vertex

        for i in range(self.n):
            [a, b, c] = map(
                int, sys.stdin.readline().split()
            )  # Update self.key, self.left, self.right from each input line
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c

    def inOrderTraversal(
        self, i, result
    ):  # Standard implementation of in-order traversal, https://en.wikipedia.org/wiki/Tree_traversal
        if i == -1:
            return None
        self.inOrderTraversal(self.left[i], result)
        result.append(self.key[i])
        self.inOrderTraversal(self.right[i], result)
        return result

    def preOrderTraversal(
        self, i, result
    ):  # Standard implementation of pre-order traversal, https://en.wikipedia.org/wiki/Tree_traversal
        if i == -1:
            return None
        result.append(self.key[i])
        self.preOrderTraversal(self.left[i], result)
        self.preOrderTraversal(self.right[i], result)
        return result

    def postOrderTraversal(
        self, i, result
    ):  # Standard implementation of post-order traversal, https://en.wikipedia.org/wiki/Tree_traversal
        if i == -1:
            return None
        self.postOrderTraversal(self.left[i], result)
        self.postOrderTraversal(self.right[i], result)
        result.append(self.key[i])
        return result


def main():
    tree = TreeOrders()
    tree.read()
    print(" ".join(str(x) for x in tree.inOrderTraversal(0, list())))
    print(" ".join(str(x) for x in tree.preOrderTraversal(0, list())))
    print(" ".join(str(x) for x in tree.postOrderTraversal(0, list())))


threading.Thread(target=main).start()
