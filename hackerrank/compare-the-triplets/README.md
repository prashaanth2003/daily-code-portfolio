# ⚖️ Compare the Triplets

**HackerRank | Algorithms | Easy**

## Problem

Alice and Bob each have a triplet representing scores for three categories. Compare the two triplets point by point and award points to whoever has the higher score in each category.

## Algorithm

1. Iterate through indices 0, 1, 2.
2. For each index:
   - If `a[i] > b[i]` → Alice gets 1 point.
   - If `a[i] < b[i]` → Bob gets 1 point.
   - Otherwise → no points.
3. Return `[alice_score, bob_score]`.

## Complexity

| Metric | Value |
|--------|-------|
| Time   | O(1) — fixed 3 iterations |
| Space  | O(1) |

## Code Snippet

```python
def compare_triplets(a: List[int], b: List[int]) -> List[int]:
    alice = bob = 0
    for i in range(3):
        if a[i] > b[i]:
            alice += 1
        elif a[i] < b[i]:
            bob += 1
    return [alice, bob]
```

## Run

```bash
python solution.py
```
