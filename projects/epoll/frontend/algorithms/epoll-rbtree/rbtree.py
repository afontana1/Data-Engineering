"""
Red–Black Tree (RBTree) implementation
=====================================

What this is for
----------------
This module implements a **Red–Black Tree**, a self-balancing binary search tree that
keeps operations efficient even in worst case by enforcing balancing rules.

Typical use cases:
- Ordered maps/dictionaries (key -> value) where you need:
  - fast insert/search/delete: O(log n)
  - sorted traversal (in-order) for range queries / iteration in key order

Implementation notes
--------------------
- Uses a single shared **NIL sentinel node** (self.NIL) instead of `None` for leaves.
  This simplifies logic because every child pointer is always a node.
- Each node is colored `"red"` or `"black"` and rotations + recoloring maintain
  the red–black invariants after insert/delete.
- This code provides:
  - insert(key, value): inserts or updates
  - search(key): lookup
  - delete(key): delete by key
  - inorder(): returns sorted (key, value) pairs (debug/verification)

Red–Black Tree invariants (high-level)
--------------------------------------
1) Every node is either red or black.
2) The root is black.
3) All leaves (the NIL sentinel) are black.
4) Red nodes cannot have red children (no two reds in a row).
5) Every path from a node to descendant NIL leaves has the same number of black nodes
   ("black height" is consistent).

The fixup routines (_insert_fixup and _delete_fixup) are the standard CLRS-style
procedures that restore these invariants using recoloring and tree rotations.
"""


