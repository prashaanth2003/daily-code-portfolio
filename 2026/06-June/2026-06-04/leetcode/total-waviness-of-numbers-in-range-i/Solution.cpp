#include <iostream>
#include <string>
#include <vector>
#include <cassert>

class Solution {
public:
    // Computes the waviness of a given number n
    int computeWaviness(int n) {
        std::string s = std::to_string(n);
        int len = s.length();
        if (len < 3) return 0;
        
        int waviness = 0;
        for (int i = 1; i < len - 1; ++i) {
            if (s[i] > s[i-1] && s[i] > s[i+1]) {
                waviness++; // Peak
            } else if (s[i] < s[i-1] && s[i] < s[i+1]) {
                waviness++; // Valley
            }
        }
        return waviness;
    }

    // Sums the waviness for all numbers in the inclusive range [num1, num2]
    int sumWaviness(int num1, int num2) {
        int total = 0;
        for (int i = num1; i <= num2; ++i) {
            total += computeWaviness(i);
        }
        return total;
    }
};

int main() {
    Solution solver;
    
    // Example 1: num1 = 120, num2 = 130
    // Expected output: 3
    std::cout << "Running Example 1 (num1 = 120, num2 = 130)..." << std::endl;
    int res1 = solver.sumWaviness(120, 130);
    std::cout << "Result: " << res1 << " (Expected: 3)" << std::endl;
    assert(res1 == 3);
    
    // Example 2: num1 = 198, num2 = 202
    // Expected output: 3
    std::cout << "Running Example 2 (num1 = 198, num2 = 202)..." << std::endl;
    int res2 = solver.sumWaviness(198, 202);
    std::cout << "Result: " << res2 << " (Expected: 3)" << std::endl;
    assert(res2 == 3);
    
    // Example 3: num1 = 4848, num2 = 4848
    // Expected output: 2
    std::cout << "Running Example 3 (num1 = 4848, num2 = 4848)..." << std::endl;
    int res3 = solver.sumWaviness(4848, 4848);
    std::cout << "Result: " << res3 << " (Expected: 2)" << std::endl;
    assert(res3 == 2);
    
    std::cout << "🎉 All local tests passed!" << std::endl;
    return 0;
}
