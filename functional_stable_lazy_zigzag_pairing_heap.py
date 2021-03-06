"""Module that defines functional stable zigzag pairing heap."""

from pep_3140 import Deque
from pep_3140 import List
from sorted_using_heap import sorted_using_functional_stable_heap
from functional_priority_queue import FunctionalPriorityQueue


class FunctionalStableLazyZigzagPairingHeap(FunctionalPriorityQueue):
    """A heap that is functional, stable, lazy, and zigzag pairing.

    Heap: An implementation, usable as a queue, least priority value in, first out.
    Functional: After creation, state is never changed. Constructing modified object to return if needed.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Stable: Two include methods to allow caller decide tiebreaker.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.

    This implementation uses Deque to store ordered collection of sub-heaps.
    Note that Deque is mutable."""

    def __init__(self, top_item=None, forest=None):
        """Initialize a queue.."""
        self.top_item = top_item
        self.forest = forest if forest is not None else Deque()

    def copy(self):
        """Return shalow copy for the caller to mutate."""
        return FunctionalStableLazyZigzagPairingHeap(self.top_item, Deque(self.forest))

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return self.copy()
        return FunctionalStableLazyZigzagPairingHeap(None, Deque([self]))

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        ensured = self.ensure_top_demoted()
        ensured.forest.append(FunctionalStableLazyZigzagPairingHeap(top_item=item))
        return ensured

    def _include_after(self, heap):
        """Include another heap, prioritized after current items."""
        copied = self.copy()
        copied.forest.append(heap)
        return copied

    def _include_before(self, heap):
        """Include another heap, prioritized before current items."""
        copied = self.copy()
        copied.forest.appendleft(heap)
        return copied

    def peek(self):
        """Return heap with top promoted and top item. Top is None if empty."""
        promoted = self.ensure_top_promoted()
        return promoted, promoted.top_item

    def pop(self):
        """If not empty, return tuple of the smaller queue and the least item."""
        ensured = self.ensure_top_promoted()
        item = ensured.top_item
        ensured.top_item = None
        return ensured, item

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade and return."""
        if (self.top_item is not None) or (not self.forest):
            return self.copy()
        # Copy trees so we can mutate them.
        popping_forest = Deque([tree.copy() for tree in self.forest])
        while len(popping_forest) > 1:
            # zig
            new_forest = Deque()
            while len(popping_forest) > 1:
                # Sub-heaps should always be promoted and non-empty.
                latter = popping_forest.pop()
                former = popping_forest.pop()
                if latter.top_item < former.top_item:
                    new_forest.appendleft(latter._include_before(former))
                else:
                    new_forest.appendleft(former._include_after(latter))
            if popping_forest:
                new_forest.appendleft(popping_forest.pop())
            popping_forest = new_forest
            # zag
            new_forest = Deque()
            while len(popping_forest) > 1:
                former = popping_forest.pop()
                latter = popping_forest.pop()
                if latter.top_item < former.top_item:
                    new_forest.append(latter._include_before(former))
                else:
                    new_forest.append(former._include_after(latter))
            if popping_forest:
                new_forest.append(popping_forest.pop())
            popping_forest = new_forest
        return popping_forest.pop()


def fslzph_sorted(source):
    """Return new list of items, sorted using the mslzp heap."""
    return sorted_using_functional_stable_heap(FunctionalStableLazyZigzagPairingHeap, source)
