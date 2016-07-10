import math
import random

from comparison_counting_wrapper import ComparisonCountingWrapper as Wrap
from comparison_counting_wrapper import SimpleCounter as Counter
from mutable_stable_lazy_zigzag_pairing_heap import mslzph_sort

M = 10000
print "averaging over M:", M
N = 21
print "comparing at N:", N
comp_sum = 0.0
comp_sqsum = 0.0
for iteration in range(M):
    counter = Counter()
    source = []
    for index in range(N):
        source.append((index, Wrap(index, counter)))
    random.shuffle(source)
    result = mslzph_sort(source)
    for index in range(N):
        assert result[index][0] == index
    comp_sum += counter.count
    comp_sqsum += counter.count * counter.count
print "mslzph:", comp_sum / M, ", sigma:", math.sqrt((M * comp_sqsum - comp_sum * comp_sum) / (M - 1)) / M
