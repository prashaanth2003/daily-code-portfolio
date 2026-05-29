def solveMeFirst(a: int, b: int) -> int:
    """
    Computes the sum of two integers.
    
    Complexity:
    - Time Complexity: O(1)
    - Space Complexity: O(1)
    """
    return a + b

if __name__ == "__main__":
    num1 = 2
    num2 = 3
    res = solveMeFirst(num1, num2)
    print(f"{num1} + {num2} = {res} (Expected: 5)")
