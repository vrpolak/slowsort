"""Module that defines mutable inclusion preferring zigzag pairing heap."""

from pep_3140 import Deque
from pep_3140 import List
from sorted_using_heap import sorted_using_mutable_unstable_heap
from mutable_priority_queue import MutablePriorityQueue

class MutableInclusionPreferringLazyZigzagPairingHeap(MutablePriorityQueue):
    """Heap: An implementation, usable as a queue, least priority value in, first out.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Inclusion preferring: Only one inclusin method, included heap is preferred to existinmg ones.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.
    This heap does NOT result in stable sort algorithm.

    This implementation uses Deque to store ordered collection of sub-heaps."""

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
        """Return number of items stored."""
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
        demoted = MutableInclusionPreferringLazyZigzagPairingHeap(self.top_item, self.forrest, self.length)
        self.top_item = None
        self.forrest = Deque([demoted])

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        self.ensure_top_demoted()
        heap = MutableInclusionPreferringLazyZigzagPairingHeap(top_item=item)
        # Addition is not inclusion, so late items are not preferred.
        self.forrest.append(heap)
        self.length += 1

    def include_before(self, heap):
        """Include another heap, prioritized before current items."""
        self.ensure_top_promoted()
        self.length += len(heap)
        self.forrest.appendleft(heap)

    def peek(self):
        """Return least priority item, this includes promoting top, but not extraction."""
        if self.is_empty():
            raise IndexError("MutableInclusionPreferringLazyZigzagPairingHeap: peek when empty.")
        self.ensure_top_promoted()
        return self.top_item

    def pop(self):
        """If not empty, extract the least item from self and return that."""
        if self.is_empty():
            raise IndexError("MutableInclusionPreferringLazyZigzagPairingHeap: pop when empty.")
        self.ensure_top_promoted()
        item = self.top_item
        self.top_item = None
        self.length -= 1
        return item

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if (self.top_item is not None) or (not self.forrest):
            return
        while len(self.forrest) > 1:
            # zig
            new_forrest = Deque()
            while len(self.forrest) > 1:
                latter = self.forrest.pop()
                former = self.forrest.pop()
                if latter.peek() < former.peek():
                    latter.include_before(former)
                    new_forrest.appendleft(latter)
                else:
                    former.include_before(latter)
                    new_forrest.appendleft(former)
            if self.forrest:
                new_forrest.appendleft(self.forrest.pop())
            self.forrest = new_forrest
            # zag
            new_forrest = Deque()
            while len(self.forrest) > 1:
                former = self.forrest.popleft()
                latter = self.forrest.popleft()
                if latter.peek() < former.peek():
                    latter.include_before(former)
                    new_forrest.append(latter)
                else:
                    former.include_before(latter)
                    new_forrest.append(former)
            if self.forrest:
                new_forrest.append(self.forrest.pop())
            self.forrest = new_forrest
        new_state = self.forrest.pop()
        self.top_item = new_state.top_item
        self.forrest = new_state.forrest


def miplzph_sorted(source):
    """Return new list of items, sorted using the mslzp heap."""
    return sorted_using_mutable_unstable_heap(MutableInclusionPreferringLazyZigzagPairingHeap, source)
