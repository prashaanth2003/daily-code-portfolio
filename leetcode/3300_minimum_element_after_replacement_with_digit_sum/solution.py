def minElement(nums: list[int]) -> int:
    """
    Replaces each element in nums with the sum of its digits and returns 
    the minimum element in nums after all replacements.
    
    Complexity:
    - Time Complexity: O(N * K) where N is the length of nums and K is the average 
      number of digits of elements in nums (K <= 5 for normal 32-bit integers).
    - Space Complexity: O(1) auxiliary space.
    """
    def digit_sum(n: int) -> int:
        return sum(int(digit) for digit in str(n))
        
    return min(digit_sum(num) for num in nums)

# Example execution
if __name__ == "__main__":
    test_nums1 = [10, 12, 13, 14]
    print(f"Input: {test_nums1} -> Output: {minElement(test_nums1)} (Expected: 1)")
    
    test_nums2 = [999, 19, 199]
    print(f"Input: {test_nums2} -> Output: {minElement(test_nums2)} (Expected: 10)")
