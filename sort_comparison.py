import math
import operator
import random
import sys
import time

from pep_3140 import List
from comparison_counting_wrapper import ComparisonCountingWrapper
from comparison_counting_wrapper import SimpleCounter
from mutable_stable_lazy_zigzag_pairing_heap import mslzph_sorted
from mutable_stable_lazy_zigzag_pairing_weak_heap import mslzpwh_sorted
from functional_stable_lazy_zigzag_pairing_heap import fslzph_sorted
from mutable_inclusion_preferring_lazy_zigzag_pairing_heap import miplzph_sorted
from mutable_lazy_weight_linking_heap import mlwlh_sorted
from halving_ford_johnson_sort import hfj_sorted
from complete_ford_johnson_sort import cfj_sorted
from reordered_ford_johnson_sort import rfj_sorted


class SortAtLength(object):
    """Class for holding information about sort test progress."""

    def __init__(self, tested_sort, length):
        """Initialize."""
        self.sort = tested_sort
        self.length = length
        self.runs = 0
        self.summ = 0.0
        self.sqsumm = 0.0
        self.time = 0.0
        print '.',
        sys.stdout.flush()
        self.add_run()
        self.add_run()

    def add_run(self):
        """Perform next test run and update counters."""
        counter = SimpleCounter()
        source = List([ComparisonCountingWrapper(index, counter) for index in range(self.length)])
        random.seed(self.runs + 42)
        random.shuffle(source)
        time_start = time.time()
        wrapped_result = self.sort(source)
        time_stop = time.time()
        result = List([item.value for item in wrapped_result])
        assert result == List(range(self.length)), str(result)
        self.summ += counter.count
        self.sqsumm += counter.count * counter.count
        self.time += time_stop - time_start
        self.runs += 1

    def get_average(self):
        """Return average number of comparisons so far."""
        return self.summ / self.runs

    def get_sigma_squared(self):
        """Return sigma describing precision of measured average."""
        return (self.runs * self.sqsumm - self.summ * self.summ) / (self.runs - 1.8) / (self.runs * self.runs)


class SortOverRange(object):
    """Class for holding information about sort test progress, range agregation part."""

    def __init__(self, tested_sort, weight, name, length_limit):
        """Initialize."""
        self.sort = tested_sort
        self.weight = weight
        self.name = name
        self.length = length_limit
        print "Creating base data for", name
        self.sorts = [SortAtLength(tested_sort, length) for length in range(length_limit)]
        print
        self.runs = 2
        self.time = sum([sort.time for sort in self.sorts])

    def add_run(self):
        """Perform next test run and update counters."""
        [sort.add_run() for sort in self.sorts]
        self.time = sum([sort.time for sort in self.sorts])
        self.runs += 1

    def get_average(self):
        """Return average number of comparisons so far."""
        return sum([sort.get_average() for sort in self.sorts])

    def get_sigma(self):
        """Return sigma describing precision of measured average."""
        return math.sqrt(sum([sort.get_sigma_squared() for sort in self.sorts]))

    def get_priority(self):
        """Return numeric value indicating progress of testing."""
        return self.time / self.weight


sorts_input = (
    (sorted, 2, "timsort"),
    (rfj_sorted, 20, "rfj"),
    (cfj_sorted, 16, "cfj"),
    (hfj_sorted, 4, "hfj"),
    (mlwlh_sorted, 2, "mlwlh"),
    (miplzph_sorted, 2, "miplzph"),
    (mslzph_sorted, 2, "mslzph"),
    (mslzpwh_sorted, 2, "mslzpwh"),
    (fslzph_sorted, 2, "fslzph"),
)

length = 257
print "Testing on range up to", length
sorts = [SortOverRange(item[0], item[1], item[2], length) for item in sorts_input]
while 1:
    sorts = sorted(sorts, key=operator.attrgetter("weight", "name"))
    for sort in sorts:
        print sort.name, ": average", sort.get_average(), "sigma", sort.get_sigma(), "time average", sort.time / sort.runs, "runs", sort.runs
    sorts = sorted(sorts, key=operator.methodcaller("get_priority"))
    print
    print "Getting more data for", sorts[0].name
    sorts[0].add_run()
