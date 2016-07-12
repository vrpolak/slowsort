"""Module that defines Ford-Johnson sortin algorithm."""

# FIXME: Finish writing implementation.

class ComparablePayload(object):
    """Pair of key and payload, comparable by key. Can be used to store sorted pairs."""

    def __init__(self, key, payload):
        self.key = key
        self.payload = payload

    def __cmp__(self, other):
        return self.key.__cmp__(other.key)


def binary_insert(element, target, lower_index, upper_index):
    """Insert element into target list.
    Lower index is confirmed to be before, can be -1;
    Upper index is confirmed to be after, can be len(target)."""
    window_size = upper_index - lower_index
    assert window_size > 0, "Binary insert encountered non-positive window size."
    if window_size <= 1:
        if lower_index < 0:
            result = [element]
            result.extend(target)
            return result
        result = target[:lower_index + 1]
        result.append(element)
        if upper_index < len(target):
            result.extend(target[upper_index:])
        return result
    critical_index = lower_index + window_size / 2
    if element < target[critical_index]:
        return binary_insert(element, target, lower_index, critical_index)
    else:
        return binary_insert(element, target, critical_index, upper_index)


def ford_johnson_sort(source):
    """Form pairs and sort them according to top elements (odd element at the end).
    Binary-insert dangling elements in an order that maximizes efficiency.

    Source should support len(), pop(), and element should support comparison."""
    if len(source) < 2:
        return source
    pairs = []
    while len(source) > 1:
        former = source.pop()
        latter = source.pop()
        if former <= later:
            pairs.append(ComparablePayload(former, latter))
        else:
            pairs.append(ComparablePayload(latter, former))
    ford_johnson_sort(pairs)
    insertion_target = [pairs[0].key(), pairs[0].payload]
    for pair in pairs[1:]:
        insertion_target.append(pair[0])
    jacobsthal_previous = 1
    jacobsthal_current = 1
    while 1:
        jacobsthal_old = jacobsthal_previous
        jacobsthal_previous = jacobsthal_current
        jacobsthal_current = jacobsthal_previous + 2 * jacobsthal_old
