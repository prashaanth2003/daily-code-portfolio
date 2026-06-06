"""
LeetCode #3753 - Total Waviness of Numbers in Range II
Difficulty: Hard

Problem:
Given two integers num1 and num2 representing an inclusive range [num1, num2],
return the total sum of waviness for all numbers in the range.

The waviness of a number is defined as the total count of its peaks and valleys:
- A digit is a peak if it is strictly greater than both of its immediate neighbors.
- A digit is a valley if it is strictly less than both of its immediate neighbors.
- The first and last digits cannot be peaks or valleys.
- Any number with fewer than 3 digits has a waviness of 0.

Constraints: 1 <= num1 <= num2 <= 10^15

Approach: Digit DP
Since the range can be as large as 10^15, iterating through each number is infeasible.
We use Digit DP to count the total waviness efficiently.

State:
- pos: current digit position (0-indexed from most significant)
- prev: the digit at the previous position (10 = sentinel for "no digit yet")
- prev_prev: the digit at two positions before (10 = sentinel)
- started: whether we've placed a non-zero digit yet (to handle leading zeros)
- tight: whether the prefix matches the upper bound

We return (count, total_waviness) from each state, where:
- count: how many valid numbers can be formed from this state
- total_waviness: the sum of waviness contributions from this state onward

When placing digit d at position pos:
- If prev_prev and prev are both valid digits (not sentinel), check if prev
  is a peak (prev_prev < prev > d) or valley (prev_prev > prev < d).
- The contribution is added to total_waviness.
"""

from functools import lru_cache


def total_waviness(num1: int, num2: int) -> int:
    """Return the total sum of waviness for all numbers in [num1, num2]."""
    def solve_upto(n: int) -> int:
        """Return total waviness for all numbers in [0, n]."""
        if n <= 0:
            return 0
        digits = list(map(int, str(n)))
        length = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos: int, prev: int, prev_prev: int, started: bool, tight: bool):
            """
            Returns (count, total_waviness) from this state.
            prev and prev_prev are 10 when no digit has been placed yet.
            """
            if pos == length:
                # A valid number has been formed
                return (1, 0)

            limit = digits[pos] if tight else 9
            total_count = 0
            total_wav = 0

            for d in range(0, limit + 1):
                next_tight = tight and (d == limit)
                next_started = started or (d != 0)

                if not next_started:
                    # Still leading zeros
                    cnt, wav = dp(pos + 1, 10, 10, False, next_tight)
                    total_count += cnt
                    total_wav += wav
                else:
                    # We have a digit placed
                    add_wav = 0
                    # Check if prev (which is now the digit at pos-1) is a peak or valley
                    if prev_prev != 10 and prev != 10:
                        if prev_prev < prev > d:
                            add_wav = 1  # prev is a peak
                        elif prev_prev > prev < d:
                            add_wav = 1  # prev is a valley

                    cnt, wav = dp(pos + 1, d, prev, True, next_tight)
                    total_count += cnt
                    total_wav += wav + add_wav * cnt

            return (total_count, total_wav)

        _, total = dp(0, 10, 10, False, True)
        return total

    return solve_upto(num2) - solve_upto(num1 - 1)


if __name__ == "__main__":
    # Test with given examples
    print("Example 1: num1=120, num2=130")
    result = total_waviness(120, 130)
    print(f"  Output: {result} (expected: 3)")
    assert result == 3, f"Expected 3, got {result}"

    print("Example 2: num1=198, num2=202")
    result = total_waviness(198, 202)
    print(f"  Output: {result} (expected: 3)")
    assert result == 3, f"Expected 3, got {result}"

    print("Example 3: num1=4848, num2=4848")
    result = total_waviness(4848, 4848)
    print(f"  Output: {result} (expected: 2)")
    assert result == 2, f"Expected 2, got {result}"

    # Additional test cases
    print("\nAdditional tests:")
    print(f"  num1=1, num2=9 -> {total_waviness(1, 9)} (expected: 0, all single digit)")
    print(f"  num1=10, num2=99 -> {total_waviness(10, 99)} (expected: 0, all 2-digit)")
    print(f"  num1=100, num2=100 -> {total_waviness(100, 100)} (expected: 0, 100 has 3 digits but no peak/valley)")

    # Performance test with large range
    print(f"\n  num1=1, num2=10^6 -> {total_waviness(1, 1000000)} (computed quickly via DP)")
    print("\nAll tests passed!")
