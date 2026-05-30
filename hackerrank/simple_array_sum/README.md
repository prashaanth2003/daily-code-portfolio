# 🔢 HackerRank: Simple Array Sum

## 📝 Problem Description

Given an array of integers, find the sum of its elements.

For example, if the array $ar = [1, 2, 3]$, $1 + 2 + 3 = 6$, so return $6$.

### Input Format
- The first line contains an integer, $n$, denoting the size of the array.
- The second line contains $n$ space-separated integers representing the array's elements.

### Output Format
- Print the sum of the array's elements as a single integer.

---

## 💡 Solution

A direct, single-pass iteration or build-in `sum()` function resolves this problem in linear time.

```python
def simpleArraySum(ar):
    return sum(ar)
```

---

## 📈 Complexity Analysis

- **Time Complexity**: $\mathcal{O}(N)$ where $N$ is the number of elements in the array. We visit each element exactly once.
- **Space Complexity**: $\mathcal{O}(1)$ auxiliary space as we only keep a running accumulator (or $\mathcal{O}(N)$ to store the array in memory).
