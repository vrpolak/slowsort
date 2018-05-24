"""Module that defines Ford-Johnson sorting algorithm with pluggable details."""

from pep_3140 import Deque
from pep_3140 import List
from comparable_payload import ComparablePayload


def pluggable_ford_johnson_sort(mutating_insert, original_source):
    """Form pairs and sort them according to top elements (odd element at the end).
    Binary-insert dangling elements in an order that maximizes efficiency.

    Original_source should be iterable supporting len() and element should support comparison.
    Returned value is either the original, or a new List.
    This sort is functional, in sense it does not modify original source.
    """
    if len(original_source) < 2:
        return original_source
    source = Deque(original_source)
    pairs = List()
    while len(source) > 1:
        former = source.popleft()
        latter = source.popleft()
        if former > latter:
            pairs.append(ComparablePayload(former, latter))
        else:
            pairs.append(ComparablePayload(latter, former))
    pairs = pluggable_ford_johnson_sort(mutating_insert, pairs)
    len_pairs = len(pairs)
    # Additional index payload is needed for localizing anchors.
    first_item = ComparablePayload(pairs[0].payload, 0)
    second_item = ComparablePayload(pairs[0].key, 0)
    indexed_target = List([first_item, second_item])
    jacobsthal_previous = 1
    jacobsthal_current = 1
    while jacobsthal_current < len_pairs:
        jacobsthal_backup = jacobsthal_previous
        jacobsthal_previous = jacobsthal_current
        jacobsthal_current = jacobsthal_previous + 2 * jacobsthal_backup
        jacobsthal_backup = jacobsthal_current
        if jacobsthal_current > len_pairs:
            jacobsthal_current = len_pairs
        for index in range(len_pairs)[jacobsthal_previous:jacobsthal_current]:
            indexed_target.append(ComparablePayload(pairs[index].key, index))
        if jacobsthal_backup > len_pairs:
            # We have a leeway, we can discount the cost of inserting the odd element.
            if len(source):
                mutating_insert(ComparablePayload(source.popleft(), 0), indexed_target, -1, len(indexed_target))
        upper_index = len(indexed_target) - 1
        for index in range(len_pairs)[jacobsthal_current - 1:jacobsthal_previous - 1:-1]:
            while indexed_target[upper_index].payload != index:
                upper_index -= 1
                assert upper_index >= 0, ("jacobsthal_current: " + str(jacobsthal_current) + '\n' +
                                          "jacobsthal_previous: " + str(jacobsthal_previous) + '\n' +
                                          "jacobsthal_backup: " + str(jacobsthal_backup) + '\n' +
                                          "len_pairs: " + str(len_pairs) + '\n' + "index: " + str(index) + '\n' +
                                          "len_indexed_target: " + str(len(indexed_target)) + '\n' +
                                          "indexed_target: " + str(List([str(List([item.payload, item.key])) for item in indexed_target])) + '\n' +
                                          "pairs: " + str(List([str(List([index, pair.key])) for (index, pair) in enumerate(pairs)]))
                                         )
            mutating_insert(ComparablePayload(pairs[index].payload, 0), indexed_target, -1, upper_index)
    bare_target = List([item.key for item in indexed_target])
    if len(source):
        mutating_insert(source.popleft(), bare_target, -1, len(bare_target))
    return bare_target
