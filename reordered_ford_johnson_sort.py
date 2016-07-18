"""Module that defines "reordered" Ford-Johnson sorting algorithm with complete insertion."""


from complete_binary_insert import mutating_complete_binary_insert
from pluggable_reordered_ford_johnson_sort import pluggable_reordered_ford_johnson_sort
from stabilize_sorted import stabilize_sorted


@stabilize_sorted
def rfj_sorted(source):
    """Plug complete_binary_insert into pluggable_ford_johnson_sort."""
    return pluggable_reordered_ford_johnson_sort(mutating_complete_binary_insert, source)
