"""
HackerRank - Compare the Triplets
Difficulty: Easy
Domain: Algorithms

Problem:
Alice and Bob each created a problem for HackerRank. A reviewer rates the two challenges,
awarding points on a scale from 1 to 100 for three categories: problem clarity, originality, and difficulty.

Given a[0..2] and b[0..2], compare:
- If a[i] > b[i], Alice gets 1 point.
- If a[i] < b[i], Bob gets 1 point.
- If a[i] == b[i], neither gets a point.

Return [alice_score, bob_score].
"""

from typing import List


def compare_triplets(a: List[int], b: List[int]) -> List[int]:
    """
    Compares two triplets and returns the scores for Alice and Bob.

    Time Complexity: O(1) — always 3 comparisons.
    Space Complexity: O(1).
    """
    alice = bob = 0
    for i in range(3):
        if a[i] > b[i]:
            alice += 1
        elif a[i] < b[i]:
            bob += 1
    return [alice, bob]


# ---------- Unit Tests ----------
import unittest


class TestCompareTriplets(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(compare_triplets([5, 6, 7], [3, 6, 10]), [1, 1])

    def test_example_2(self):
        self.assertEqual(compare_triplets([17, 28, 30], [99, 16, 8]), [2, 1])

    def test_all_equal(self):
        self.assertEqual(compare_triplets([5, 5, 5], [5, 5, 5]), [0, 0])

    def test_alice_wins_all(self):
        self.assertEqual(compare_triplets([10, 10, 10], [1, 2, 3]), [3, 0])

    def test_bob_wins_all(self):
        self.assertEqual(compare_triplets([1, 2, 3], [10, 10, 10]), [0, 3])

    def test_edge_zeros(self):
        self.assertEqual(compare_triplets([0, 0, 0], [0, 0, 0]), [0, 0])


if __name__ == "__main__":
    unittest.main()
