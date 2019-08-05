"""Module that defines abstract functional priority queue."""


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class FunctionalPriorityQueue(object):
    """Priority queue, least priority value in, first out.

    Self is never altered. Modified object is created and returned when needed."""

    def __init__(self):
        """Initialize an empty queue."""
        raise NotImplementedError

    def add(self, item):
        """Return modified queue with added item."""
        raise NotImplementedError

    def pop(self):
        """If not empty, return tuple of the smaller queue and the least item."""
        raise NotImplementedError

    def peek(self):
        """If not empty, return tuple of optimized queue and the least item.
        If empty, return tuple of optimized queue and None."""
        raise NotImplementedError
