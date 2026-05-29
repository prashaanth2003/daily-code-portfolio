# LeetCode 3300: Minimum Element After Replacement With Digit Sum

- **Difficulty**: Easy
- **URL**: [LeetCode Problem 3300](https://leetcode.com/problems/minimum-element-after-replacement-with-digit-sum/)
- **Topic Tags**: Array, Math

## Problem Statement

You are given an integer array `nums`.

You replace each element in `nums` with the **sum** of its digits.

Return the **minimum** element in `nums` after all replacements.

### Example 1
```
Input: nums = [10,12,13,14]
Output: 1
Explanation: nums becomes [1, 3, 4, 5] after all replacements, with minimum element 1.
```

### Example 2
```
Input: nums = [1,2,3,4]
Output: 1
Explanation: nums becomes [1, 2, 3, 4] after all replacements, with minimum element 1.
```

### Example 3
```
Input: nums = [999,19,199]
Output: 10
Explanation: nums becomes [27, 10, 19] after all replacements, with minimum element 10.
```

## Solution Approach

1. We iterate over each integer in the `nums` array.
2. For each number, we convert it to a string to sum its individual digits (or we can use standard modulo and integer division arithmetic).
3. We replace the number with its digit sum.
4. Finally, we return the minimum value from the transformed array of digit sums.

## Complexity Analysis
- **Time Complexity**: $O(N \times K)$ where $N$ is the number of elements in the array and $K$ is the maximum number of digits of any number (which is $\le 5$ for the problem constraints).
- **Space Complexity**: $O(1)$ auxiliary space as we do not use any extra space that scales with the input size.
