import logging
import random
import sys

from comparison_logging_wrapper import ComparisonLoggingWrapper as Lwrap
from comparison_counting_wrapper import ComparisonCountingWrapper as Cwrap
from comparison_counting_wrapper import SimpleCounter as Counter
from ford_johnson_sort import ford_johnson_sort as sort

# FIXME: Replace this with introspectable logger, to eye-independent tests.
log = logging.getLogger("logging_test")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

def wrap(value):
    """Wrap using "log" logger."""
    return Lwrap(value, log)

def visual_test(integer_list):
    """Basic test logic for test which use wrappers to log comparisons."""
    source = map(wrap, integer_list)
    result = sort(source[:])
    sorted_source = sorted(source)
    if not result == sorted_source:
        msg = "result: " + str(result) + ", source: " + str(sorted_source)
        raise AssertionError(msg)

# Sort empty, no log seen.
visual_test([])

# Sort single, no log seen.
visual_test([0])

# Sort sorted pair, see one comparison.
visual_test([0, 1])

# Sort anti-sorted pair, see one comparison.
visual_test([1, 0])

# Sort already sorted: N=21.
visual_test(range(21))

# Sort antisorted, N=21.
visual_test(range(21).reverse())

# Random shuffles as I do not feel like constructing a worst case.
M = 100
N = 21
for iteration in range(M):
    counter = Counter()
    source = range(N)
    random.shuffle(source)
    print repr(source)
    wrapped = []
    for index in source:
        wrapped.append(Cwrap(index, counter))
    result = sort(wrapped)
    unwrapped = []
    for item in result:
        unwrapped.append(item.value)
    print counter.count
    assert unwrapped == range(N)
