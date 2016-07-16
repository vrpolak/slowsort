import logging
import random
import sys

from comparison_logging_wrapper import ComparisonLoggingWrapper as Lwrap
from comparison_counting_wrapper import ComparisonCountingWrapper as Cwrap
from comparison_counting_wrapper import SimpleCounter as Counter
from functional_stable_lazy_zigzag_pairing_heap import FunctionalStableLazyZigzagPairingHeap as Heap

# FIXME: Replace this with introspectable logger, to eye-independent tests.
log = logging.getLogger("logging_test")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

def empty_check(heap, name):
    """Try to pop, catch and comment exception, fail assert otherwise."""
    try:
        heap, obj = heap.pop()
    except IndexError:
        print name, "works ok."
    else:
        raise AssertionError("not emptied: %s", name)

def wrap(value):
    """Wrap using "log" logger."""
    return Lwrap(value, log)

one = wrap(1)
two = wrap(2)

heap = Heap()
empty_check(heap, "empty")

heap = Heap()
heap = heap.add(1, one)
heap, pri = heap.get_top_priority()
assert pri is one
heap, popped = heap.pop()
# No log seen.
assert popped == 1
empty_check(heap, "one")

heap = Heap()
heap = heap.add(1, one)
heap = heap.add(2, two)
heap, pri = heap.get_top_priority()
# Log should be seen.
assert pri is one
heap, popped = heap.pop()
assert popped == 1
heap, popped = heap.pop()
assert popped == 2
empty_check(heap, "12")

heap = Heap()
heap = heap.add(2, two)
heap = heap.add(1, one)
heap, popped = heap.pop()
# Log should be seen.
assert popped == 1
heap, popped = heap.pop()
assert popped == 2
empty_check(heap, "21")

# Sort already sorted: N=21.
N = 21
heap = Heap()
for index in range(N):
    heap = heap.add(index, wrap(index))
result = []
for index in range(N):
    heap, item = heap.pop()
    result.append(item)
assert result == range(N)
empty_check(heap, "s21")

# Sort antisorted, N=21.
N = 21
heap = Heap()
for index in range(N - 1, -1, -1):
    heap = heap.add(index, wrap(index))
result = []
for index in range(N):
    heap, item = heap.pop()
    result.append(item)
assert result == range(N)
empty_check(heap, "a21")

# Random shuffles as I do noty feel like constructing a worst case.
M = 100
N = 21
for iteration in range(M):
    counter = Counter()
    source = list(range(N))
    random.shuffle(source)
    print repr(source)
    for index in source:
        heap = heap.add(index, Cwrap(index, counter))
    result = []
    for index in range(N):
        heap, item = heap.pop()
        result.append(item)
    print counter.count
    assert result == range(N)
