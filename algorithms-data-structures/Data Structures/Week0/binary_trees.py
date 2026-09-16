class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST(object):
    """Binary search tree implementation
    Important properties:
    - BST's have at most two children
    - Depth is measured as distance from the root to a specific node
    - The length from n to its deepest descendant

    Types:
    - Complete: every level except possibly the last is completed filled, and all nodes
                            in the last level are as far left as possible
    - Full: a tree in which every node has either 0 or 2 children

    Property of BST:
    - The value of the left child of any node in a binary search tree will be less
      than whatever value we have in that node, and the value to the right will
      be greater than what we have in that node
    """

    def __init__(self, value):
        self.root = Node(value)

    def depth_first_preorder(self, start, traversal):
        if start:
            traversal += str(start.value) + "-"
            traversal = self.depth_first_preorder(start.left, traversal)
            traversal = self.depth_first_preorder(start.right, traversal)
        return traversal

    def depth_in_order(self, start, traversal):
        if start:
            traversal = self.depth_in_order(start.left, traversal)
            traversal += str(start.value) + "-"
            traversal = self.depth_in_order(start.right, traversal)
        return traversal

    def depth_post_order(self, start, traversal):
        if start:
            traversal = self.depth_post_order(start.left, traversal)
            traversal = self.depth_post_order(start.right, traversal)
            traversal += str(start.value) + "-"
        return traversal

    def level_order(self, start):
        if start is None:
            return
        queue = []
        queue.insert(0, start)
        traversal = ""
        while len(queue) > 0:
            traversal += str(queue[-1].value) + "-"
            node = queue.pop()
            if node.left:
                queue.insert(0, node.left)
            if node.right:
                queue.insert(0, node.right)
        return traversal

    def reverse_level_order(self, start):
        if start is None:
            return
        stack, queue = [], []
        queue.append(start)
        traversal = ""
        while len(queue) > 0:
            node = queue.pop()
            stack.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return "-".join([str(x) for x in stack[::-1]])

    def height(self, start):
        if not start:
            return -1
        left = self.height(start.left)
        right = self.height(start.right)
        return 1 + max(left, right)

    def search(self, value):
        """downside with simplicity is the BST structure changed"""
        check = self.root.value
        if check == value:
            print(check)
            return True
        if value < check:
            self.root = self.root.left
            return self.search(value)
        if value > check:
            self.root = self.root.right
            return self.search(value)
        return False

    def insert_frm_list(self, lst):
        if not self.root.value:
            self.root = Node(lst[0])
            lst = lst[1:]

        stack = []
        stack.append(self.root)
        while lst:
            val = lst.pop(0)
            node = stack.pop()
            if node.value > val:
                node.right = Node(val)
            if node.value < val:
                node.left = Node(val)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return "Done"

    def insert(self, new_val):
        self.insert_helper(self.root, new_val)

    def insert_helper(self, current, new_val):
        if current.value < new_val:
            if current.right:
                self.insert_helper(current.right, new_val)
            else:
                current.right = Node(new_val)
        else:
            if current.left:
                self.insert_helper(current.left, new_val)
            else:
                current.left = Node(new_val)

    def is_bst_satisfied(self):
        def helper(node, lower=float("-inf"), upper=float("inf")):
            if not node:
                return True

            val = node.value
            if val <= lower or val >= upper:
                return False

            if not helper(node.right, val, upper):
                return False
            if not helper(node.left, lower, val):
                return False
            return True

        return helper(self.root)

    def is_bst(self):
        if not self.root:
            return
        stack = []
        stack.append(self.root)
        while stack:
            val = stack.pop()
            if val.right:
                if val.right.value > val.value:
                    stack.append(val.right)
                else:
                    return False
            if val.left:
                if val.left.value < val.value:
                    stack.append(val.left)
                else:
                    return False
        return True


if __name__ == "__main__":
    bst = BST(7)
    bst.insert(3)
    bst.insert(10)
    bst.insert(5)
    bst.insert(1)
    bst.insert(8)
    bst.insert(9)
    bst.insert(2)

    tree = BST(1)
    tree.root.left = Node(2)
    tree.root.right = Node(3)
    tree.root.left.left = Node(4)
    tree.root.left.right = Node(5)
    tree.root.right.left = Node(6)
    tree.root.right.right = Node(7)
    tree.root.right.right.right = Node(8)
    # stuff = [8,3,10,1,6]
    # print(tree.insert_frm_list(stuff))
    print(bst.is_bst_satisfied())
    print(bst.is_bst())
    print(tree.is_bst_satisfied())
    print(tree.is_bst())
