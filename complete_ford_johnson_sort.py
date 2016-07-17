"""Module that defines Ford-Johnson sorting algorithm using complete insertion."""


from complete_binary_insert import mutating_complete_binary_insert
from pluggable_ford_johnson_sort import pluggable_ford_johnson_sort
from stabilize_sorted import stabilize_sorted


@stabilize_sorted
def cfj_sorted(source):
    """Plug complete_binary_insert into pluggable_ford_johnson_sort_destructive."""
    return pluggable_ford_johnson_sort(mutating_complete_binary_insert, source)
