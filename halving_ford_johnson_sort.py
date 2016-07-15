"""Module that defines Ford-Johnson sorting algorithm using halving insertion."""


from halving_binary_insert import halving_binary_insert
from pluggable_ford_johnson_sort import pluggable_ford_johnson_sort_destructive
from comparable_payload import ComparablePayload


def halving_ford_johnson_sort_destructive(source):
    """Plug halving_binary_insert into pluggable_ford_johnson_sort_destructive."""
    return pluggable_ford_johnson_sort_destructive(halving_binary_insert, source)


def halving_ford_johnson_sort(source):
    """Copy iterable source to a list and apply destructive sort. Return the result."""
    return halving_ford_johnson_sort_destructive(list(source))


def halving_ford_johnson_sort_tuples(source):
    """Adapter for sorting tuples by [1] element."""
    cp_source = [ComparablePayload(item[1], item) for item in source]
    cp_result = halving_ford_johnson_sort(cp_source)
    result = [item.payload for item in cp_result]
    return result
