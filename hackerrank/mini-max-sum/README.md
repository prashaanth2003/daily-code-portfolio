# 📊 HackerRank - Mini-Max Sum

**Difficulty:** Easy  
**Topics:** Array, Sorting, Mathematics

## Problem Statement

Given five positive integers, find the minimum and maximum values that can be calculated by summing exactly four of the five integers. Then print the respective minimum and maximum values as a single line of two space-separated long integers.

## Examples

For `arr = [1, 3, 5, 7, 9]`:
- The minimum sum is calculated by summing everything except the maximum element (`9`):  
  `1 + 3 + 5 + 7 = 16`
- The maximum sum is calculated by summing everything except the minimum element (`1`):  
  `3 + 5 + 7 + 9 = 24`

The function should print:
```
16 24
```

### Constraints
- $1 \le arr[i] \le 10^9$
- The output can be greater than a 32-bit integer, so 64-bit integers should be used (standard `int` in Python handles arbitrary precision automatically).

## Solution Approach: Linear Scan ($O(1)$ Space)

A naive approach would be to sort the array first, which takes $O(n \log n)$ time. Since $n = 5$, sorting is fast, but we can do even better in $O(n)$ time and $O(1)$ auxiliary space without sorting!

1. Calculate the sum of all 5 integers in the array, let's call it `total_sum`.
2. Find the minimum element (`min_val`) and maximum element (`max_val`) in the array.
3. The minimum possible sum of 4 elements is `total_sum - max_val` (excluding the largest element).
4. The maximum possible sum of 4 elements is `total_sum - min_val` (excluding the smallest element).

This is highly optimal as it only requires a single pass over the array.

### Complexity

- **Time Complexity:** $O(n)$ where $n$ is the number of elements (which is 5). Hence, it runs in $O(1)$ constant time.
- **Space Complexity:** $O(1)$ auxiliary space.

## Running the Solution

```bash
python solution.py
```

Expected output:
```
--- RUNNING HACKERRANK TESTS ---
Test Case 1: arr=[1, 3, 5, 7, 9]
  Output:   16 24
  Expected: 16 24
Test Case 2: arr=[1, 2, 3, 4, 5]
  Output:   10 14
  Expected: 10 14
Test Case 3: arr=[5, 5, 5, 5, 5]
  Output:   20 20
  Expected: 20 20

All HackerRank tests passed!
```
