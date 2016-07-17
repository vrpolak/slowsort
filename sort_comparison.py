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

# FIXME: Rework sorts to follow the same protocol so that adapters are not needed as much.

def sort_test(tested_sort, N, M, name):
    """Common logic for testing one algorithm."""
    print "testing", name, "averaging over M:", M, "...",
    sys.stdout.flush()
    time_start = time.time()
    state = random.getstate()
    comp_sum = 0.0
    comp_sqsum = 0.0
    longest = 0
    for iteration in range(M):
        counter = SimpleCounter()
        source = List([ComparisonCountingWrapper(index, counter) for index in range(N)])
        random.shuffle(source)
        result = List([item.value for item in tested_sort(source)])
        assert result == List(range(N)), str(result)
        if counter.count > longest:
            longest = counter.count
        comp_sum += counter.count
        comp_sqsum += counter.count * counter.count
    random.setstate(state)
    time_stop = time.time()
    print ":", "longest:", longest, "avg:", comp_sum / M, "sigma:", math.sqrt((M * comp_sqsum - comp_sum * comp_sum) / (M - 1)) / M, "time", time_stop - time_start

random.seed(42)

N = 1000
print "comparing at N:", N
m = 100

sort_test(fslzph_sorted, N, 2 * m, "fslzph")

sort_test(cfj_sorted, N, 40 * m, "cfj")

sort_test(hfj_sorted, N, 40 * m, "hfj")

sort_test(mlwlh_sorted, N, 1 * m, "mlwlh")

sort_test(miplzph_sorted, N, 2 * m, "miplzph")

sort_test(mslzph_sorted, N, 2 * m, "mslzph")
