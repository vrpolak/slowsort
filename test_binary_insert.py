from ford_johnson_sort import binary_insert

result = binary_insert(10, [], -1, 0)
assert result == [10], repr(result)
result = binary_insert(5, [10], -1, 1)
assert result == [5, 10], repr(result)
result = binary_insert(7, [5, 10], -1, 2)
assert result == [5, 7, 10], repr(result)
result = binary_insert(2, [5, 7, 10], -1, 3)
assert result == [2, 5, 7, 10], repr(result)
result = binary_insert(13, [2, 5, 7, 10], -1, 4)
assert result == [2, 5, 7, 10, 13], repr(result)
