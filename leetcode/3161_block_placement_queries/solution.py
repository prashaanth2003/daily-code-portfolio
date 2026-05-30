import bisect

class SegmentTree:
    """
    A segment tree supporting point updates and range maximum queries (RMQ)
    to efficiently query the maximum empty interval size.
    """
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (2 * self.n)

    def update(self, pos, value):
        """
        Point Update: Sets the gap size ending at position `pos` to `value`.
        Time Complexity: O(log N)
        """
        pos += self.n
        self.tree[pos] = value
        pos //= 2
        while pos > 0:
            self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
            pos //= 2

    def query(self, left, right):
        """
        Range Query: Finds the maximum gap size in the interval [left, right).
        Time Complexity: O(log N)
        """
        res = 0
        left += self.n
        right += self.n
        while left < right:
            if left & 1:
                res = max(res, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                res = max(res, self.tree[right])
            left //= 2
            right //= 2
        return res

class Solution:
    def getResults(self, queries: list[list[int]]) -> list[bool]:
        """
        Processes queries of type 1 (add obstacle at x) and type 2 (query if a block of size sz can fit in [0, x]).
        Time Complexity: O(Q * log M) where M <= min(50000, 3 * Q)
        Space Complexity: O(M)
        """
        # Find maximum coordinate to bound the Segment Tree
        max_x = 0
        for q in queries:
            max_x = max(max_x, q[1])
            
        M = max_x + 1
        
        # Sorted list of obstacles with sentinels at 0 and M
        obstacles = [0, M]
        
        # Initialize segment tree
        seg = SegmentTree(M + 1)
        
        # Initial gap between 0 and M is M, ending at M
        seg.update(M, M)
        
        results = []
        
        for q in queries:
            if q[0] == 1:
                x = q[1]
                # Find adjacent obstacles to find affected interval
                idx = bisect.bisect_left(obstacles, x)
                prev_obs = obstacles[idx - 1]
                next_obs = obstacles[idx]
                
                # Split old gap (next_obs - prev_obs) into:
                # 1. (x - prev_obs) ending at x
                # 2. (next_obs - x) ending at next_obs
                seg.update(x, x - prev_obs)
                seg.update(next_obs, next_obs - x)
                
                # Maintain the obstacles in sorted order
                bisect.insort_left(obstacles, x)
                
            elif q[0] == 2:
                x = q[1]
                sz = q[2]
                
                # Find nearest obstacle to the left of x
                idx = bisect.bisect_right(obstacles, x)
                prev_obs = obstacles[idx - 1]
                
                # Case A: Maximum empty interval ending at or before prev_obs
                max_left_gap = seg.query(0, prev_obs + 1)
                
                # Case B: The partial interval between prev_obs and x
                curr_gap = x - prev_obs
                
                # Determine feasibility
                if max(max_left_gap, curr_gap) >= sz:
                    results.append(True)
                else:
                    results.append(False)
                    
        return results
