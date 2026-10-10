# Merge Sort Tree

A Python library that preprocesses an immutable sequence of integers into a segment tree of sorted segments, enabling efficient range counting queries such as "how many elements in `arr[l:r+1]` are ≤ x?".

```python
from merge_sort_tree import MergeSortTree

data = [5, 2, 8, 1, 9, 3]
tree = MergeSortTree(data)

print(tree.count_less_equal(1, 4, 5))  # 2 (elements 2 and 1)
print(tree.count_between(0, 5, 2, 8))  # 4 (5,2,8,3)
```

## Why this library exists

Range counting queries on static arrays are common in competitive programming, offline data analysis, and any scenario where you need repeated order-statistic lookups over subarrays. A naive scan of the subarray is O(n) per query, which becomes slow for many queries. A Merge Sort Tree stores the sorted order of each segment during a one-time O(n log n) preprocessing step, allowing each query to run in O(log² n) using binary search on the sorted lists. This is a straightforward, dependency-free way to get fast range counting without a complex dynamic structure.

The trade-off is memory: the tree uses O(n log n) space because each element appears in the sorted list of every ancestor segment. For large arrays this can be significant, but it is a reasonable cost for the query speedup.

## Edge cases

The array must be non-empty and contain only integers. The tree is static; after construction there is no way to add or remove elements. Query indices are inclusive and zero-based, and `left` must be less than or equal to `right`.

For strict inequalities, `count_less` uses `value - 1`. This is safe for all integer values except the most negative possible integer. That case is handled by returning 0, since no integer can be strictly less than the minimum integer.

## API

The library exports a single class:

- `MergeSortTree(data)` — builds the tree from a sequence of integers.
- `count_less_equal(left, right, value)` — returns the number of elements in `data[left:right+1]` that are ≤ `value`.
- `count_less(left, right, value)` — returns the number of elements < `value`.
- `count_greater(left, right, value)` — returns the number of elements > `value`.
- `count_between(left, right, low, high)` — returns the number of elements in `[low, high]`.
- `len(tree)` — returns the length of the original sequence.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

