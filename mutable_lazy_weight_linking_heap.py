"""Module that defines mutable weight linking lazy heap."""

from mutable_stable_lazy_zigzag_pairing_heap import MutableStableLazyZigzagPairingHeap as queue
from mutable_priority_queue import MutablePriorityQueue

class MutableLazyWeightLinkingHeap(MutablePriorityQueue):
    """Heap: An implementation, usable as a queue, least priority value in, first out.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Linking: Top is found by repeated linking of two sub-heaps, but selection is not a simple pairing.
    Weight: The two heaps to link are the ones with least elements in them.
    This heap does NOT result in stable sort algorithm.

    This implementation uses MutableStableLazyZigzagPairingHeap to store collection of sub-heaps."""

    def __init__(self, top_item=None, forrest=None):
        """Initialize the heap, possibly to a prepared state."""
        self.top_item = top_item
        self.forrest = forrest or queue()
        self.weight = len(self.forrest)
        if self.top_item:
            self.weight += 1

    def __len__(self):
        """Return number of items stored."""
        return self.weight

    def is_empty(self):
        """Return boolean corresponding to emptiness of the heap."""
        return self.weight < 1

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the heap."""
        return not self.is_empty()

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if not self.top_item:
            return
        demoted = MutableLazyWeightLinkingHeap(self.top_item, self.forrest)
        self.top_item = None
        self.forrest = queue().add(demoted, len(demoted))

    def add(self, payload, priority):
        """Add item to self, do not compare yet."""
        self.ensure_top_demoted()
        item = (priority, payload)
        heap = MutableLazyWeightLinkingHeap(top_item=item)
        # assert len(heap) == 1
        self.forrest.add(heap, 1)
        self.weight += 1

    def include(self, heap):
        """Include another heap, no comparisons other than to top, which is assumed to be done already."""
        self.ensure_top_promoted()
        len_heap = len(heap)
        self.forrest.add(heap, len_heap)
        self.weight += len_heap

    def get_top_priority(self):
        """Return least priority, this includes promoting top."""
        if self.is_empty():
            raise IndexError("MutableLazyWeightLinkingHeap: pop when empty.")
        self.ensure_top_promoted()
        return self.top_item[0]

    def pop(self):
        """If not empty, extract the least item from self and return that."""
        if self.is_empty():
            raise IndexError("MutableLazyWeightLinkingHeap: pop when empty.")
        self.ensure_top_promoted()
        payload = self.top_item[1]
        self.top_item = None
        self.weight -= 1
        return payload

    def ensure_top_promoted(self):
        """Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade."""
        if self.top_item or not self.forrest:
            return
        while len(self.forrest) > 1:
            smaller = self.forrest.pop()
            smaller_priority = smaller.get_top_priority()
            bigger = self.forrest.pop()
            bigger_priority = bigger.get_top_priority()
            if smaller_priority <= bigger_priority:
                smaller.include(bigger)
                self.forrest.add(smaller, len(smaller))
            else:
                bigger.include(smaller)
                self.forrest.add(bigger, len(bigger))
        new_state = self.forrest.pop()
        self.top_item = new_state.top_item
        self.forrest = new_state.forrest


def mlwlh_sort(source):
    """Return new list of (payload, key) pairs, sorted using the mslzp heap."""
    heap = MutableLazyWeightLinkingHeap()
    for payload, key in source:
        heap.add(payload, key)
    result = []
    while heap.is_nonempty():
        key = heap.get_top_priority()
        payload = heap.pop()
        result.append((payload, key))
    return result
