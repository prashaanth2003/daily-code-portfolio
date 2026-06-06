"""
HackerRank - Mini-Max Sum
Difficulty: Easy

Problem:
Given five positive integers, find the minimum and maximum values that can be
calculated by summing exactly four of the five integers. Then print the respective
minimum and maximum values as a single line of two space-separated long integers.

Approach:
To find the minimum sum of 4 out of 5 integers, we sum all five and subtract the maximum element.
To find the maximum sum of 4 out of 5 integers, we sum all five and subtract the minimum element.
This is optimal and takes O(1) auxiliary space and O(n) time, where n = 5 (constant).
"""

def miniMaxSum(arr: list[int]) -> tuple[int, int]:
    total_sum = sum(arr)
    min_val = min(arr)
    max_val = max(arr)
    min_sum = total_sum - max_val
    max_sum = total_sum - min_val
    return min_sum, max_sum

if __name__ == '__main__':
    # Test cases
    test_cases = [
        ([1, 3, 5, 7, 9], (16, 24)),
        ([1, 2, 3, 4, 5], (10, 14)),
        ([5, 5, 5, 5, 5], (20, 20)),
        ([1000000000, 1000000000, 1000000000, 1000000000, 1000000000], (4000000000, 4000000000))
    ]
    
    print("--- RUNNING HACKERRANK TESTS ---")
    for i, (arr, expected) in enumerate(test_cases, 1):
        res = miniMaxSum(arr)
        print(f"Test Case {i}: arr={arr}")
        print(f"  Output:   {res[0]} {res[1]}")
        print(f"  Expected: {expected[0]} {expected[1]}")
        assert res == expected, f"Expected {expected}, got {res}"
        
    print("\nAll HackerRank tests passed!")
