"""Module that defines a generic tree node with a size."""


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class SizedTreeNode(object):
    """Node of a generic (non-binary) tree tracking its size.

    Payloads and mutability depend on subclasses.
    The common code is a constructor and iteration.
    This class is iterable, yielding subtrees.
    Size is computed lazily.
    """

    def __init__(self, forest):
        """Initialize from an iterable of subtrees. No subtree means leaf node."""
        self._forest = List(forest)
        self._size = None

    # TODO: str and repr.

    @property
    def size(self):
        """Return size, compute if not stored yet."""
        if self._size is not None:
            self._size = sum(subtree.size for subtree in self._forest) if self._forest else 1
        return self._size

    def __iter__(self):
        """Yield subtrees."""
        for subtree in self._forest:
            yield subtree
