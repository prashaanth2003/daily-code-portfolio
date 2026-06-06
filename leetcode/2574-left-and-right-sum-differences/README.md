# 📊 LeetCode #2574 - Left and Right Sum Differences

**Difficulty:** Easy  
**Topics:** Array, Prefix Sum

## Problem Statement

You are given a **0-indexed** integer array `nums` of size `n`.

Define two arrays `leftSum` and `rightSum` where:
- `leftSum[i]` is the sum of elements to the left of the index `i` in the array `nums`. If there is no such element, `leftSum[i] = 0`.
- `rightSum[i]` is the sum of elements to the right of the index `i` in the array `nums`. If there is no such element, `rightSum[i] = 0`.

Return an integer array `answer` of size `n` where `answer[i] = |leftSum[i] - rightSum[i]|`.

## Examples

| Input | Output | Explanation |
|-------|--------|-------------|
| `nums = [10,4,8,3]` | `[15,1,11,22]` | `leftSum = [0,10,14,22]`, `rightSum = [15,11,3,0]`. Diff = `[|0-15|, |10-11|, |14-3|, |22-0|] = [15,1,11,22]` |
| `nums = [1]` | `[0]` | `leftSum = [0]`, `rightSum = [0]`. Diff = `[0]` |

## Solution Approach: Optimized Prefix Sum

A naive solution would compute the left sum and right sum for each element independently, resulting in an $O(n^2)$ time complexity.

Instead, we can solve this in $O(n)$ time and $O(1)$ auxiliary space using an **Optimized Prefix Sum** approach:
1. Compute the sum of all elements in `nums` and store it in `total_sum`.
2. Initialize `left_sum = 0`.
3. Iterate through `nums`. For each element `x`:
   - The elements to the right of `x` must sum to `total_sum - left_sum - x`. This is our `right_sum`.
   - Calculate the absolute difference `|left_sum - right_sum|` and append it to the answer.
   - Update `left_sum += x`.

This avoids allocating separate arrays for `leftSum` and `rightSum`, making it highly space-efficient.

### Complexity

- **Time Complexity:** $O(n)$ — We iterate through the array once to sum all elements, and once more to construct the answer.
- **Space Complexity:** $O(1)$ auxiliary space (excluding the output array).

## Running the Solution

```bash
python solution.py
```

Expected output:
```
Test Case 1: nums=[10, 4, 8, 3]
  Output:   [15, 1, 11, 22]
  Expected: [15, 1, 11, 22]
Test Case 2: nums=[1]
  Output:   [0]
  Expected: [0]
Test Case 3: nums=[2, 3, 5]
  Output:   [8, 3, 5]
  Expected: [8, 3, 5]

All LeetCode tests passed!
```
