"""Module that defines functions for creating sorted from heap.

Curently functions return sorted List.
Alternative would be to return function which performs sorted,
but that way is less friendly for adding debug logging."""


from stabilize_sorted import stabilize_sorted
from pep_3140 import List


def sorted_using_mutable_stable_heap(heap_class, source):
    """Put items in heap, create List py popping them."""
    heap = heap_class()
    for item in source:
        heap.add(item)
    result = List()
    while heap:
        result.append(heap.pop())
    return result


@stabilize_sorted
def sorted_using_mutable_unstable_heap(heap_class, source):
    """Stabilized unstable sorted using mutable heap class."""
    return sorted_using_mutable_stable_heap(heap_class, source)


def sorted_using_functional_unstable_heap
    """Put items in heap, create List py popping them."""
    heap = heap_class()
    for item in source:
        heap = heap.add(item)
    result = List()
    while heap:
        heap, item = heap.pop()
        result.append(item)
    return result


@stabilize_sorted
def sorted_using_functional_stable_heap
    """Stabilized unstable sorted using functional heap class."""
    return sorted_using_functional_stable_heap(heap_class, source)
