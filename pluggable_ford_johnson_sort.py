"""Module that defines Ford-Johnson sorting algorithm with pluggable details."""


from pep_3140 import list_str
from comparable_payload import ComparablePayload


def pluggable_ford_johnson_sort_destructive(binary_insert, source):
    """Form pairs and sort them according to top elements (odd element at the end).
    Binary-insert dangling elements in an order that maximizes efficiency.

    Source should support len(), pop(), and element should support comparison."""
    if len(source) < 2:
        return source
    pairs = []
    while len(source) > 1:
        former = source.pop()
        latter = source.pop()
        if former > latter:
            pairs.append(ComparablePayload(former, latter))
        else:
            pairs.append(ComparablePayload(latter, former))
    pairs = pluggable_ford_johnson_sort_destructive(binary_insert, pairs)
    len_pairs = len(pairs)
    # Additional index value is needed for localizing anchors.
    first_item = ComparablePayload(pairs[0].payload, 0)
    second_item = ComparablePayload(pairs[0].key, 0)
    insertion_target = [first_item, second_item]
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
            insertion_target.append(ComparablePayload(pairs[index].key, index))
        if jacobsthal_backup > len_pairs:
            # We have a leeway, we can discount the cost of inserting the odd element.
            if len(source):
                odd = ComparablePayload(source.pop(), 0)
                insertion_target = binary_insert(odd, insertion_target, -1, len(insertion_target))
        upper_index = len(insertion_target) - 1
        for index in range(len_pairs)[jacobsthal_current - 1:jacobsthal_previous - 1:-1]:
            while insertion_target[upper_index].payload != index:
                upper_index -= 1
                assert upper_index >= 0, ("jacobsthal_current: " + str(jacobsthal_current) + '\n' +
                                          "jacobsthal_previous: " + str(jacobsthal_previous) + '\n' +
                                          "jacobsthal_backup: " + str(jacobsthal_backup) + '\n' +
                                          "len_pairs: " + str(len_pairs) + '\n' + "index: " + str(index) + '\n' +
                                          "len_insertion_target: " + str(len(insertion_target)) + '\n' +
                                          "insertion_target: " + list_str([list_str([item.payload, item.key]) for item in insertion_target]) + '\n' +
                                          "pairs: " + list_str([list_str([index, pair.key]) for (index, pair) in enumerate(pairs)])
                                         )
            item = ComparablePayload(pairs[index].payload, 0)
            insertion_target = binary_insert(item, insertion_target, -1, upper_index)
    # Index value is no longer needed.
    for index in range(len(insertion_target)):
        insertion_target[index] = insertion_target[index].key
    if len(source):
        odd = source.pop()
        insertion_target = binary_insert(odd, insertion_target, -1, len(insertion_target))
    # print "sorted", [str(item) for item in insertion_target]  # PEP 3140
    return insertion_target
