#!/usr/bin/env python3
import sys

def simpleArraySum(ar):
    """
    Computes and returns the sum of an array of integers.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    return sum(ar)

if __name__ == '__main__':
    # Read all inputs from standard input
    input_data = sys.stdin.read().split()
    if input_data:
        n = int(input_data[0])
        ar = [int(x) for x in input_data[1:n+1]]
        result = simpleArraySum(ar)
        print(result)
