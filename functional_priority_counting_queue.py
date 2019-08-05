"""Module that defines abstract functional priority counting queue."""


from functional_priority_queue import FunctionalPriorityQueue


# TODO: Make this Abstract Base Class so that users can rely on isinstance.

class FunctionalPriorityCountingQueue(FunctionalPriorityQueue):
    """Priority queue, least priority value in, first out.

    Self is never altered. Modified object is created and returned when needed."""

    def __len__(self):
        """Return number of items stored."""

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        raise NotImplementedError

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        raise NotImplementedError
