"""Module that defines abstract functional priority queue with invalidate operation."""


from functional_priority_queue import FunctionalPriorityQueue


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class FunctionalInvalidatingPriorityQueue(FunctionalPriorityQueue):
    """Priority queue, with invalidate operation.
    Self is never altered. Modified object is created and returned when needed."""

    def invalidate(self, item_is_invalid):
        """Return new queue without items on which the argument function returns true."""
        raise NotImplementedError
