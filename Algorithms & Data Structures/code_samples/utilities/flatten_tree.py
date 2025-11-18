# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def flatten(self, root):
        """
        :type root: TreeNode
        :rtype: None Do not return anything, modify root in-place instead.
        """
        node_storage = []
        firstNode = root

        while root or node_storage:
            if root.left:
                if root.right:
                    node_storage.append(root.right)
                root.right = root.left
                root.left = None
                continue
            elif root.right:
                root = root.right
                continue
            elif node_storage:
                root.right = node_storage.pop()
                root = root.right
            else:
                root = None

        return firstNode
