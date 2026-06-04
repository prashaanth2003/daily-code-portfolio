# 🌊 LeetCode 3751: Total Waviness of Numbers in Range I

## 📝 Problem Description
You are given two integers `num1` and `num2` representing an inclusive range `[num1, num2]`.

The **waviness** of a number is defined as the total count of its **peaks** and **valleys**:
- A digit is a **peak** if it is **strictly greater** than both of its immediate neighbors.
- A digit is a **valley** if it is **strictly less** than both of its immediate neighbors.
- The first and last digits of a number **cannot** be peaks or valleys.
- Any number with fewer than 3 digits has a waviness of 0.

Return the total sum of waviness for all numbers in the range `[num1, num2]`.

### Constraints
- `1 <= num1 <= num2 <= 10^5`

---

## 💡 Intuition & Approach
Since the constraints are very small (`num2 <= 10^5`), the maximum range size is `10^5` and each number has at most `6` digits. A direct, simulation-based approach is highly optimal, straightforward, and 100% correct.

### Algorithm
1. Iterate through every integer `n` in the range `[num1, num2]`.
2. Convert `n` to its string representation `s`.
3. If the length of `s` is less than 3, its waviness is `0`.
4. Otherwise, iterate `i` from `1` to `len - 2`:
   - Check if `s[i] > s[i-1]` and `s[i] > s[i+1]` (Peak).
   - Check if `s[i] < s[i-1]` and `s[i] < s[i+1]` (Valley).
   - If either is true, increment the waviness for `n` by 1.
5. Sum the waviness of all numbers and return.

### Bonus: Scaling to Large Constraints (Digit DP)
If the constraints were `num2 <= 10^18`, simulation would time out. The optimal approach would be **Digit Dynamic Programming**.
We could define a state:
`dp(idx, prev_digit, is_increasing, is_less, is_started, waviness_count)`
where:
- `idx` is the current digit position.
- `prev_digit` is the digit at `idx-1`.
- `is_increasing` is boolean tracking if the last move was increasing or decreasing (helps identify a peak or valley transition).
- `is_less` is a tight-bound restriction flag.
- `is_started` tracks leading zeros.
- `waviness_count` tracks the accumulated peaks/valleys.

Using Digit DP, we can solve the problem in `O(log10(num2) * 10 * 2 * 2 * log10(num2))` which runs in micro-seconds even for numbers up to `10^18`.

---

## ⚡ Complexity Analysis
- **Time Complexity:** $\mathcal{O}((num2 - num1) \times \log_{10}(num2))$.
  For `num2 = 10^5`, this is at most $10^5 \times 6 = 6 \times 10^5$ operations, taking less than 15ms in C++.
- **Space Complexity:** $\mathcal{O}(\log_{10}(num2))$ auxiliary space to store the string representation of each number.
