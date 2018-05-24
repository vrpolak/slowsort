"""Module that defines abstract mutable priority weak queue."""


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class MutablePriorityWeakQueue(object):
    """Priority queue, least priority value in, first out (or vanish).

    The main difference from ordinary "non-weak" queues
    is that those can act as storages.
    Weak queue is not storage, it is only a cache.
    If the object is not referenced from elsewhere,
    it will be deleted from the queue.
    Weak queues seem to be easier to implement
    than queues with explicit remove operation
    (as that needs equality and search inside the queue,
    whereas weak queues can remove the item only when encountered).

    As the removal can be postponed, len and is_empty are not supported anymore
    (contrary to non-weak queue, they would no longer be cheap operations).
    Instead, peek() always works, but returns None if the queue is found empty.

    Self is altered regularily to avoid excessive object creation."""

    def __init__(self):
        """Initialize an empty queue."""
        raise NotImplementedError

    def add(self, item):
        """Add item to self, return None."""
        raise NotImplementedError

    def peek(self):
        """Locate the least item, and return that or None."""
        raise NotImplementedError

    def pop(self):
        """Extract the least item from self and return that or None."""
        raise NotImplementedError
