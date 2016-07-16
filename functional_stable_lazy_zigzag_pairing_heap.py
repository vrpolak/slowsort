"""Module that defines functional stable zigzag pairing heap."""

from collections import deque
from functional_priority_queue import FunctionalPriorityQueue

class FunctionalStableLazyZigzagPairingHeap(FunctionalPriorityQueue):
    """Heap: An implementation, usable as a queue, least priority value in, first out.
    Functional: After creation, state is never changed. Constructing modified object to return if needed.
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

    def __len__(self):
        """Return number of stored elements."""
        length = len(self.forrest)
        if self.top_item:
            length += 1
        return length

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        return (not self.forrest) and (not self.top_item)

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        return not self.is_empty()

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if not self.top_item:
            return self
        demoted = FunctionalStableLazyZigzagPairingHeap(self.top_item, self.forrest)
        return FunctionalStableLazyZigzagPairingHeap(None, deque[demoted])

    def add(self, payload, priority):
        """Add item to self, prioritized after current items, do not compare yet."""
        ensured = self.ensure_top_demoted()
        item = (priority, payload)
        heap = FunctionalStableLazyZigzagPairingHeap(top_item=item)
        ensured.forrest.append(heap)
        return ensured

    def include_after(self, heap):
        """Include another heap, prioritized after current items."""
        ensured = self.ensure_top_promoted()
        ensured.forrest.append(heap)
        return ensured

    def include_before(self, heap):
        """Include another heap, prioritized before current items."""
        ensured = self.ensure_top_promoted()
        ensured.forrest.appendleft(heap)
        return ensured

    def get_top_priority(self):
        """Return heap with top promoted and priority of top."""
        if self.is_empty():
            raise IndexError("FunctionalStableLazyZigzagPairingHeap: pop when empty.")
        promoted = self.ensure_top_promoted()
        return promoted, promoted.top_item[0]

    def pop(self):
        """If not empty, return tuple of the smaller queue and the least item."""
        if self.is_empty():
            raise IndexError("FunctionalStableLazyZigzagPairingHeap: pop when empty.")
        ensured = self.ensure_top_promoted()
        payload = ensured.top_item[1]
        ensured.top_item = None
        return ensured, payload

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if self.top_item or not self.forrest:
            return self
        popping_forrest = deque(self.forrest)
        while len(popping_forrest) > 1:
            # zig
            new_forrest = deque()
            while len(popping_forrest) > 1:
                latter = popping_forrest.pop()
                latter, latter_priority = latter.get_top_priority()
                former = popping_forrest.pop()
                former, former_priority = former.get_top_priority()
                if latter_priority < former_priority:
                    new_forrest.appendleft(latter.include_before(former))
                else:
                    new_forrest.appendleft(former.include_after(latter))
            if popping_forrest:
                new_forrest.appendleft(popping_forrest.pop())
            popping_forrest = new_forrest
            # zag
            new_forrest = deque()
            while len(popping_forrest) > 1:
                former = popping_forrest.popleft()
                former, former_priority = former.get_top_priority()
                latter = popping_forrest.popleft()
                latter, latter_priority = latter.get_top_priority()
                if latter_priority < former_priority:
                    new_forrest.append(latter.include_before(former))
                else:
                    new_forrest.append(former.include_after(latter))
            if popping_forrest:
                new_forrest.append(popping_forrest.pop())
            popping_forrest = new_forrest
        return popping_forrest.pop()


def fslzph_sort(source):
    """Return new list of (payload, key) pairs, sorted using the mslzp heap."""
    heap = FunctionalStableLazyZigzagPairingHeap()
    for payload, key in source:
        heap = heap.add(payload, key)
    result = []
    while heap.is_nonempty():
        heap, key = heap.get_top_priority()
        heap, payload = heap.pop()
        result.append((payload, key))
    return result
