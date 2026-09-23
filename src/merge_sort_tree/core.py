"""Core implementation of the Merge Sort Tree.

The tree is built from an immutable sequence of integers. It is a static
data structure: after construction, elements cannot be added, removed, or
modified. Each node of the segment tree stores the sorted list of elements
in its segment. A range counting query returns the number of elements in a
subarray that are less than or equal to a given value.

Why a static tree?
    Merge Sort Trees are intended for workloads where the array is fixed
    and many range queries are issued. The memory overhead is O(n log n)
    and each query runs in O(log^2 n). If mutability were required, a
    Fenwick tree of sorted vectors or a balanced BST would be more
    appropriate, but would complicate the implementation and the API.
"""

from __future__ import annotations

from bisect import bisect_right
from math import inf
from typing import List, Sequence


class MergeSortTree:
    """A static segment tree that stores sorted segments.

    The tree is built from a sequence of integers. Query results are
    deterministic and depend only on the input sequence and query
    parameters.

    Attributes:
        _n: The length of the original sequence.
        _tree: The internal segment tree representation. The tree is stored
            as a list of lists. The root is at index 1. For a node at index
            `i`, its left child is at `2*i` and its right child at `2*i+1`.
            This layout avoids recursive node objects and reduces memory
            overhead. Each node contains a sorted list of the elements in
            its segment.
    """

    def __init__(self, data: Sequence[int]) -> None:
        """Build the tree from the given sequence.

        Args:
            data: A sequence of integers. The sequence is copied; later
                mutations of the original sequence do not affect the tree.

        Raises:
            TypeError: If `data` is not a sequence of integers or if an
                element is not an integer.
            ValueError: If `data` is empty.
        """
        if not isinstance(data, Sequence):
            raise TypeError("data must be a sequence of integers")
        if len(data) == 0:
            raise ValueError("data must not be empty")

        for x in data:
            if not isinstance(x, int):
                raise TypeError("all elements must be integers")

        self._n = len(data)
        # The tree array has size 4*n to safely accommodate any segment tree
        # built from an array of length n. This is a common static allocation
        # strategy: the maximum number of nodes for a segment tree over n
        # elements is 4*n.
        self._tree: List[List[int]] = [[] for _ in range(4 * self._n)]
        self._build(data, 1, 0, self._n - 1)

    def _build(self, data: Sequence[int], node: int, left: int, right: int) -> None:
        """Recursively build the tree.

        Args:
            data: The original sequence.
            node: The current node index in `_tree`.
            left: The left index of the current segment in `data`.
            right: The right index of the current segment in `data`.
        """
        if left == right:
            self._tree[node] = [data[left]]
            return

        mid = (left + right) // 2
        self._build(data, 2 * node, left, mid)
        self._build(data, 2 * node + 1, mid + 1, right)

        left_child = self._tree[2 * node]
        right_child = self._tree[2 * node + 1]

        # Merge the two sorted child lists into the current node's sorted list.
        merged: List[int] = []
        i = j = 0
        while i < len(left_child) and j < len(right_child):
            if left_child[i] <= right_child[j]:
                merged.append(left_child[i])
                i += 1
            else:
                merged.append(right_child[j])
                j += 1
        if i < len(left_child):
            merged.extend(left_child[i:])
        if j < len(right_child):
            merged.extend(right_child[j:])

        self._tree[node] = merged

    def count_less_equal(self, left: int, right: int, value: int) -> int:
        """Return the number of elements in the subarray `data[left:right+1]`
        that are less than or equal to `value`.

        Args:
            left: The inclusive start index of the query range.
            right: The inclusive end index of the query range.
            value: The threshold value for comparison.

        Returns:
            The count of elements in the range that are <= value.

        Raises:
            IndexError: If `left` or `right` are out of bounds or if
                `left > right`.
            TypeError: If `left`, `right`, or `value` are not integers.
        """
        if not all(isinstance(x, int) for x in (left, right, value)):
            raise TypeError("left, right, and value must be integers")
        if left < 0 or right >= self._n or left > right:
            raise IndexError("query indices are out of bounds")

        return self._query(1, 0, self._n - 1, left, right, value)

    def _query(
        self,
        node: int,
        seg_left: int,
        seg_right: int,
        q_left: int,
        q_right: int,
        value: int,
    ) -> int:
        """Recursively query the tree.

        Args:
            node: Current node index.
            seg_left: Left boundary of the node's segment.
            seg_right: Right boundary of the node's segment.
            q_left: Left boundary of the query range.
            q_right: Right boundary of the query range.
            value: The threshold value.

        Returns:
            The count of elements <= value in the intersection of the node's
            segment and the query range.
        """
        if q_left <= seg_left and seg_right <= q_right:
            # Complete overlap: use binary search on the sorted list.
            # bisect_right returns the insertion point to the right of any
            # existing entries equal to value, which gives the count of
            # elements <= value.
            return bisect_right(self._tree[node], value)

        if seg_right < q_left or q_right < seg_left:
            # No overlap.
            return 0

        mid = (seg_left + seg_right) // 2
        return self._query(2 * node, seg_left, mid, q_left, q_right, value) + self._query(
            2 * node + 1, mid + 1, seg_right, q_left, q_right, value
        )

    def count_less(self, left: int, right: int, value: int) -> int:
        """Return the number of elements in the subarray `data[left:right+1]`
        that are strictly less than `value`.

        This is implemented by counting elements <= value - 1. This avoids
        duplicating the traversal logic and is correct because all elements
        are integers. If `value` is `-inf`, the result is 0; `inf` is
        represented by a very large integer sentinel, but users should
        simply use `count_less_equal` for unbounded queries.

        Args:
            left: Inclusive start index.
            right: Inclusive end index.
            value: Exclusive upper bound.

        Returns:
            The count of elements < value.

        Raises:
            IndexError: If indices are out of bounds or `left > right`.
            TypeError: If arguments are not integers.
        """
        if not isinstance(value, int):
            raise TypeError("value must be an integer")
        # Using value - 1 is safe for all integer values except the minimum
        # possible integer. For that edge case, no integer can be strictly
        # less than it, so we return 0 directly.
        if value == -inf:
            return 0
        return self.count_less_equal(left, right, value - 1)

    def count_greater(self, left: int, right: int, value: int) -> int:
        """Return the number of elements in the subarray `data[left:right+1]`
        that are strictly greater than `value`.

        This is implemented by subtracting the count of elements <= value
        from the total number of elements in the query range.

        Args:
            left: Inclusive start index.
            right: Inclusive end index.
            value: Exclusive lower bound.

        Returns:
            The count of elements > value.

        Raises:
            IndexError: If indices are out of bounds or `left > right`.
            TypeError: If arguments are not integers.
        """
        if not isinstance(value, int):
            raise TypeError("value must be an integer")
        if left < 0 or right >= self._n or left > right:
            raise IndexError("query indices are out of bounds")
        total = right - left + 1
        return total - self.count_less_equal(left, right, value)

    def count_between(self, left: int, right: int, low: int, high: int) -> int:
        """Return the number of elements in the range that are >= `low` and
        <= `high`.

        Args:
            left: Inclusive start index.
            right: Inclusive end index.
            low: Inclusive lower bound.
            high: Inclusive upper bound.

        Returns:
            The count of elements in [low, high].

        Raises:
            IndexError: If indices are out of bounds or `left > right`.
            TypeError: If arguments are not integers.
            ValueError: If `low > high`.
        """
        if not all(isinstance(x, int) for x in (left, right, low, high)):
            raise TypeError("all arguments must be integers")
        if low > high:
            raise ValueError("low must be <= high")
        return self.count_less_equal(left, right, high) - self.count_less(left, right, low)

    def __len__(self) -> int:
        """Return the length of the original sequence."""
        return self._n
