"""Design document specifying future Python module."""

from sorted_using_heap import sorted_using_functional_stable_heap
from functional_invalidating_priority_queue import FunctionalInvalidatingPriorityQueue

class FunctionalGreedyBranchInsertHeap(FunctionalInvalidatingPriorityQueue):
    """Heap: An implementation, usable as a queue, least priority value in, first out.
    Functional: After creation, state is never changed. Constructing modified object to return if needed.
    Lazy: Top element is determined only upon pop or peek, in hope to get more relevant comparisons.
    Insert: As Ford-Johnson is inserting leafs into trunk, this also finds better-place for a subtree.
    Branch: Not only leafs, but whole sub-trees can be inserted, to trunk of any sibling sub-tree.
    Gredy: Only one insert operation is considered, taking the most information-effective one at a time.

    Invariant: Each heap is a directed tree, perhaps except it is sub-heap of nothing else,
    when it can be forrest (or tree with top item None).

    One sub-tree insert transforms the tree to another, more narrow one.
    It is possible to count how many linear extensions given tree has,
    by computing some combinatorial numbers in bottom-up manner.
    Most of by-standing sub-trees only contribute by multiplicative factors,
    so we can imagine they are sorted already.

    Some notation is in order. We want to insert sub-tree with top item "a" and other "A" items under it.
    The target is the sibling sub-tree with top item "b0", which has "b1" under it and another "B0" items unrelated to "b1",
    then "b1" has "b2" under it and another "B1" items, and so on, with trunk in interest ending in "bk" item
    with "Bk" items under it and no other distinguishing item.
    After insertion, "a" may end up above "b0", under "bk" or anywhere in the "b" chain.

    We use C(n, k) to denote combinatorial number n!/k!(n-k)!
    Before insertion, the "bk" tree had only one linear extensions (as it is already linear by our assumption),
    with 1+Bk items overall.
    b(k-1) tree has 2+Bk+B(k-1) items, B(k-1) is linear, so it has C(1+Bk+B(k-1), B(k-1)) linear extensions.
    Idea: b(k-1) is definitely first, but then we only need to know set of places B(k-1) items end up at.

    Similarly, at b(k-2) level we incur another C(2+Bk+B(k-1)+B(k-2), B(k-2)) multiplication factor
    from merging in B(k-2), while the b(k-1) factor stays there as well.
    Note that numerator of previous factor is factorial of a number one-off of one of denominator factorial numbers,
    so they (factorials) almost cancel out, the remaining factor is weight of sub-tree in (denominator).

    Now imagine a situation after "a" was inserted somewhere. We have trunk chain one item longer, but what depends on "a" position?
    For overall linear extension count, numerator is the same, factorials in denumerators are the same,
    only the weight factors differ. So for relative comparisons, only product of trunk item weights are important
    (with the top-most one being irrelevant).

    Simple example: A=0, B0=1, B1=0, B2=0, b3 does not exist (occurs in the 5 item Ford-Johnson sort).
    a top: 1*2*4 = 8 in denominator
    a elsewhere (3 cases): 1*2*3 = 6 in denominator.
    Sounds about right. With B0=0 it would be the same (insertion to 3-item chain is perfect)
    but with B0=1 it is relatively harder for "a" to beat b0 as there is one more witness.

    I am not sure what the most efficient way to determine comparison tree for the insertion,
    so for now we will search for best using K^2 search (pairs, triples, and so on until whole chain).
    Each comparison has information content given by its entropy, we can compute average entropy
    and chose the most entropic one (then most comparisons one, then most/least A or similar heuristics).

    The important point is that only value of "k" and then A and B* numbers matter.
    there may be efficient ways to chose proper trunk, but for now we will brute-force it.
    Perhaps one rule may be to stop chain at bk which has strictly smaller overal weight (number of items) than "a" has,
    as at that point it would make more sense to insert bk into "a" and not vice versa.

    Each inner node is potential parent of "a" and b0, but then there may be many equivalent pairs
    of A and B*. To avoid wasting resources, we should cache results for each such "topology",
    and for that we need a way to localize possible trunk types within particular node.
    Also, "extending down" an insertion trunk is efficient (only one factor more for computed positions,
    and one more "a" position to compute). This suggests to favor small A.

    Each tree only grows by inclusions (and narrows-down by inner insertions) so let us talk about what can be tracked.
    If a node has zero or one child, there is no insertion on this level possible.
    If a node has one child, it has only one possibility for trunk extension, so it would be easy pass child data.
    As soon as a node has two childs, it gets complicated. In case the weights are differing, we have two distinct extensions.
    In case weights are the same, we could be examining duplicated state, but on the another hand
    this is a perfect comparison. For now we could require equal-weight links are preferred to (other) insertions.
    Such link comparison should be done as soon as possible. This restores first phase of Ford-Johnson
    and distinguishes from mlwlh which allows linking 2 with 1 or 3 and so on.
    Also, now extensions are guaranteed to produce diferent Bk, which is nice.
    And also "asap" requirement means we never need to choose from three equi-weighting childs.
    Perhaps except invalidate? Yes, that could trim weights, but we can do "chronological order" then.
    Invalidation is not planned to be measured soon, after all.

    This guarantees each leaf ends an unique (maximal) insertion trunk. From the point of view of every ancestor.
    And every inner node ends non-maximal trunk. So "topology" for this part needs no abstraction.
    And at each level, candidate As are different, so every pair on non-root node
    independent element (having non-root node's parent as ancestor) denotes an insertion possibility.
    Note that successful insertion may trigger EWL (Equal Weight Linking), which should probably count to average effectiveness.

    Now, what are the consequences of performed insert (maybe with EWL) on ancestor nodes?
    On A position, nothing. Literally.
    On trunk extensions, depends. All trunks with old "a" position are now invalid, at least its A is now different.
    Trunks avoiding new "a" position look similar, but weights will be different, so whole a/b0 (+ewl) tree has to be rebuilt.
    In other words, trunk remains valid only if its nodes were functionally recycled.
    Also in other words, there is no abstraction either, and the localization is just a lex-ordered set of weight tuples.
    So the localization copies the tree structure, so it is never needed, if insert+ewl creates set
    of nodes that are now garbage, and set of newly functionally created nodes.
    Oh, insert+ewl is guaranteed to free (at least) two childs and create new child of size not present before,
    so just list of weights is our clue to which trunks should be considered.
    All in all it looks like insert+ewl can built set of obsolete and new trunks, so each node experiencing change
    would know which trunks to eliminate and which to add.

    Oh, from local point of view there is no topology, byt from global point of view there is,
    as different sub-trees could attempt the same insertion on their lower branches,
    so we need (A, B*) registry anyway,
    Also, for comparison tree construction it would be useful to keep lower parts of branch+A cached
    so that upper node can build upon that. And make it (A, Bl..k, E) registry, where E is a number of available EWLs,
    as that will affect lower point of best trunk.

    Thinking about it, there is EWL possibility (in principle) if for example Bk contains A-sized child.
    But that does not sound (greedy of first level), so that could be included in later algorithms.

    So we will have registry, I guess mutable one, which would count references.
    It would be updated on the fly, probably on make-before-break basis?
    No. As explained, added/removed trunks always differ on (at least) one weight.
    I can just tell that higher Es should protect smaller ones from getting gc-ed.
    Either by logic, or by counting them explicitly.

    TODO: Update the rest of docstring.

    This heap is also Invalidating, allowing to remove multiple items according to validator.

    This implementation uses Deque to store ordered collection of sub-heaps.
    Note that Deque is mutable."""

    # FIXME: The following is implementation of another Heap.

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

    def is_empty(self):
        """Return boolean corresponding to emptiness of the queue."""
        return self.length < 1

    def is_nonempty(self):
        """Return boolean corresponding to opposite of emptiness of the queue."""
        return self.length > 0

    def ensure_top_demoted(self):
        """In case heap has a top, demote it so merge is easier."""
        if self.top_item is None:
            return self
        return FunctionalStableLazyZigzagPairingHeap(None, Deque[self], self.length)

    def add(self, item):
        """Add item to self, prioritized after current items, do not compare yet."""
        ensured = self.ensure_top_demoted()
        ensured.forrest.append(FunctionalStableLazyZigzagPairingHeap(top_item=item))
        ensured.length += 1
        return ensured

    def include_after(self, heap):
        """Include another heap, prioritized after current items."""
        ensured = self.ensure_top_promoted()
        ensured.forrest.append(heap)
        ensured.length += len(heap)
        return ensured

    def include_before(self, heap):
        """Include another heap, prioritized before current items."""
        ensured = self.ensure_top_promoted()
        ensured.forrest.appendleft(heap)
        ensured.length += len(heap)
        return ensured

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
            return self
        popping_forrest = Deque(self.forrest)
        while len(popping_forrest) > 1:
            # zig
            new_forrest = Deque()
            while len(popping_forrest) > 1:
                # Sub-heaps should always be promoted, but better safe state then be then sorry.
                latter, latter_top = popping_forrest.pop().peek()
                former, former_top = popping_forrest.pop().peek()
                if latter_top < former_top:
                    new_forrest.appendleft(latter.include_before(former))
                else:
                    new_forrest.appendleft(former.include_after(latter))
            if popping_forrest:
                new_forrest.appendleft(popping_forrest.pop())
            popping_forrest = new_forrest
            # zag
            new_forrest = Deque()
            while len(popping_forrest) > 1:
                former, former_top = popping_forrest.popleft().peek()
                latter, latter_top = popping_forrest.popleft().peek()
                if latter_top < former_top:
                    new_forrest.append(latter.include_before(former))
                else:
                    new_forrest.append(former.include_after(latter))
            if popping_forrest:
                new_forrest.append(popping_forrest.pop())
            popping_forrest = new_forrest
        return popping_forrest.pop()

    def invalidate(self, item_is_invalid):
        """Return new queue without items on which the argument function returns true."""
        new_heap = FunctionalStableLazyZigzagPairingHeap()
        if (self.top_item is not None) and (not item_is_invalid(self.top_item)):
            new_heap.top_item = self.top_item
            new_heap.length += 1
        for heap in forrest:
            invalidated = heap.invalidate(item_is_invalid)
            if invalidated:
                if invalidated.top_item is not None:
                    new_heap.forrest.append(invalidated)
                else:
                    new_heap.forrest.extend(invalidated.forrest)
                new_heap.length += len(invalidated)
        return new_heap

def fslzph_sorted(source):
    """Return new list of items, sorted using the mslzp heap."""
    return sorted_using_functional_stable_heap(FunctionalStableLazyZigzagPairingHeap, source)
