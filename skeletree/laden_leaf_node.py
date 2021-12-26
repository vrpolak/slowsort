"""Module that defines a leaf tree node with a payload."""


from skeletree.skeleton_resolved_node import SkeletonResolvedNode

# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class LadenLeafNode(object):
    """Leaf node of a generic (non-binary) tree carrying a payload.

    In sorting, payload is one item of the collection to sort.

    TODO: Subclass of SizedTreeNode?
    """

    def __init__(self, payload):
        """Initialize from a payload."""
        self._payload = payload

    # TODO: str and repr.

    @property
    def size(self):
        """Return size, 1 as this is a leaf."""
        return 1

    def skeletize(self):
        """Return skeleton leaf node."""
        return SkeletonResolvedNode([])

    # Not iterable, call your isisntance() first,
