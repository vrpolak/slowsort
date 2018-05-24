"""Module that provides the default implementation of MutableBinaryTreeLadenNode.

TODO: Delete as no search here uses this."""

from mutable_binary_tree_laden_node import MutableBinaryTreeLadenNode


class DefaultImplMutableBinaryTreeLadenNode(MutableBinaryTreeLadenNode):
    """Node of binary tree, carrying a payload object.

    Left and right children are either None or also Node.
    Self is altered regularily to avoid excessive object creation."""

    def __init__(self, payload):
        """Initialize an childless node."""
        self.payload = payload
        self.left_child = None
        self.right_child = None

    def get_payload(self):
        """Return the payload, do not change state."""
        return self.payload

    def get_left_child(self):
        """Return left child or None, do not change state."""
        return self.left_child

    def get_right_child(self):
        """Return right child or None, do not change state."""
        return self.right_child

    def swap_payload(self, payload):
        """Set the new payload, return the old payload."""
        odl_payload = self.payload
        self.payload = payload
        return odl_payload

    def swap_left_child(self, node):
        """Set node (may be None) as new left child, return the previous left child."""
        old_left_child = self.left_child
        self.left_child = node
        return odl_left_child

    def swap_right_child(self, node):
        """Set node (may be None) as new right child, return the previous right child."""
        old_right_child = self.right_child
        self.right_child = node
        return odl_right_child
