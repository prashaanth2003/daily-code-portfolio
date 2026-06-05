# 📊 LeetCode #3753 - Total Waviness of Numbers in Range II

**Difficulty:** Hard  
**Topics:** Digit DP, Dynamic Programming, Counting

## Problem Statement

Given two integers `num1` and `num2` representing an inclusive range `[num1, num2]`, return the **total sum of waviness** for all numbers in the range.

The **waviness** of a number is defined as the total count of its **peaks** and **valleys**:
- A digit is a **peak** if it is strictly greater than both of its immediate neighbors.
- A digit is a **valley** if it is strictly less than both of its immediate neighbors.
- The first and last digits of a number **cannot** be peaks or valleys.
- Any number with fewer than 3 digits has a waviness of 0.

**Constraints:** `1 <= num1 <= num2 <= 10^15`

## Examples

| Input | Output | Explanation |
|-------|--------|-------------|
| `num1=120, num2=130` | `3` | 120(peak=1) + 121(peak=1) + 130(peak=1) |
| `num1=198, num2=202` | `3` | 198(peak=1) + 201(valley=1) + 202(valley=1) |
| `num1=4848, num2=4848` | `2` | 4848(peak=1 + valley=1) |

## Solution Approach: Digit DP

Since the range can be as large as `10^15`, iterating through each number is infeasible. We use **Digit DP** to count the total waviness efficiently.

### State Definition

```
dp(pos, prev, prev_prev, started, tight) -> (count, total_waviness)
```

- **pos**: Current digit position (0-indexed from most significant)
- **prev**: The digit at the previous position (sentinel `10` = no digit yet)
- **prev_prev**: The digit two positions before (sentinel `10`)
- **started**: Whether we've placed a non-zero digit yet (handles leading zeros)
- **tight**: Whether the prefix matches the upper bound

### Transitions

For each digit `d` at position `pos`:
1. If `prev_prev` and `prev` are both valid digits, check if `prev` is a **peak** (`prev_prev < prev > d`) or **valley** (`prev_prev > prev < d`).
2. Add 1 to waviness contribution if a peak or valley is found.
3. Recurse to the next position.

### Complexity

- **Time:** O(length × 10 × 10 × 2 × 2 × 10) = O(10 × 10 × 10 × length) ≈ O(1000 × log₁₀(n)) — very fast
- **Space:** O(length × 10 × 10 × 2 × 2) for memoization

## Key Insight

The trick is that we return **(count, total_waviness)** from each state, not just a single value. When we detect a peak/valley at position `pos`, we multiply the contribution by the count of numbers that can be formed from the remaining positions.

## Running the Solution

```bash
python solution.py
```

Expected output:
```
Example 1: num1=120, num2=130
  Output: 3 (expected: 3)
Example 2: num1=198, num2=202
  Output: 3 (expected: 3)
Example 3: num1=4848, num2=4848
  Output: 2 (expected: 2)
All tests passed!
```
