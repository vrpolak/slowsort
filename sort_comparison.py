import math
import random
import sys
import time

from comparison_counting_wrapper import ComparisonCountingWrapper as Wrap
from comparison_counting_wrapper import SimpleCounter as Counter
from mutable_stable_lazy_zigzag_pairing_heap import mslzph_sort
from mutable_inclusion_preferring_lazy_zigzag_pairing_heap import miplzph_sort
from mutable_lazy_weight_linking_heap import mlwlh_sort
from ford_johnson_sort import ford_johnson_sort_tuples as fj_sort

# FIXME: Rework sorts to follow the same protocol so that adapters are not needed as much.

def sort_test(tested_sort, N, M, name):
    """Common logic for testing one algorithm."""
    print "testing", name, "...",
    sys.stdout.flush()
    time_start = time.time()
    state = random.getstate()
    comp_sum = 0.0
    comp_sqsum = 0.0
    longest = 0
    for iteration in range(M):
        counter = Counter()
        source = []
        for index in range(N):
            source.append((index, Wrap(index, counter)))
        random.shuffle(source)
        result = tested_sort(source)
        for index in range(N):
            assert result[index][0] == index
        if counter.count > longest:
            longest = counter.count
        comp_sum += counter.count
        comp_sqsum += counter.count * counter.count
    random.setstate(state)
    time_stop = time.time()
    print ":", "longest:", longest, "avg:", comp_sum / M, "sigma:", math.sqrt((M * comp_sqsum - comp_sum * comp_sum) / (M - 1)) / M, "time", time_stop - time_start

M = 1000
print "averaging over M:", M
N = 1000
print "comparing at N:", N

sort_test(fj_sort, N, M, "fj")

sort_test(mlwlh_sort, N, M, "mlwlh")

sort_test(miplzph_sort, N, M, "miplzph")

sort_test(mslzph_sort, N, M, "mslzph")
