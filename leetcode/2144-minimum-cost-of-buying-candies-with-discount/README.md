# 🍬 Minimum Cost of Buying Candies With Discount

**LeetCode 2144 | Easy | Array, Greedy, Sorting**

## Problem

A shop offers a "buy 2, get 1 free" discount on candies. For every two candies you buy, you can take a third candy for free — but the free candy must cost **less than or equal to** the minimum cost of the two purchased candies.

Given an integer array `cost`, return the **minimum total cost** to buy all candies.

## Intuition

To minimize the total cost, we want the **most expensive candies** to be the ones we get free. By sorting in descending order and grouping every 3 candies, the third (cheapest) in each group is always eligible to be free.

## Algorithm

1. Sort `cost` in **descending** order.
2. Iterate through the sorted list.
3. For every third element (index 2, 5, 8, ...), **skip** it (it's free).
4. Sum the remaining elements.

## Complexity

| Metric | Value |
|--------|-------|
| Time   | O(n log n) — sorting dominates |
| Space  | O(1) — sorting in place |

## Example

```
Input:  cost = [1, 2, 3]
Sorted: [3, 2, 1]
Buy:    3 + 2 = 5
Free:   1
Output: 5
```

## Code Snippet

```python
def minimum_cost(cost: List[int]) -> int:
    cost.sort(reverse=True)
    total = 0
    for i in range(len(cost)):
        if i % 3 != 2:  # every 3rd item is free
            total += cost[i]
    return total
```

## Run

```bash
python solution.py
```
