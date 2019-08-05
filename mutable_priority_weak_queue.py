"""Module that defines abstract mutable priority weak queue."""


from mutable_priority_queue import MutablePriorityQueue


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class MutablePriorityWeakQueue(MutablePriorityQueue):
    """Priority queue, least priority value in, first out (or vanish).

    The main difference from ordinary "non-weak" queues
    is that those can act as storages.
    Weak queue is not a storage, it is only a cache.
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
    pass
