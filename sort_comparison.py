import math
import random

from comparison_counting_wrapper import ComparisonCountingWrapper as Wrap
from comparison_counting_wrapper import SimpleCounter as Counter
from mutable_stable_lazy_zigzag_pairing_heap import mslzph_sort
from mutable_inclusion_preferring_lazy_zigzag_pairing_heap import miplzph_sort
from mutable_lazy_weight_linking_heap import mlwlh_sort

M = 1000
print "averaging over M:", M
N = 1000
print "comparing at N:", N
sorts = [mslzph_sort, miplzph_sort, mlwlh_sort]
comp_sum = {sort: 0.0 for sort in sorts}
comp_sqsum = {sort: 0.0 for sort in sorts}
for iteration in range(M):
    for sort in sorts:
        # TODO: Do a copy.deepcopy so that sorts use the same sources.
        counter = Counter()
        source = []
        for index in range(N):
            source.append((index, Wrap(index, counter)))
        random.shuffle(source)
        result = sort(source)
        for index in range(N):
            assert result[index][0] == index
        comp_sum[sort] += counter.count
        comp_sqsum[sort] += counter.count * counter.count
summ = comp_sum[mslzph_sort]
sqsumm = comp_sqsum[mslzph_sort]
print "mslzph:", summ / M, ", sigma:", math.sqrt((M * sqsumm - summ * summ) / (M - 1)) / M
summ = comp_sum[miplzph_sort]
sqsumm = comp_sqsum[miplzph_sort]
print "miplzph:", summ / M, ", sigma:", math.sqrt((M * sqsumm - summ * summ) / (M - 1)) / M
summ = comp_sum[mlwlh_sort]
sqsumm = comp_sqsum[mlwlh_sort]
print "mlwlh:", summ / M, ", sigma:", math.sqrt((M * sqsumm - summ * summ) / (M - 1)) / M
