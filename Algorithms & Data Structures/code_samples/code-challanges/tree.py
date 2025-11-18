# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


node_storage = []


class Solution:
    def gimme_da_nodes_pls(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root:
            return
        if root:
            node_storage.append(root)
        if root.left:
            self.gimme_da_nodes_pls(root.left)
        if root.right:
            self.gimme_da_nodes_pls(root.right)

    def flatten(self, root: TreeNode) -> None:

        self.gimme_da_nodes_pls(root)
        for i in range(len(node_storage)):

            if i == len(node_storage) - 1:
                node_storage[i].right = None
                break

            node_storage[i].left = None
            node_storage[i].right = node_storage[i + 1]

        return node_storage
