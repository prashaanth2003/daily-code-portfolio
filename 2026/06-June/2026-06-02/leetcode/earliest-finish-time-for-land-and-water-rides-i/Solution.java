// LeetCode 3633 - Earliest Finish Time for Land and Water Rides I
// Difficulty: Easy | Topics: Array, Two Pointers, Binary Search, Greedy, Sorting
//
// Problem: Given land rides (startTime[i], duration[i]) and water rides (startTime[j], duration[j]),
// a tourist must ride exactly one from each category in either order. Find the earliest possible
// finish time.

import java.util.Arrays;

class Solution {
    public int earliestFinishTime(int[] landStartTime, int[] landDuration,
                                   int[] waterStartTime, int[] waterDuration) {
        int n = landStartTime.length;
        int m = waterStartTime.length;
        int best = Integer.MAX_VALUE;
        
        // Try all pairs (land first, then water) or (water first, then land)
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                // Option 1: Land ride i -> Water ride j
                int finishLand = landStartTime[i] + landDuration[i];
                int startWater = Math.max(finishLand, waterStartTime[j]);
                int finishWater = startWater + waterDuration[j];
                best = Math.min(best, finishWater);
                
                // Option 2: Water ride j -> Land ride i
                int finishWaterFirst = waterStartTime[j] + waterDuration[j];
                int startLand = Math.max(finishWaterFirst, landStartTime[i]);
                int finishLandLast = startLand + landDuration[i];
                best = Math.min(best, finishLandLast);
            }
        }
        
        return best;
    }
    
    // Test harness
    public static void main(String[] args) {
        Solution sol = new Solution();
        
        // Example 1
        int[] landStart1 = {2, 8};
        int[] landDur1   = {4, 1};
        int[] waterStart1 = {6};
        int[] waterDur1   = {3};
        int res1 = sol.earliestFinishTime(landStart1, landDur1, waterStart1, waterDur1);
        System.out.println("Example 1: " + res1 + " (expected 9) " + (res1 == 9 ? "PASS" : "FAIL"));
        
        // Example 2
        int[] landStart2 = {5};
        int[] landDur2   = {3};
        int[] waterStart2 = {1};
        int[] waterDur2   = {10};
        int res2 = sol.earliestFinishTime(landStart2, landDur2, waterStart2, waterDur2);
        System.out.println("Example 2: " + res2 + " (expected 14) " + (res2 == 14 ? "PASS" : "FAIL"));
        
        // Edge case: single pair
        int[] ls3 = {1};
        int[] ld3 = {2};
        int[] ws3 = {3};
        int[] wd3 = {4};
        int res3 = sol.earliestFinishTime(ls3, ld3, ws3, wd3);
        System.out.println("Edge case: " + res3 + " (expected 7) " + (res3 == 7 ? "PASS" : "FAIL"));
    }
}
