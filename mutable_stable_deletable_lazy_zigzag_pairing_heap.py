"""Module that defines mutable stable deletable zigzag pairing heap."""

from pep_3140 import Deque
from pep_3140 import List
from sorted_using_heap import sorted_using_mutable_stable_heap
from mutable_deletable_priority_queue import MutableDeletablePriorityQueue


class MutableStableDeletableLazyZigzagPairingHeap(MutableDeletablePriorityQueue):
    """A heap that is mutable, stable, lazy, and zigzag pairing.

    Heap: An implementation, usable as a queue, least priority value in, first out.
    Deletable: Items can be deleted without popping, items have to be hashable.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Stable: Two include methods to allow caller decide tiebreaker.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.

    This implementation uses Deque to store ordered collection of sub-heaps.
    Limitation: Items have to be hashable, as deletion is lazy, using set.
    """

    def __init__(self, top_item=None, forest=None, deleted=None):
        """Initialize a queue."""
        self.top_item = top_item
        self.forest = Deque() if forest is None else forest
        self.deleted = set() if deleted is None else deleted

    def delete(self, item):
        """Lazily remove the item from consideration. TODO: Check whether is even in?"""
        self.delete.add(item)

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return
        demoted = MutableStableDeletableLazyZigzagPairingHeap(self.top_item, self.forest, self.deleted)
        self.top_item = None
        self.forest = Deque([demoted])

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        if item in self.deleted:
            self.deleted.remove(item)
            return
        self.ensure_top_demoted()
        self.forest.append(MutableStableDeletableLazyZigzagPairingHeap(item, None, self.deleted))

    def _include_after(self, heap):
        """Include another heap, prioritized after current items."""
        self.forest.append(heap)

    def _include_before(self, heap):
        """Include another heap, prioritized before current items."""
        self.forest.appendleft(heap)

    def peek(self):
        """Return least priority item, this includes promoting top, but not extraction."""
        self.ensure_top_promoted()
        return self.top_item

    def pop(self):
        """If not empty, extract the least item from self and return that."""
        self.ensure_top_promoted()
        item = self.top_item
        self.top_item = None
        return item

    # TODO: Merge this into peek(), weak heaps suggest that makes things faster. Or is it not bothering with len?
    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if (self.top_item is not None):
            if self.top_item not in self.deleted:
                return
            self.top_item = None
            self.deleted.remove(self.item)
        if not self.forest:
            return
        # Make sure subheaps do not have deleted tops before zigzagging.
        new_forest = Deque()
        while len(self.forest):
            tree = self.forest.pop()
            tree.ensure_top_promoted()
            if tree.top_item is not None:
                new_forest.appendleft(tree)
        self.forest = new_forest
        while len(self.forest) > 1:
            # zig
            new_forest = Deque()
            while len(self.forest) > 1:
                latter = self.forest.pop()
                former = self.forest.pop()
                # Sub-heaps should be nonempty and have top promoted (and not deleted).
                if latter.top_item < former.top_item:
                    latter._include_before(former)
                    new_forest.appendleft(latter)
                else:
                    former._include_after(latter)
                    new_forest.appendleft(former)
            if self.forest:
                new_forest.appendleft(self.forest.pop())
            self.forest = new_forest
            # zag
            new_forest = Deque()
            while len(self.forest) > 1:
                former = self.forest.popleft()
                latter = self.forest.popleft()
                if latter.top_item < former.top_item:
                    latter._include_before(former)
                    new_forest.append(latter)
                else:
                    former._include_after(latter)
                    new_forest.append(former)
            if self.forest:
                new_forest.append(self.forest.pop())
            self.forest = new_forest
        new_state = self.forest.pop()
        self.top_item = new_state.top_item
        self.forest = new_state.forest


def msdlzph_sorted(source):
    """Return new List of items, sorted using the msdlzp heap."""
    return sorted_using_mutable_stable_heap(MutableStableDeletableLazyZigzagPairingHeap, source)
