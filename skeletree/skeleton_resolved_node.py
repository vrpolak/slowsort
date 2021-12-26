"""Module that defines a skeleton tree node that is resolved."""


from skeletree.sized_tree_node import SizedTreeNode

# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class SkeletonResolvedNode(SizedTreeNode):
    """Node of a generic (non-binary) tree without payloads, resolved.

    Compared to SizedTreeNode, equality and hashing is supported.
    Hashing is done via frozenset, hence the need for the node to be resolved.
    Empty forest means leafskeleton node.
    """

    def __init__(self, forest):
        """Initialize from an iterable of subtrees. No subtree means leaf node."""
        super().__init__(forest)
        sizes = Frozenset(subtree.size for subtree in self)
        if len(sizes) != len(self._forest):
            raise RuntimeError(f"Not resolved: {self._forest}")
        self._forest = Frozenset(self._forest)
        self._hash = hash(self._forest)

    # TODO: str and repr.

    def __hash__(self):
        """Return the cached hash."""
        return self._hash
