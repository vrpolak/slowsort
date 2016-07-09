import logging
import sys

from comparison_logging_wrapper import ComparisonLoggingWrapper as Wrap
from mutable_stable_lazy_zigzag_pairing_heap import MutableStableLazyZigzagPairingHeap as Heap

# FIXME: Replace this with introspectable logger, to eye-independent tests.
log = logging.getLogger("logging_test")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

def empty_check(heap, name):
    """Try to pop, catch and comment exception, fail assert otherwise."""
    try:
        obj = heap.pop()
    except IndexError:
        print name, "works ok."
    else:
        raise AssertionError("not emptied: %s", name)

def wrap(value):
    """Wrap using "log" logger."""
    return Wrap(value, log)

one = wrap(1)
two = wrap(2)
assert one != two
assert one < two
assert two > one

heap = Heap()
empty_check(heap, "empty")

heap = Heap()
heap.add(1, one)
pri = heap.get_top_priority()
assert pri is one
popped = heap.pop()
# No log seen.
assert popped == 1
empty_check(heap, "one")

heap = Heap()
heap.add(1, one)
heap.add(2, two)
pri = heap.get_top_priority()
# Log should be seen.
assert pri is one
popped = heap.pop()
assert popped == 1
popped = heap.pop()
assert popped == 2
empty_check(heap, "12")

heap = Heap()
heap.add(2, two)
heap.add(1, one)
popped = heap.pop()
# Log should be seen.
assert popped == 1
popped = heap.pop()
assert popped == 2
empty_check(heap, "12")
