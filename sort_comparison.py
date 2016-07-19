import math
import random
import sys
import time

from pep_3140 import List
from comparison_counting_wrapper import ComparisonCountingWrapper
from comparison_counting_wrapper import SimpleCounter
from mutable_stable_lazy_zigzag_pairing_heap import mslzph_sorted
from functional_stable_lazy_zigzag_pairing_heap import fslzph_sorted
from mutable_inclusion_preferring_lazy_zigzag_pairing_heap import miplzph_sorted
from mutable_lazy_weight_linking_heap import mlwlh_sorted
from halving_ford_johnson_sort import hfj_sorted
from complete_ford_johnson_sort import cfj_sorted
from reordered_ford_johnson_sort import rfj_sorted


def sort_test_core(tested_sort, N, summ, sqsumm, time_total):
    """Run one sort, assert, return updated counters."""
    # TODO: Bring back longest.
    counter = SimpleCounter()
    source = List([ComparisonCountingWrapper(index, counter) for index in range(N)])
    random.shuffle(source)
    time_start = time.time()
    result = List([item.value for item in tested_sort(source)])
    time_stop = time.time()
    assert result == List(range(N)), str(result)
    return summ + counter.count, sqsumm + counter.count * counter.count, time_total + (time_stop - time_start)


def sort_test(tested_sort, N, M, name, seed=42):
    """Test one algorithm at one length multiple times."""
    random.seed(seed)
    print "testing", name, "averaging over M:", M, "...",
    sys.stdout.flush()
    comp_sum = 0.0
    comp_sqsum = 0.0
    time_total = 0.0
    for iteration in range(M):
        comp_sum, comp_sqsum, time_total = sort_test_core(tested_sort, N, comp_sum, comp_sqsum, time_total)
    print ":", "avg:", comp_sum / M, "sigma:", math.sqrt((M * comp_sqsum - comp_sum * comp_sum) / (M - 1)) / M, "time", time_total

N = 1000
print "comparing at N:", N
m = 100

sort_test(rfj_sorted, N, 40 * m, "rfj")

sort_test(cfj_sorted, N, 40 * m, "cfj")

sort_test(hfj_sorted, N, 40 * m, "hfj")

sort_test(mlwlh_sorted, N, 1 * m, "mlwlh")

sort_test(miplzph_sorted, N, 2 * m, "miplzph")

sort_test(mslzph_sorted, N, 2 * m, "mslzph")

sort_test(fslzph_sorted, N, 2 * m, "fslzph")
