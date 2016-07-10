"""Module that defines mutable stable zigzag pairing heap."""

from collections import deque
from mutable_priority_queue import MutablePriorityQueue

class MutableStableLazyZigzagPairingHeap(MutablePriorityQueue):
    """Heap: An implementation, usable as a queue, least priority value in, first out.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Stable: Two include methods to allow caller decide tiebreaker.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.

    This implementation uses deque to store ordered collection of sub-heaps."""

    def __init__(self, top_item=None, forrest=None):
        """Initialize a queue.."""
        self.top_item = top_item
        self.forrest = forrest or deque()

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        return (not self.forrest) and (not self.top_item)

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        return not self.is_empty()

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if not self.top_item:
            return
        demoted = MutableStableLazyZigzagPairingHeap(self.top_item, self.forrest)
        self.top_item = None
        self.forrest = deque([demoted])

    def add(self, payload, priority):
        """Add item to self, prioritized after current items, do not compare yet."""
        self.ensure_top_demoted()
        item = (priority, payload)
        heap = MutableStableLazyZigzagPairingHeap(top_item=item)
        self.forrest.append(heap)

    def include_after(self, heap):
        """Include another heap, prioritized after current items."""
        self.ensure_top_promoted()
        self.forrest.append(heap)

    def include_before(self, heap):
        """Include another heap, prioritized before current items."""
        self.ensure_top_promoted()
        self.forrest.appendleft(heap)

    def get_top_priority(self):
        """Return least priority, this includes promoting top."""
        if self.is_empty():
            raise IndexError("MutableStableLazyZigzagPairingHeap: pop when empty.")
        self.ensure_top_promoted()
        return self.top_item[0]

    def pop(self):
        """If not empty, extract the least item from self and return that."""
        if self.is_empty():
            raise IndexError("MutableStableLazyZigzagPairingHeap: pop when empty.")
        self.ensure_top_promoted()
        payload = self.top_item[1]
        self.top_item = None
        return payload

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if self.top_item or not self.forrest:
            return
        while len(self.forrest) > 1:
            # zig
            new_forrest = deque()
            while len(self.forrest) > 1:
                latter = self.forrest.pop()
                latter_priority = latter.get_top_priority()
                former = self.forrest.pop()
                former_priority = former.get_top_priority()
                if latter_priority < former_priority:
                    latter.include_before(former)
                    new_forrest.appendleft(latter)
                else:
                    former.include_after(latter)
                    new_forrest.appendleft(former)
            if self.forrest:
                new_forrest.appendleft(self.forrest.pop())
            self.forrest = new_forrest
            # zag
            new_forrest = deque()
            while len(self.forrest) > 1:
                former = self.forrest.popleft()
                former_priority = former.get_top_priority()
                latter = self.forrest.popleft()
                latter_priority = latter.get_top_priority()
                if latter_priority < former_priority:
                    latter.include_before(former)
                    new_forrest.append(latter)
                else:
                    former.include_after(latter)
                    new_forrest.append(former)
            if self.forrest:
                new_forrest.append(self.forrest.pop())
            self.forrest = new_forrest
        new_state = self.forrest.pop()
        self.top_item = new_state.top_item
        self.forrest = new_state.forrest


def mslzph_sort(source):
    """Return new list of (payload, key) pairs, sorted using the mslzp heap."""
    heap = MutableStableLazyZigzagPairingHeap()
    for payload, key in source:
        heap.add(payload, key)
    result = []
    while heap.is_nonempty():
        key = heap.get_top_priority()
        payload = heap.pop()
        result.append((payload, key))
    return result
