# 🔺 HackerRank - Staircase

**Difficulty:** Easy  
**Domain:** Algorithms > Warmup

## Problem Statement

Write a function that prints a staircase of size `n` using `#` symbols and spaces. The staircase is right-aligned.

**Example (n=4):**
```
   #
  ##
 ###
####
```

The last line has no leading spaces.

## Solution Approach

For each row `i` (1-indexed):
- Print `(n - i)` spaces
- Print `i` hash (`#`) characters

This is a straightforward string-building problem that tests basic loop logic.

### Complexity

- **Time:** O(n²) — each of the n rows prints up to n characters
- **Space:** O(n) — building strings for each row

## Running the Solution

```bash
python solution.py
```

Expected output:
```
Staircase of size 4:
   #
  ##
 ###
####

Staircase of size 6:
     #
    ##
   ###
  ####
 #####
######

Running unit tests:
  n=1: ✓ (1 lines, correct format)
  n=2: ✓ (2 lines, correct format)
  n=3: ✓ (3 lines, correct format)
  n=4: ✓ (4 lines, correct format)
  n=5: ✓ (5 lines, correct format)
  n=10: ✓ (10 lines, correct format)

All tests passed!
```
