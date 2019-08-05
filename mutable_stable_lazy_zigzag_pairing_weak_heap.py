"""Module that defines mutable stable zigzag pairing weak heap."""

from weakref import ref

from pep_3140 import Deque
from pep_3140 import List
from sorted_using_weak_heap import sorted_using_mutable_stable_weak_heap
from mutable_priority_weak_queue import MutablePriorityWeakQueue


def _ref_or_none(item):
    """Return weak reference if item is (or points to) non-None, else return None."""
    if isinstance(item, ref):
        item = item()
    return None if item is None else ref(item)


def _item_or_none(reference):
    """Return weakly referenced item, or None if reference is None or the item is dead."""
    return None if reference is None else reference()


class MutableStableLazyZigzagPairingWeakHeap(MutablePriorityWeakQueue):
    """A weak heap that is mutable, stable, lazy and zigzag pairing.

    Heap: An implementation, usable as a queue, least priority value in, first out.
    Weak: Not a container. Items can vanish from the queue, iff they gets garbage collected.
    Lazy: Least element is determined only upon pop, in hope to get more relevant comparisons.
    Mutable: Self is altered regularily to avoid excessive object creation.
    Stable: Two include methods to allow caller decide tiebreaker.
    Pairing: Most subheap comparisons are on pairs of "equal" sub-heaps.
    Zigzag: The odd sub-heap is left at alternating ends.

    This implementation uses Deque to store ordered collection of sub-heaps."""

    def __init__(self, top_item=None, forest=None):
        """Initialize a queue."""
        self.top_ref = _ref_or_none(top_item)
        self.forest = forest if forest is not None else Deque()

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        self.top_ref = _ref_or_none(self.top_ref)
        if self.top_ref is None:
            return
        demoted = MutableStableLazyZigzagPairingWeakHeap(self.top_ref, self.forest, self.length)
        self.top_ref = None
        self.forest = Deque([demoted])

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        self.ensure_top_demoted()
        self.forest.append(MutableStableLazyZigzagPairingWeakHeap(top_item=item))

    def _include_after(self, heap):
        """Include another heap, forest-ordered after current items."""
        # Do not ensure top promoted, as it was the previous top who won comparison.
        self.forest.append(heap)

    def _include_before(self, heap):
        """Include another heap, forest-ordered before current items."""
        # Do not ensure top promoted, as it was the previous top who won comparison.
        self.forest.appendleft(heap)

    def peek(self):
        """Return least priority item or None if empty, this includes promoting top, but not extraction.

        This also acts as ensure_top_promoted.

        Do pairwise includes in zigzag fashion until there is only one tree. Then upgrade.
        Return the top item (not weakref) to make sure top stay promoted (instead of vanishing).
        """
        top_item = _item_or_none(self.top_ref)
        if (top_item is not None) or (not self.forest):
            return top_item
        # In order to prevent returning None on nonempty heap,
        # we need to track any comparison winner, to prevent it from dying.
        protected = None
        while len(self.forest) > 1:
            # zig
            new_forest = Deque()
            while len(self.forest) > 1:
                latter_heap = self.forest.pop()
                former_heap = self.forest.pop()
                # We need to peek and check for None as items might got deleted.
                latter_item = latter_heap.peek()
                former_item = former_heap.peek()
                if latter_item is None:
                    if former_item is None:
                        continue
                    else:
                        self.forest.append(former_heap)
                        continue
                if former_item is None:
                    self.forest.append(latter_heap)
                    continue
                if latter_item < former_item:
                    protected = latter_item
                    latter_heap._include_before(former_heap)
                    new_forest.appendleft(latter_heap)
                else:
                    protected = former_item
                    former_heap._include_after(latter_heap)
                    new_forest.appendleft(former_heap)
            if self.forest:
                new_forest.appendleft(self.forest.pop())
            self.forest = new_forest
            # zag
            new_forest = Deque()
            while len(self.forest) > 1:
                former_heap = self.forest.popleft()
                latter_heap = self.forest.popleft()
                former_item = former_heap.peek()
                latter_item = latter_heap.peek()
                if latter_item is None:
                    if former_item is None:
                        continue
                    else:
                        self.forest.appendleft(former_heap)
                        continue
                if former_item is None:
                    self.forest.appendleft(latter_heap)
                    continue
                if latter_item < former_item:
                    protected = latter_item
                    latter_heap._include_before(former_heap)
                    new_forest.append(latter_heap)
                else:
                    protected = former_item
                    former_heap._include_after(latter_heap)
                    new_forest.append(former_heap)
            if self.forest:
                new_forest.append(self.forest.pop())
            self.forest = new_forest
        new_state = self.forest.pop()
        self.top_ref = new_state.top_ref
        self.forest = new_state.forest
        top_item = _item_or_none(self.top_ref)
        return protected if top_item is None else top_item

    def pop(self):
        """Extract the least item from self and return that, or None if empty."""
        item = self.peek()
        self.top_ref = None
        return item


def mslzpwh_sorted(source):
    """Return new List of items, sorted using the mslzpw heap."""
    return sorted_using_mutable_stable_weak_heap(MutableStableLazyZigzagPairingWeakHeap, source)
