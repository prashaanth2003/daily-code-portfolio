#include <iostream>
#include <vector>
#include <iomanip>
#include <cassert>

class Solution {
public:
    void plusMinus(const std::vector<int>& arr) {
        int n = arr.size();
        if (n == 0) return;
        
        int positiveCount = 0;
        int negativeCount = 0;
        int zeroCount = 0;
        
        for (int num : arr) {
            if (num > 0) {
                positiveCount++;
            } else if (num < 0) {
                negativeCount++;
            } else {
                zeroCount++;
            }
        }
        
        std::cout << std::fixed << std::setprecision(6);
        std::cout << (double)positiveCount / n << "\n";
        std::cout << (double)negativeCount / n << "\n";
        std::cout << (double)zeroCount / n << "\n";
    }
};

int main() {
    Solution solver;
    std::cout << "Running Plus Minus Example (arr = [-4, 3, -9, 0, 4, 1])..." << std::endl;
    std::vector<int> arr = {-4, 3, -9, 0, 4, 1};
    solver.plusMinus(arr);
    return 0;
}