class RBNode:
    """
    A node in a Red–Black Tree.

    Attributes
    ----------
    key : comparable
        Key used for ordering in the BST (must support < and > comparisons).
    value : any
        Payload stored with the key.
    color : str
        Either "red" or "black".
    left, right : RBNode
        Child pointers. In this implementation, child pointers point to RBTree.NIL
        rather than None for missing children.
    parent : RBNode | None
        Parent pointer. The root's parent is None.

    Notes
    -----
    __slots__ is used to reduce per-node memory overhead (common in tree structures).
    """
    __slots__ = ("key", "value", "color", "left", "right", "parent")

    def __init__(self, key=None, value=None,
                 color="black", left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.color = color  # "red" or "black"
        self.left = left
        self.right = right
        self.parent = parent


class RBTree:
    """
    Red–Black Tree storing (key, value) pairs.

    Public API
    ----------
    insert(key, value) -> RBNode
        Insert a key/value pair. If key exists, update its value and return the node.
    search(key) -> RBNode | None
        Return the node for key, or None if not found.
    delete(key) -> bool
        Delete by key. Returns True if deleted, False if not found.
    inorder(node=None, res=None) -> list[tuple[key, value]]
        In-order traversal (sorted by key). Primarily for debugging/testing.

    Internal helpers
    ----------------
    left_rotate / right_rotate
        Local structural changes that preserve BST order.
    _insert_fixup
        Restores RB invariants after insertion.
    _delete_fixup
        Restores RB invariants after deletion when a black node is removed/moved.
    transplant
        Replaces one subtree with another (used by delete).
    minimum
        Finds minimum key in subtree (used by delete).
    """

    def __init__(self):
        """
        Initialize an empty RBTree.

        Creates a single shared NIL sentinel node:
        - Always colored black
        - Left/right pointers refer to itself
        - Used as the child for all "missing" leaves

        Root begins as NIL (empty tree).
        """
        # Single shared NIL (sentinel) node
        self.NIL = RBNode()
        self.NIL.color = "black"
        self.NIL.left = self.NIL.right = self.NIL
        self.root = self.NIL

    # ---- rotations ----

    def left_rotate(self, x):
        """
        Left-rotate around node x.

        Before:
              x
               \
                y
               /
              T2

        After:
              y
             /
            x
             \
              T2

        This preserves BST ordering while changing the local shape.
        Used during fixup steps to restore RB invariants.
        """
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """
        Right-rotate around node y (mirror of left_rotate).

        Before:
                y
               /
              x
               \
                T2

        After:
              x
               \
                y
               /
              T2
        """
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    # ---- insert ----

    def insert(self, key, value):
        """
        Insert (key, value) into the tree.

        Behavior
        --------
        - If key does not exist: insert a new red node in the BST position,
          then restore RB invariants via _insert_fixup.
        - If key already exists: update the node's value and return it
          (tree structure is unchanged).

        Returns
        -------
        RBNode
            The inserted or updated node.

        Complexity
        ----------
        O(log n) expected/worst-case due to balancing.
        """
        node = RBNode(key, value, color="red",
                      left=self.NIL, right=self.NIL)
        y = None
        x = self.root

        # Standard BST insert search for position
        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                # Key exists: update and return.
                x.value = value
                return x

        # Attach to parent y
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        # Restore red-black properties after insertion
        self._insert_fixup(node)
        return node

    def _insert_fixup(self, z):
        """
        Restore RB invariants after inserting node z.

        New nodes are inserted as red. Violations can occur if z's parent is red,
        which would break the "no two consecutive reds" rule.

        The loop resolves violations using:
        - recoloring (when uncle is red)
        - rotations + recoloring (when uncle is black)

        This is the classic CLRS algorithm with mirrored cases.
        """
        while z.parent is not None and z.parent.color == "red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # uncle
                if y.color == "red":
                    # Case 1: parent and uncle are red -> recolor and move up
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    # Uncle is black
                    if z == z.parent.right:
                        # Case 2: triangle -> rotate to form line
                        z = z.parent
                        self.left_rotate(z)
                    # Case 3: line -> recolor and rotate
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    self.right_rotate(z.parent.parent)
            else:
                # Mirror image of above cases
                y = z.parent.parent.left  # uncle
                if y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "black"
                    z.parent.parent.color = "red"
                    self.left_rotate(z.parent.parent)

        # Ensure root is always black
        self.root.color = "black"

    # ---- transplant & min ----

    def transplant(self, u, v):
        """
        Replace subtree rooted at u with subtree rooted at v.

        Used by delete() to "splice out" nodes and reconnect the tree.
        Parent pointers are updated accordingly.
        """
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, x=None):
        """
        Return the node with the minimum key in subtree rooted at x.

        If x is None, starts from the tree root.
        Returns None if the tree (or subtree) is empty.
        """
        if x is None:
            x = self.root
        if x == self.NIL:
            return None
        while x.left != self.NIL:
            x = x.left
        return x

    # ---- search ----

    def search(self, key):
        """
        Search for key and return its node, or None if not found.

        Complexity: O(log n) in a balanced RB tree.
        """
        x = self.root
        while x != self.NIL:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x
        return None

    # ---- delete ----

    def delete(self, key):
        """
        Delete the node with the given key.

        Returns
        -------
        bool
            True if a node was found and deleted, False otherwise.

        Notes
        -----
        Deletion is more subtle than insertion in RB trees. If the removed node
        (or the node moved into its place) was black, the black-height invariants
        may be violated. _delete_fixup repairs these using rotations/recoloring.

        This follows the CLRS approach:
        - If node has 0 or 1 non-NIL children: splice it out.
        - If node has 2 children: swap with successor (minimum of right subtree),
          then delete successor in its original location.
        """
        z = self.search(key)
        if z is None:
            return False

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            # Replace z by its right child
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            # Replace z by its left child
            x = z.left
            self.transplant(z, z.left)
        else:
            # Two children: use successor y (min of right subtree)
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                # Successor is direct child of z
                x.parent = y
            else:
                # Move successor up, and attach z.right under it
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            # Put successor where z was
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        # If we removed/moved a black node, fix potential violations
        if y_original_color == "black":
            self._delete_fixup(x)

        return True

    def _delete_fixup(self, x):
        """
        Restore RB invariants after deletion, starting from node x.

        x is the node that moved into the deleted node's position (possibly NIL).
        If a black node was removed, x may have an extra "black deficit" that must
        be repaired (often described as "double black" in some explanations).

        The procedure uses sibling cases:
        - sibling red -> rotate to convert into black-sibling case
        - sibling black with black children -> recolor and move up
        - sibling black with a red "near" child -> rotate sibling
        - sibling black with a red "far" child -> rotate parent and recolor
        """
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                w = x.parent.right  # sibling
                if w.color == "red":
                    # Case: sibling red -> rotate parent, recolor
                    w.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "black" and w.right.color == "black":
                    # Case: sibling black, both children black -> recolor sibling, move up
                    w.color = "red"
                    x = x.parent
                else:
                    if w.right.color == "black":
                        # Case: far child black, near child red -> rotate sibling
                        w.left.color = "black"
                        w.color = "red"
                        self.right_rotate(w)
                        w = x.parent.right
                    # Case: far child red -> rotate parent, recolor to finish
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # Mirror of above with left/right swapped
                w = x.parent.left
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "black" and w.left.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "black"

    # ---- traversal (for debugging) ----

    def inorder(self, node=None, res=None):
        """
        In-order traversal of the tree.

        Parameters
        ----------
        node : RBNode | None
            Starting node. Defaults to root.
        res : list | None
            Accumulator list. If None, a new list is created.

        Returns
        -------
        list[tuple[key, value]]
            Sorted list of (key, value) pairs.

        Notes
        -----
        Intended for debugging/testing (verifying BST order and contents).
        Not optimized for huge trees due to recursion depth limits in Python.
        """
        if res is None:
            res = []
        if node is None:
            node = self.root
        if node != self.NIL:
            self.inorder(node.left, res)
            res.append((node.key, node.value))
            self.inorder(node.right, res)
        return res