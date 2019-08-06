"""Module that defines abstract mutable priority queue with deletion."""

# TODO: Make this Abstract Base Class so that users can rely on isinstance.


from mutable_priority_queue import MutablePriorityQueue


class MutableDeletablePriorityQueue(MutablePriorityQueue):
    """Priority queue, least priority value in, first out. Deletes items.

    Items have to be hashable.

    Self is altered regularily to avoid excessive object creation."""

    def delete(self, item):
        """Remove the item from heap."""
        raise NotImplementedError