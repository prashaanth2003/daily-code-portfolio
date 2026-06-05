"""
HackerRank - Staircase
Difficulty: Easy

Problem:
Write a function that prints a staircase of size n using '#' symbols and spaces.
The staircase is right-aligned, composed of '#' characters and spaces.

Example (n=4):
   #
  ##
 ###
####

The last line has no leading spaces.

Approach:
For each row i (0-indexed), print (n-1-i) spaces followed by (i+1) '#' characters.
"""


def staircase(n: int) -> None:
    """
    Print a staircase of size n.

    Args:
        n: The height of the staircase (1 <= n <= 100)
    """
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        hashes = "#" * i
        print(spaces + hashes)


# Unit tests
def test_staircase():
    """Test the staircase function's output."""
    import io
    import sys

    for n in [1, 2, 3, 4, 5, 10]:
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        staircase(n)
        sys.stdout = old_stdout

        # Use rstrip to only strip trailing newlines, NOT leading spaces
        lines = captured.getvalue().rstrip("\n").split("\n")
        assert len(lines) == n, f"Expected {n} lines, got {len(lines)}"

        for i, line in enumerate(lines):
            expected = " " * (n - i - 1) + "#" * (i + 1)
            assert line == expected, f"Line {i}: expected '{expected}', got '{line}'"

        print(f"  n={n}: ✓ ({n} lines, correct format)")


if __name__ == "__main__":
    # Test cases
    print("Staircase of size 4:")
    staircase(4)
    print()

    print("Staircase of size 6:")
    staircase(6)
    print()

    print("Staircase of size 1:")
    staircase(1)
    print()

    print("Running unit tests:")
    test_staircase()
    print("\nAll tests passed!")