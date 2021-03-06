"""Module that defines abstract mutable priority queue."""

# TODO: Make this Abstract Base Class so that users can rely on isinstance.


class MutablePriorityQueue(object):
    """Priority queue, least priority value in, first out.

    Self is altered regularily to avoid excessive object creation."""

    def __init__(self):
        """Initialize an empty queue."""
        raise NotImplementedError

    def add(self, item):
        """Add item to self, return None."""
        raise NotImplementedError

    def peek(self):
        """If not empty, locate the least item and return that."""
        raise NotImplementedError

    def pop(self):
        """If not empty, extract the least item from self and return that.
        If empty, return None."""
        raise NotImplementedError
