"""Module that defines a reordered version of Ford-Johnson sorting algorithm with pluggable details."""

from pep_3140 import Deque
from pep_3140 import List
from comparable_payload import ComparablePayload


def pluggable_reordered_ford_johnson_sort(mutating_insert, original_source):
    """Form pairs and sort them according to top elements (odd element at the end).
    Binary-insert dangling elements in an order that maximizes efficiency.

    The order takes into account placement of previous inserts,
    basically it can change order of inserts to differ from the Jacobsthal one.

    Original_source should be iterable supporting len() and element should support comparison.
    Returned value is either the original, or a new List.
    This sort is functional, in sense it does not modify original source.
    """
    len_original_source = len(original_source)
    if len_original_source < 2:
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
    odd_item = None if len(source) < 1 else source.pop()
    pairs = pluggable_reordered_ford_johnson_sort(mutating_insert, pairs)
    # Additional index payload is needed for localizing anchors.
    first_item = ComparablePayload(pairs[0].payload, 0)
    second_item = ComparablePayload(pairs[0].key, 0)
    indexed_target = List([first_item, second_item])
    danglers = List([None])  # to align indexes
    # pairs[].key could be re-used for danglers, byt that would be more error-prone.
    for index, pair in list(enumerate(pairs))[1:]:
        # Nonzero index means that item dangling under anchor was not inserted yet.
        indexed_target.append(ComparablePayload(pair.key, index))
        danglers.append(pair.payload)
    efficiency_list = List()
    for index in range(2, len_original_source):
        bits = len(bin(index)) - 2
        efficiency_list.append(ComparablePayload(-1.0 * (index + 1) / (1 << bits), index))
    efficiency_list = sorted(efficiency_list)
    for _ in range(len_original_source - len(indexed_target)):
        len_target = len(indexed_target)
        for efficiency_item in efficiency_list:
            anchor_index = efficiency_item.payload
            if anchor_index < len_target:
                anchor = indexed_target[anchor_index]
                dangler_index = anchor.payload
                if dangler_index > 0:
                    anchor.payload = 0
                    # print "inserting dangler at efficiency", efficiency_item.key, "at index", anchor_index, "for source size", len_original_source
                    mutating_insert(ComparablePayload(danglers[dangler_index], 0), indexed_target, -1, anchor_index)
                    break
            elif anchor_index == len_target:
                if odd_item is not None:
                    # print "inserting odd at efficiency", efficiency_item.key, "at index", anchor_index, "for source size", len_original_source
                    mutating_insert(ComparablePayload(odd_item, 0), indexed_target, -1, len_target)
                    odd_item = None
                    break
    assert len(indexed_target) == len_original_source
    return List([item.key for item in indexed_target])
