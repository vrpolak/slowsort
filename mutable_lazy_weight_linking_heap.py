"""Module that defines mutable weight linking lazy heap."""

from pep_3140 import List
from comparable_payload import ComparablePayload
from sorted_using_heap import sorted_using_mutable_unstable_counting_heap
from mutable_counting_priority_queue import MutableCountingPriorityQueue


class MutableLazyWeightLinkingHeap(MutableCountingPriorityQueue):
    """A heap that is mutable, lazy and weight linking.

    Heap: An implementation, usable as a queue, least priority value in, first out.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Linking: Top is found by repeated linking of two sub-heaps, but selection is not a simple pairing.
    Weight: The two heaps to link are the ones with least elements in them.
    This heap does NOT result in stable sort algorithm.

    This implementation uses List and sort() to store collection of sub-heaps.

    Sub-heaps are prioritized by their length, so item of forest is ComparablePayload(length, sub-heap)
    Items are checked by "is None", as empty string and zero are valid items with false truth value."""

    def __init__(self, top_item=None, forest=None, known_weight=None):
        """Initialize the heap, possibly to a prepared state."""
        self.top_item = top_item
        self.forest = forest if forest is not None else List()
        # It is not called known_length as there may be different weight algorithms in future.
        if known_weight is not None:
            self.weight = known_weight
            return
        if forest:
            raise NotImplementedError("Implement iteration over MutableStableLazyZigzagPairingHeap which does not change its state.")
        self.weight = 0 if top_item is None else 1

    def __len__(self):
        """Return number of items stored."""
        return self.weight

    def is_empty(self):
        """Return boolean corresponding to emptiness of the heap."""
        return self.weight < 1

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the heap."""
        return self.weight > 0

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return
        known_weight = self.weight
        demoted = MutableLazyWeightLinkingHeap(self.top_item, self.forest, known_weight)
        self.top_item = None
        self.forest = List([ComparablePayload(known_weight, demoted)])

    def add(self, item):
        """Add item to self, do not compare yet."""
        self.ensure_top_demoted()
        singleton_heap = MutableLazyWeightLinkingHeap(top_item=item)
        self.forest.append(ComparablePayload(1, singleton_heap))
        self.weight += 1

    def _include(self, heap):
        """Include another heap, no comparisons other than to top, which is assumed to be done already."""
        weight = len(heap)
        self.forest.append(ComparablePayload(weight, heap))
        self.weight += weight

    def peek(self):
        """If not empty, locate the least item and return that."""
        if self.is_empty():
            raise IndexError("MutableLazyWeightLinkingHeap: pop when empty.")
        self.ensure_top_promoted()
        return self.top_item

    def pop(self):
        """If not empty, extract the least item from self and return that."""
        if self.is_empty():
            raise IndexError("MutableLazyWeightLinkingHeap: pop when empty.")
        self.ensure_top_promoted()
        item = self.top_item
        self.top_item = None
        self.weight -= 1
        return item

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if (self.top_item is not None) or (not self.forest):
            return
        while len(self.forest) > 1:
            self.forest.sort()
            smaller = self.forest[0].payload
            bigger = self.forest[1].payload
            # Sub-heaps should be nonempty and have top promoted.
            if smaller.top_item <= bigger.top_item:
                smaller._include(bigger)
                self.forest[:2] = []
                self.forest.append(ComparablePayload(len(smaller), smaller))
            else:
                bigger._include(smaller)
                self.forest[:2] = []
                self.forest.append(ComparablePayload(len(bigger), bigger))
        new_state = self.forest[0].payload
        self.top_item = new_state.top_item
        self.forest = new_state.forest


def mlwlh_sorted(source):
    """Return new list of itemss, sorted using the mslzp heap."""
    return sorted_using_mutable_unstable_counting_heap(MutableLazyWeightLinkingHeap, source)
