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

    def __init__(self, top_item=None, forrest=None, known_length=None):
        """Initialize a queue.."""
        self.top_item = top_item
        self.forrest = forrest if forrest is not None else Deque()
        if known_length is not None:
            self.length = known_length
        else:
            self.length = sum(map(len, self.forrest))
            self.length += (self.top_item is not None)

    def __len__(self):
        """Return number of stored elements."""
        return self.length

    def copy(self):
        """Return shalow copy for the caller to mutate."""
        return FunctionalStableLazyZigzagPairingHeap(self.top_item, Deque(self.forrest), len(self))

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        return self.length < 1

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        return self.length > 0

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return self.copy()
        return FunctionalStableLazyZigzagPairingHeap(None, Deque([self]), self.length)

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        ensured = self.ensure_top_demoted()
        ensured.forrest.append(FunctionalStableLazyZigzagPairingHeap(top_item=item))
        ensured.length += 1
        return ensured

    def _include_after(self, heap):
        """Include another heap, prioritized after current items."""
        copied = self.copy()
        copied.forrest.append(heap)
        copied.length += len(heap)
        return copied

    def _include_before(self, heap):
        """Include another heap, prioritized before current items."""
        copied = self.copy()
        copied.forrest.appendleft(heap)
        copied.length += len(heap)
        return copied

    def peek(self):
        """Return heap with top promoted and top item."""
        if self.is_empty():
            raise IndexError("FunctionalStableLazyZigzagPairingHeap: pop when empty.")
        promoted = self.ensure_top_promoted()
        return promoted, promoted.top_item

    def pop(self):
        """If not empty, return tuple of the smaller queue and the least item."""
        if self.is_empty():
            raise IndexError("FunctionalStableLazyZigzagPairingHeap: pop when empty.")
        ensured = self.ensure_top_promoted()
        item = ensured.top_item
        ensured.top_item = None
        ensured.length -= 1
        return ensured, item

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade and return."""
        if (self.top_item is not None) or (not self.forrest):
            return self.copy()
        popping_forrest = Deque(self.forrest)
        while len(popping_forrest) > 1:
            # zig
            new_forrest = Deque()
            while len(popping_forrest) > 1:
                # Sub-heaps should always be promoted, but better save state then be then sorry.
                latter, latter_top = popping_forrest.pop().peek()
                former, former_top = popping_forrest.pop().peek()
                if latter_top < former_top:
                    new_forrest.appendleft(latter._include_before(former))
                else:
                    new_forrest.appendleft(former._include_after(latter))
            if popping_forrest:
                new_forrest.appendleft(popping_forrest.pop())
            popping_forrest = new_forrest
            # zag
            new_forrest = Deque()
            while len(popping_forrest) > 1:
                former, former_top = popping_forrest.popleft().peek()
                latter, latter_top = popping_forrest.popleft().peek()
                if latter_top < former_top:
                    new_forrest.append(latter._include_before(former))
                else:
                    new_forrest.append(former._include_after(latter))
            if popping_forrest:
                new_forrest.append(popping_forrest.pop())
            popping_forrest = new_forrest
        return popping_forrest.pop()


def fslzph_sorted(source):
    """Return new list of items, sorted using the mslzp heap."""
    return sorted_using_functional_stable_heap(FunctionalStableLazyZigzagPairingHeap, source)
