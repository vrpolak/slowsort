"""Module that defines mutable inclusion preferring zigzag pairing heap."""

from pep_3140 import Deque
from pep_3140 import List
from sorted_using_heap import sorted_using_mutable_unstable_heap
from mutable_priority_queue import MutablePriorityQueue


class MutableInclusionPreferringLazyZigzagPairingHeap(MutablePriorityQueue):
    """A heap that is mutable, inclusion preferring, lazy, and zigzag pairing.

    Heap: An implementation, usable as a queue, least priority value in, first out.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Inclusion preferring: Only one inclusion method, included heap is preferred to existing ones.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.
    This heap does NOT result in stable sort algorithm.

    This implementation uses Deque to store ordered collection of sub-heaps."""

    def __init__(self, top_item=None, forest=None):
        """Initialize a queue."""
        self.top_item = top_item
        self.forest = forest if forest is not None else Deque()

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return
        demoted = MutableInclusionPreferringLazyZigzagPairingHeap(self.top_item, self.forest)
        self.top_item = None
        self.forest = Deque([demoted])

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        self.ensure_top_demoted()
        heap = MutableInclusionPreferringLazyZigzagPairingHeap(top_item=item)
        # Addition is not inclusion, so late items are not preferred.
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
                # Subheaps should be nonempty and have top promoted already.
                if latter.top_item < former.top_item:
                    latter._include_before(former)
                    new_forest.appendleft(latter)
                else:
                    former._include_before(latter)
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
                    former._include_before(latter)
                    new_forest.append(former)
            if self.forest:
                new_forest.append(self.forest.pop())
            self.forest = new_forest
        new_state = self.forest.pop()
        self.top_item = new_state.top_item
        self.forest = new_state.forest


def miplzph_sorted(source):
    """Return new list of items, sorted using the mslzp heap."""
    return sorted_using_mutable_unstable_heap(MutableInclusionPreferringLazyZigzagPairingHeap, source)
