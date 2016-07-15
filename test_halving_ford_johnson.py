import logging
import random
import sys

from pep_3140 import list_str
from comparison_logging_wrapper import ComparisonLoggingWrapper as Lwrap
from comparison_counting_wrapper import ComparisonCountingWrapper as Cwrap
from comparison_counting_wrapper import SimpleCounter as Counter
from halving_ford_johnson_sort import halving_ford_johnson_sort as sort

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
    result = sort(source)
    unwrap = [item.value for item in result]
    sorted_integer_list = sorted(list(integer_list))
    if not unwrap == sorted_integer_list:
        msg = "result: " + list_str(unwrap) + ", sorted source: " + list_str(sorted_integer_list)
        raise AssertionError(msg)

# Sort empty, no log seen.
print "empty"
visual_test([])

# Sort single, no log seen.
print "single"
visual_test([0])

# Sort sorted pair, see one comparison.
print "sorted pair"
visual_test([0, 1])

# Sort anti-sorted pair, see one comparison.
print "antisorted pair"
visual_test([1, 0])

# Sort already sorted: N=21.
print "sorted 21"
visual_test(list(range(21)))

# Sort antisorted, N=21.
print "antisorted 21"
source = list(range(21))
source.reverse()
visual_test(source)

# Random shuffles as I do not feel like constructing a worst case.
print "random M N tests"
M = 100
N = 21
for iteration in range(M):
    counter = Counter()
    source = list(range(N))
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

# Increasingly long shuffles on unwrapped integers, to check correctness.
print "random 1..M tests"
M = 2000
for N in range(M):
    source = list(range(N))
    random.shuffle(source)
    result = sort(source)
    assert result == range(N)
