"""Module that defines Ford-Johnson sorting algorithm using halving insertion."""


from halving_binary_insert import mutating_halving_binary_insert
from pluggable_ford_johnson_sort import pluggable_ford_johnson_sort
from stabilize_sorted import stabilize_sorted


@stabilize_sorted
def hfj_sorted(source):
    """Plug halving_binary_insert into pluggable_ford_johnson_sort."""
    return pluggable_ford_johnson_sort(mutating_halving_binary_insert, source)
