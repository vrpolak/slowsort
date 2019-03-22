"""Module that defines mutable stable zigzag pairing heap."""

from pep_3140 import Deque
from pep_3140 import List
from sorted_using_heap import sorted_using_mutable_stable_heap
from mutable_priority_queue import MutablePriorityQueue


class MutableStableLazyZigzagPairingHeap(MutablePriorityQueue):
    """A heap that is mutable, stable, lazy, and zigzag pairing.

    Heap: An implementation, usable as a queue, least priority value in, first out.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Stable: Two include methods to allow caller decide tiebreaker.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.

    This implementation uses Deque to store ordered collection of sub-heaps."""

    def __init__(self, top_item=None, forest=None, known_length=None):
        """Initialize a queue."""
        self.top_item = top_item
        self.forest = forest if forest is not None else Deque()
        if known_length is not None:
            self.length = known_length
        else:
            self.length = sum(map(len, self.forest))
            self.length += (self.top_item is not None)

    def __len__(self):
        """Return number of stored elements."""
        return self.length

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        return self.length < 1

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        return self.length > 0

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return
        demoted = MutableStableLazyZigzagPairingHeap(self.top_item, self.forest, self.length)
        self.top_item = None
        self.forest = Deque([demoted])

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        self.ensure_top_demoted()
        self.forest.append(MutableStableLazyZigzagPairingHeap(top_item=item))
        self.length += 1

    def _include_after(self, heap):
        """Include another heap, prioritized after current items."""
        self.length += len(heap)
        self.forest.append(heap)

    def _include_before(self, heap):
        """Include another heap, prioritized before current items."""
        self.length += len(heap)
        self.forest.appendleft(heap)

    def peek(self):
        """Return least priority item, this includes promoting top, but not extraction."""
        if self.is_empty():
            raise IndexError("MutableStableLazyZigzagPairingHeap: peek when empty.")
        self.ensure_top_promoted()
        return self.top_item

    def pop(self):
        """If not empty, extract the least item from self and return that."""
        if self.is_empty():
            raise IndexError("MutableStableLazyZigzagPairingHeap: pop when empty.")
        self.ensure_top_promoted()
        item = self.top_item
        self.top_item = None
        self.length -= 1
        return item

    # TODO: Merge this into peek(), weak heaps suggest that makes things faster. Or is it not bothering with len?
    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if (self.top_item is not None) or (not self.forest):
            return
        while len(self.forest) > 1:
            # zig
            new_forest = Deque()
            while len(self.forest) > 1:
                latter = self.forest.pop()
                former = self.forest.pop()
                if latter.peek() < former.peek():
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
                if latter.peek() < former.peek():
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


def mslzph_sorted(source):
    """Return new List of items, sorted using the mslzp heap."""
    return sorted_using_mutable_stable_heap(MutableStableLazyZigzagPairingHeap, source)
