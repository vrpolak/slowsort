"""Module that defines abstract mutable priority counting queue."""

# TODO: Make this Abstract Base Class so that users can rely on isinstance.


from mutable_priority_queue import MutablePriorityQueue


class MutableCountingPriorityQueue(MutablePriorityQueue):
    """Priority queue, least priority value in, first out. Tracks size.

    Self is altered regularily to avoid excessive object creation."""

    def __len__(self):
        """Return number of items stored."""

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        raise NotImplementedError

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        raise NotImplementedError
