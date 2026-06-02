# 🔢 A Very Big Sum

**HackerRank** | **Difficulty:** Easy | **Domain:** Algorithms

---

## Problem Statement

In this challenge, you need to calculate and print the sum of elements in an array, considering that some integers may be **very large** — potentially exceeding the 32-bit integer range.

### Function Description

Complete the `aVeryBigSum` function:

**Parameters:**
- `long[] ar` — an array of long integers

**Returns:**
- `long` — the sum of all array elements

### Constraints

- 1 ≤ n ≤ 10
- 0 ≤ ar[i] ≤ 10¹⁰

---

## Solution Approach

A simple **linear scan** with a 64-bit accumulator:

1. Initialize `sum = 0L`
2. Iterate through each element, adding to sum
3. Return the final sum

### Why `long`?
A 32-bit `int` maxes out at ~2.1 × 10⁹, but array values can be up to 10¹⁰ and the sum of 10 such values can reach 10¹¹ — well beyond 32-bit range. Java's `long` (64-bit) handles this comfortably.

### Complexity Analysis

| Metric | Value |
|--------|-------|
| **Time Complexity** | **O(n)** — Single pass through array |
| **Space Complexity** | **O(1)** — Constant extra space |

---

## Sample Input / Output

```
Input:
5
1000000001 1000000002 1000000003 1000000004 1000000005

Output:
5000000015
```

---

*Solved on June 2, 2026*
