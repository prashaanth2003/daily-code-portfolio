// HackerRank - A Very Big Sum
// Difficulty: Easy | Domain: Algorithms
//
// Problem: Calculate and print the sum of elements in an array,
// considering that some integers may be very large (exceeding 32-bit range).

import java.io.*;
import java.util.*;

class Result {
    
    /*
     * Complete the 'aVeryBigSum' function below.
     *
     * The function is expected to return a LONG.
     * The function accepts LONG_INTEGER_ARRAY ar as parameter.
     */
    public static long aVeryBigSum(List<Long> ar) {
        long sum = 0;
        for (long num : ar) {
            sum += num;
        }
        return sum;
    }
    
}

public class Solution {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(System.out));
        
        int n = Integer.parseInt(bufferedReader.readLine().trim());
        String[] arTemp = bufferedReader.readLine().replaceAll("\\s+$", "").split(" ");
        
        List<Long> ar = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            ar.add(Long.parseLong(arTemp[i]));
        }
        
        long result = Result.aVeryBigSum(ar);
        bufferedWriter.write(String.valueOf(result));
        bufferedWriter.newLine();
        
        bufferedReader.close();
        bufferedWriter.close();
    }
}
