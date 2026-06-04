#include "MemoryTracker.hpp"
#include "MemoryPool.hpp"
#include "PoolAllocator.hpp"
#include <iostream>
#include <list>
#include <chrono>

void runBenchmark() {
    std::cout << "\n============================================\n";
    std::cout << "⚡  PERFORMANCE BENCHMARK RUNNER  ⚡\n";
    std::cout << "============================================\n";
    
    const int numOperations = 50000;
    std::cout << "Performing " << numOperations << " insertions and deletions..." << std::endl;
    
    // Benchmark 1: Standard Allocator
    auto start_std = std::chrono::high_resolution_clock::now();
    {
        std::list<int> stdList;
        for (int i = 0; i < numOperations; ++i) {
            stdList.push_back(i);
        }
        stdList.clear();
    }
    auto end_std = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed_std = end_std - start_std;
    std::cout << "⏱️  Standard std::allocator: " << elapsed_std.count() << " ms\n";
    
    // Benchmark 2: Custom Pool Allocator
    // std::list uses nodes, where each node size is sizeof(int) + 2 * sizeof(void*) (approx 24 bytes on 64-bit)
    // We allocate a pool for 50000 blocks of that node size
    struct ListNode {
        int val;
        void* prev;
        void* next;
    };
    
    MemoryPool pool(sizeof(ListNode), numOperations);
    PoolAllocator<int> poolAlloc(pool);
    
    auto start_pool = std::chrono::high_resolution_clock::now();
    {
        std::list<int, PoolAllocator<int>> poolList(poolAlloc);
        for (int i = 0; i < numOperations; ++i) {
            poolList.push_back(i);
        }
        poolList.clear();
    }
    auto end_pool = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed_pool = end_pool - start_pool;
    std::cout << "⏱️  Custom PoolAllocator:   " << elapsed_pool.count() << " ms\n";
    
    double speedup = elapsed_std.count() / elapsed_pool.count();
    std::cout << "🚀 Performance Multiplier: " << speedup << "x faster!\n";
    std::cout << "============================================\n";
}

int main() {
    std::cout << "🚀 Starting Safe Memory Manager Showcase 🚀" << std::endl;
    
    // 1. Showcase Safe Memory Tracking & Leak Detection
    std::cout << "\nCreating tracked allocations..." << std::endl;
    int* p1 = safe_new int(42);
    double* p2 = safe_new double(3.14159);
    
    std::cout << "Value 1: " << *p1 << " (Tracked at address: " << p1 << ")" << std::endl;
    std::cout << "Value 2: " << *p2 << " (Tracked at address: " << p2 << ")" << std::endl;
    
    // Intentionally delete one and leak the other to show leak detection in tests
    std::cout << "Deallocating p1..." << std::endl;
    delete p1;
    
    std::cout << "Leaving p2 leaked to demonstrate Tracker reporting..." << std::endl;
    MemoryTracker::getInstance().reportLeaks();
    
    // Clean up leaked pointer p2 so our main doesn't crash on standard program termination checks
    delete p2;
    std::cout << "\nCleaned up p2. Re-reporting leak status:" << std::endl;
    MemoryTracker::getInstance().reportLeaks();
    
    // 2. Showcase Memory Pool performance
    runBenchmark();
    
    return 0;
}
