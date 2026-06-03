# LeetCode #3635 - Earliest Finish Time for Land and Water Rides II

**Difficulty:** Medium | **Tags:** Array, Two Pointers, Binary Search, Greedy, Sorting

## Problem
Tourist rides one land + one water ride (any order). Find earliest finish time.

## Approach
Sort by end time + binary search for O((n+m)log(n+m)). Compute both orderings.

## Complexity
Time: O((n+m)log(n+m)), Space: O(n+m)
