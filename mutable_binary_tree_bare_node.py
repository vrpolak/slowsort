"""Module that defines abstract mutable binary tree node without a payload.

TODO: Delete as no search here uses this."""


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class MutableBinaryTreeBareNode(object):
    """Node of binary tree, not carrying any payload.

    Left and right children are either None or also Node.
    Self is altered regularily to avoid excessive object creation."""

    def __init__(self):
        """Initialize an childless node."""
        raise NotImplementedError

    def get_left_child(self):
        """Return left child or None."""
        raise NotImplementedError

    def get_right_child(self):
        """Return right child or None."""
        raise NotImplementedError

    def swap_left_child(self, node):
        """Set node (may be None) as new left child, return the previous left child."""
        raise NotImplementedError

    def swap_right_child(self, node):
        """Set node (may be None) as new right child, return the previous right child."""
        raise NotImplementedError
