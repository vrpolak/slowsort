"""Module collecting utilities for testing sorted-compatible algorithms."""

import logging
import random
import sys

from pep_3140 import List
from comparison_logging_wrapper import ComparisonLoggingWrapper as Lwrap
from comparison_counting_wrapper import ComparisonCountingWrapper as Cwrap
from comparison_counting_wrapper import SimpleCounter as Counter

# FIXME: Replace this with introspectable logger, to avoid eye-independent tests.
log = logging.getLogger("logging_test")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

# TODO: Add heap emptiness tests.
# TODO: Add sort stability tests.

def verbose_test(sort, bare_source):
    """Few tests using logger and small source."""
    print "Verbose test with", repr(source)
    source = List([ComparisonLoggingWrapper(value, log) for value in bare_source])
    result = List([item.value for item in sort(source)])
    assert result == sorted(bare_source), str(result)

def counting_test(sort, size, seed=42):
    """Random sfuffle range of given size, sort using counting wrapper and print result"""
    print "Counting test on length", len(bare_source),
    sys.stdout.flush
    random.seed(seed)
    source = List(range(size))
    random.shuffle(source)
    counter = Counter()
    wrapped_source = List([ComparisonCountingWrapper(value, counter) for value in bare_source])
    result = List([item.value for item in sort(wrapped_source)])
    print "used", counter.count, "comparisons."
    assert result == sorted(bare_source), str(result)

def suite(sort, scale=100, seed=42):
    verbose_test(sort, [])
    verbose_test(sort, [0])
    verbose_test(sort, [0, 1])
    verbose_test(sort, [1, 0])
    verbose_test(sort, range(21))
    verbose_test(sort, range(20, -1, -1))
    for size in range(scale):
        counting_test(sort, size)
