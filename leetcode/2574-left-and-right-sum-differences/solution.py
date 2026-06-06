"""
LeetCode #2574 - Left and Right Sum Differences
Difficulty: Easy

Problem:
Given a 0-indexed integer array nums, return an array answer where
answer[i] = |leftSum[i] - rightSum[i]|, where leftSum[i] is the sum of
elements to the left of i and rightSum[i] is the sum of elements to the right of i.

Approach: Prefix Sum (Optimized)
We can compute the total sum first. Maintain a running left_sum, initialized to 0.
For each element, right_sum is calculated as (total_sum - left_sum - num).
Then the absolute difference |left_sum - right_sum| is appended to our answer.
Finally, we add the current element to left_sum.
This allows us to solve the problem in a single pass with O(n) time and O(1) auxiliary space.
"""

class Solution:
    def leftRightDifference(self, nums: list[int]) -> list[int]:
        total_sum = sum(nums)
        left_sum = 0
        answer = []
        for x in nums:
            right_sum = total_sum - left_sum - x
            answer.append(abs(left_sum - right_sum))
            left_sum += x
        return answer

if __name__ == "__main__":
    sol = Solution()
    
    # Test case 1
    nums1 = [10, 4, 8, 3]
    expected1 = [15, 1, 11, 22]
    res1 = sol.leftRightDifference(nums1)
    print(f"Test Case 1: nums={nums1}")
    print(f"  Output:   {res1}")
    print(f"  Expected: {expected1}")
    assert res1 == expected1, f"Expected {expected1}, got {res1}"
    
    # Test case 2
    nums2 = [1]
    expected2 = [0]
    res2 = sol.leftRightDifference(nums2)
    print(f"Test Case 2: nums={nums2}")
    print(f"  Output:   {res2}")
    print(f"  Expected: {expected2}")
    assert res2 == expected2, f"Expected {expected2}, got {res2}"
    
    # Test case 3
    nums3 = [2, 3, 5]
    expected3 = [8, 3, 5]
    res3 = sol.leftRightDifference(nums3)
    print(f"Test Case 3: nums={nums3}")
    print(f"  Output:   {res3}")
    print(f"  Expected: {expected3}")
    assert res3 == expected3, f"Expected {expected3}, got {res3}"
    
    print("\nAll LeetCode tests passed!")
