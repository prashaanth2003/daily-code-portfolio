"""
LeetCode 2144 - Minimum Cost of Buying Candies With Discount
Difficulty: Easy
Tags: Array, Greedy, Sorting

Problem:
A shop is selling candies at a discount. For every two candies sold, the shop gives a third candy for free.
The customer can choose any candy to take away for free as long as the cost of the chosen candy is
less than or equal to the minimum cost of the two candies bought.

Given a 0-indexed integer array cost, where cost[i] denotes the cost of the ith candy,
return the minimum cost of buying all the candies.

Strategy:
- Sort the costs in descending order.
- Group into sets of 3: buy the first two (most expensive), get the third (cheapest) free.
- Sum the cost of the first two in each group.
"""

from typing import List


def minimum_cost(cost: List[int]) -> int:
    """
    Returns the minimum cost to buy all candies given the "buy 2, get 1 free" discount rule.

    Time Complexity: O(n log n) due to sorting.
    Space Complexity: O(1) if sorting in-place, O(n) otherwise.
    """
    cost.sort(reverse=True)
    total = 0
    for i in range(len(cost)):
        # Every third item (index 2, 5, 8, ...) is free
        if i % 3 != 2:
            total += cost[i]
    return total


# ---------- Unit Tests ----------
import unittest


class TestMinimumCost(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(minimum_cost([1, 2, 3]), 5)

    def test_example_2(self):
        self.assertEqual(minimum_cost([6, 5, 7, 9, 2, 2]), 23)

    def test_example_3(self):
        self.assertEqual(minimum_cost([5, 5]), 10)

    def test_single_candy(self):
        self.assertEqual(minimum_cost([10]), 10)

    def test_two_candies(self):
        self.assertEqual(minimum_cost([10, 20]), 30)

    def test_three_candies(self):
        self.assertEqual(minimum_cost([10, 20, 30]), 50)

    def test_all_equal(self):
        self.assertEqual(minimum_cost([5, 5, 5, 5, 5, 5]), 20)

    def test_large_input(self):
        self.assertEqual(minimum_cost([1, 2, 3, 4, 5, 6, 7, 8, 9]), 33)


if __name__ == "__main__":
    unittest.main()
