"""Module that defines Ford-Johnson sorting algorithm using complete insertion."""


from complete_binary_insert import complete_binary_insert
from pluggable_ford_johnson_sort import pluggable_ford_johnson_sort_destructive
from comparable_payload import ComparablePayload


def complete_ford_johnson_sort_destructive(source):
    """Plug complete_binary_insert into pluggable_ford_johnson_sort_destructive."""
    return pluggable_ford_johnson_sort_destructive(complete_binary_insert, source)


def complete_ford_johnson_sort(source):
    """Copy iterable source to a list and apply destructive sort. Return the result."""
    return complete_ford_johnson_sort_destructive(list(source))


def complete_ford_johnson_sort_tuples(source):
    """Adapter for sorting tuples by [1] element."""
    cp_source = [ComparablePayload(item[1], item) for item in source]
    cp_result = complete_ford_johnson_sort(cp_source)
    result = [item.payload for item in cp_result]
    return result
