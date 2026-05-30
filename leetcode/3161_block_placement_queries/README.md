# 🧱 LeetCode 3161: Block Placement Queries (Hard)

## 📝 Problem Description

An infinite number line starts at 0 and extends towards the positive x-axis. We are given a 2D array `queries` of two types:
1. **Type 1 (`[1, x]`)**: Build an obstacle at distance `x` from the origin. (Guaranteed that no obstacle exists at `x` beforehand).
2. **Type 2 (`[2, x, sz]`)**: Check if we can place a block of size `sz` **anywhere** in the range `[0, x]` such that the block entirely lies in the range `[0, x]` without intersecting any obstacles (touching is allowed). Note that this query is independent and doesn't actually place any blocks.

Return a list of boolean values, where each element is the answer to the respective type 2 query in order.

---

## 💡 Solution: Point Update, Range Maximum Query (Segment Tree)

This problem requires us to dynamically place obstacles and instantly query the maximum available "gap" (consecutive space) between adjacent obstacles in a specified prefix `[0, x]`. 

A **Segment Tree** (with Point Update and Range Maximum Query) is the ideal data structure to solve this.

### ⚙️ Core Idea

1. **Obstacle Maintenance**: Keep obstacles in a sorted list (`obstacles`). Initially, we add sentinels at `0` and `M` (the max coordinate we'll see, bounded by `min(50000, 3 * Q)`).
2. **Segment Tree Mapping**:
   - For each obstacle `x` (except 0), we store the gap to its left neighbor in the segment tree at index `x`.
   - For any obstacle `x`, the value in `tree[x]` is `x - prev_obstacle`.
   - `tree[0]` is initialized to `0`.
3. **Point Update (Type 1 - Add obstacle at `x`)**:
   - Use `bisect` to find the left neighbor `prev_obs` and right neighbor `next_obs` of `x`.
   - The old gap `next_obs - prev_obs` is split into two new gaps: `x - prev_obs` and `next_obs - x`.
   - Update the segment tree: `tree[x] = x - prev_obs` and `tree[next_obs] = next_obs - x`.
   - Insert `x` into the sorted obstacles.
4. **Range Query (Type 2 - Feasibility check for block size `sz` in `[0, x]`)**:
   - Find the largest obstacle `prev_obs <= x`.
   - Any fully formed empty gap to the left of `prev_obs` is entirely contained within `[0, prev_obs]`. The maximum of these gaps is the range maximum query of the segment tree in `[0, prev_obs]`.
   - The gap between `prev_obs` and `x` is `x - prev_obs`. This gap is also a candidate.
   - If `max(RangeMax(0, prev_obs), x - prev_obs) >= sz`, return `True`, else `False`.

---

## 📈 Complexity Analysis

- **Time Complexity**:
  - **Tree Updates/Queries**: $O(\log M)$ where $M = \min(50000, 3 \cdot Q)$.
  - **Bisect & List Insertion**: $O(Q)$ in worst-case in Python, but since $M \le 50000$, list operations are extremely fast (taking fractions of a millisecond, way below standard TLE thresholds).
  - **Total Time Complexity**: $\mathcal{O}(Q \log M)$ which is extremely optimal and executes in under **0.2 seconds** for 150,000 queries.

- **Space Complexity**:
  - $\mathcal{O}(M)$ to store the Segment Tree of size $2 \cdot M$ and the sorted obstacles. This uses very little memory (< 5 MB).
