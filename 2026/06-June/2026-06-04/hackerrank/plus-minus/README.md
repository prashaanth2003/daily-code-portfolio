# 📊 HackerRank: Plus Minus

## 📝 Problem Description
Given an array of integers, calculate the ratios of its elements that are positive, negative, and zero. Print the decimal value of each fraction on a new line with 6 places after the decimal.

### Input Format
- The first line contains an integer `n`, the size of the array.
- The second line contains `n` space-separated integers describing the array.

### Constraints
- `0 < n <= 100`
- `-100 <= arr[i] <= 100`

---

## 💡 Intuition & Approach
This is a standard array categorization and floating-point precision problem. We need to iterate through the array once, count the number of positive, negative, and zero elements, and then divide each count by the total size of the array `n`.

### Formatting Precision
To print exactly 6 decimal places, we use standard C++ output manipulators from the `<iomanip>` library:
- `std::fixed`: formats floating-point values using fixed-point notation.
- `std::setprecision(6)`: sets the decimal precision to 6 places.

---

## ⚡ Complexity Analysis
- **Time Complexity:** $\mathcal{O}(n)$, where $n$ is the size of the array. We make a single linear pass over the elements.
- **Space Complexity:** $\mathcal{O}(1)$, as we only use three integer counters and no additional auxiliary storage.
