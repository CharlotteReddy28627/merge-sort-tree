"""Tests for MergeSortTree."""

import unittest

from merge_sort_tree import MergeSortTree


class TestMergeSortTree(unittest.TestCase):
    def test_construction_and_length(self):
        data = [5, 2, 8, 1, 9, 3]
        tree = MergeSortTree(data)
        self.assertEqual(len(tree), 6)

    def test_count_less_equal_full_range(self):
        data = [5, 2, 8, 1, 9, 3]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_less_equal(0, 5, 3), 3)  # 2,1,3
        self.assertEqual(tree.count_less_equal(0, 5, 1), 1)
        self.assertEqual(tree.count_less_equal(0, 5, 0), 0)
        self.assertEqual(tree.count_less_equal(0, 5, 9), 6)

    def test_count_less_equal_subrange(self):
        data = [5, 2, 8, 1, 9, 3]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_less_equal(1, 4, 5), 2)  # 2,1
        self.assertEqual(tree.count_less_equal(2, 5, 8), 3)  # 8,1,3
        self.assertEqual(tree.count_less_equal(0, 0, 5), 1)

    def test_count_less(self):
        data = [5, 2, 8, 1, 9, 3]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_less(0, 5, 3), 2)  # 2,1
        self.assertEqual(tree.count_less(0, 5, 1), 0)
        self.assertEqual(tree.count_less(0, 5, 10), 6)
        self.assertEqual(tree.count_less(2, 4, 9), 2)  # 8,1

    def test_count_greater(self):
        data = [5, 2, 8, 1, 9, 3]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_greater(0, 5, 5), 2)  # 8,9
        self.assertEqual(tree.count_greater(0, 5, 0), 6)
        self.assertEqual(tree.count_greater(0, 5, 9), 0)
        self.assertEqual(tree.count_greater(1, 4, 2), 2)  # 8,9

    def test_count_between(self):
        data = [5, 2, 8, 1, 9, 3]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_between(0, 5, 2, 8), 4)  # 5,2,8,3
        self.assertEqual(tree.count_between(0, 5, 6, 10), 2)  # 8,9
        self.assertEqual(tree.count_between(0, 5, 0, 0), 0)
        self.assertEqual(tree.count_between(0, 5, 1, 9), 6)

    def test_single_element(self):
        tree = MergeSortTree([42])
        self.assertEqual(tree.count_less_equal(0, 0, 42), 1)
        self.assertEqual(tree.count_less(0, 0, 42), 0)
        self.assertEqual(tree.count_greater(0, 0, 42), 0)
        self.assertEqual(tree.count_between(0, 0, 41, 43), 1)

    def test_repeated_values(self):
        data = [4, 4, 4, 4]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_less_equal(0, 3, 4), 4)
        self.assertEqual(tree.count_less(0, 3, 4), 0)
        self.assertEqual(tree.count_greater(0, 3, 4), 0)
        self.assertEqual(tree.count_between(0, 3, 4, 4), 4)

    def test_negative_values(self):
        data = [-5, 0, 3, -2, 7, -5]
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_less_equal(0, 5, 0), 4)  # -5,0,-2,-5
        self.assertEqual(tree.count_less(0, 5, 0), 3)  # -5,-2,-5
        self.assertEqual(tree.count_greater(0, 5, 0), 2)  # 3,7
        self.assertEqual(tree.count_between(0, 5, -5, 0), 4)

    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            MergeSortTree([1, 2, "3"])
        with self.assertRaises(ValueError):
            MergeSortTree([])
        with self.assertRaises(TypeError):
            MergeSortTree("not a sequence")

    def test_query_errors(self):
        tree = MergeSortTree([1, 2, 3])
        with self.assertRaises(IndexError):
            tree.count_less_equal(-1, 2, 1)
        with self.assertRaises(IndexError):
            tree.count_less_equal(0, 3, 1)
        with self.assertRaises(IndexError):
            tree.count_less_equal(2, 1, 1)
        with self.assertRaises(TypeError):
            tree.count_less_equal(0, 2, "1")
        with self.assertRaises(TypeError):
            tree.count_less(0, 2, 1.5)
        with self.assertRaises(TypeError):
            tree.count_greater(0, 2, 1.0)
        with self.assertRaises(ValueError):
            tree.count_between(0, 2, 5, 1)

    def test_large_input(self):
        data = list(range(1000))
        tree = MergeSortTree(data)
        self.assertEqual(tree.count_less_equal(0, 999, 500), 501)
        self.assertEqual(tree.count_less_equal(100, 200, 150), 51)
        self.assertEqual(tree.count_greater(0, 999, 998), 1)
        self.assertEqual(tree.count_between(0, 999, 200, 800), 601)

    def test_original_data_not_mutated(self):
        data = [3, 1, 2]
        tree = MergeSortTree(data)
        data[0] = 100
        self.assertEqual(tree.count_less_equal(0, 2, 3), 3)


if __name__ == "__main__":
    unittest.main()
