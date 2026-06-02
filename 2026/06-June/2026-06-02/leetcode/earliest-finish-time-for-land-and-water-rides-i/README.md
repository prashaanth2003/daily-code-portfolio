# 🎢 Earliest Finish Time for Land and Water Rides I

**LeetCode 3633** | **Difficulty:** Easy | **Topics:** Array, Two Pointers, Binary Search, Greedy, Sorting

---

## Problem Statement

You are given two categories of theme park attractions: **land rides** and **water rides**.

- **Land rides**: `landStartTime[i]` (earliest boarding time) and `landDuration[i]` (ride length)
- **Water rides**: `waterStartTime[j]` (earliest boarding time) and `waterDuration[j]` (ride length)

A tourist must experience **exactly one** ride from **each** category, in **either order**:
1. A ride may be started at its opening time or any later moment.
2. If a ride starts at time `t`, it finishes at `t + duration`.
3. After finishing one ride, the tourist may board the other immediately (if open) or wait.

Return the **earliest possible time** at which the tourist can finish both rides.

---

## Solution Approach

Since the constraints are small (`n, m ≤ 100`), we use a straightforward **brute-force** approach:

1. **Try all pairs** — For each land ride `i` and water ride `j`, evaluate both orders:
   - **Land → Water**: Finish land, then start water (max of finish time and water's open time)
   - **Water → Land**: Finish water, then start land (max of finish time and land's open time)
2. **Track the minimum** finish time across all combinations.

### Complexity Analysis

| Metric | Value |
|--------|-------|
| **Time Complexity** | **O(n × m)** — We iterate over all land-water pairs (at most 10,000 pairs) |
| **Space Complexity** | **O(1)** — Only a few integer variables |

---

## Code Snippet

```java
// Try land i first, then water j
int finishLand = landStartTime[i] + landDuration[i];
int startWater = Math.max(finishLand, waterStartTime[j]);
int finishWater = startWater + waterDuration[j];
best = Math.min(best, finishWater);
```

## Test Results

```
Example 1: 9 (expected 9) PASS
Example 2: 14 (expected 14) PASS
Edge case: 7 (expected 7) PASS
```

---

*Solved on June 2, 2026*
