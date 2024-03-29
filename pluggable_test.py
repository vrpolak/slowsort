"""Module collecting utilities for testing sorted-compatible algorithms."""

import logging
import random
import sys

from pep_3140 import List
from comparison_logging_wrapper import ComparisonLoggingWrapper
from comparison_counting_wrapper import ComparisonCountingWrapper
from comparison_counting_wrapper import SimpleCounter
from interactive_comparison_wrapper import InteractiveComparisonWrapper

# FIXME: Replace this with introspectable logger, to avoid eye-independent tests.
log = logging.getLogger("logging_test")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

# TODO: Add heap emptiness tests.
# TODO: Add sort stability tests.

def verbose_test(sort, bare_source):
    """Few tests using logger and small source."""
    print(f"Verbose test with {bare_source}")
    source = List([ComparisonLoggingWrapper(value, log) for value in bare_source])
    result = List([item.value for item in sort(source)])
    assert result == sorted(bare_source), str(result)

def counting_test(sort, size, seed=42):
    """Random sfuffle range of given size, sort using counting wrapper and print result"""
    print(f"Counting test on length {size}")
    sys.stdout.flush
    random.seed(seed)
    source = List(range(size))
    random.shuffle(source)
    counter = SimpleCounter()
    wrapped_source = List([ComparisonCountingWrapper(value, counter) for value in source])
    result = List([item.value for item in sort(wrapped_source)])
    print(f"used {counter.count} comparisons.")
    assert result == List(range(size)), str(result)
    return counter.count

def interactive_test(sort):
    items = List()
    while 1:
        item = input("Next identifier, empty for end of list to sort: ")
        if not item:
            break
        if item in items:
            print("Already present, try again.")
        else:
            items.append(item)
            print(f"Ok, {len(items)} items so far.")
    wrapped = List([InteractiveComparisonWrapper(item) for item in items])
    print("Sorting starts")
    result = List([item.value for item in sort(wrapped)])
    print("Sorted, listing in order:")
    for value in result:
        print(f"{value}")

def suite(sort, scale=100, seed=42):
    verbose_test(sort, [])
    verbose_test(sort, [0])
    verbose_test(sort, [0, 1])
    verbose_test(sort, [1, 0])
    verbose_test(sort, range(21))
    verbose_test(sort, range(20, -1, -1))
    count = 0
    for size in range(scale):
        count += counting_test(sort, size)
    print(f"Total count needed for scale tests: {count}")
    interactive_test(sort)
