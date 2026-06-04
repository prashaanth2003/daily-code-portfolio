#include "MemoryTracker.hpp"
#include "MemoryPool.hpp"
#include <iostream>
#include <cassert>
#include <vector>

void testMemoryTracker() {
    std::cout << "Running testMemoryTracker()..." << std::endl;
    size_t initial_allocs = MemoryTracker::getInstance().getActiveAllocationsCount();
    
    int* p = safe_new int(100);
    assert(MemoryTracker::getInstance().getActiveAllocationsCount() == initial_allocs + 1);
    assert(MemoryTracker::getInstance().getActiveBytesCount() >= sizeof(int));
    
    delete p;
    assert(MemoryTracker::getInstance().getActiveAllocationsCount() == initial_allocs);
    std::cout << "✅ testMemoryTracker passed!" << std::endl;
}

void testMemoryPool() {
    std::cout << "Running testMemoryPool()..." << std::endl;
    const size_t numBlocks = 5;
    const size_t blockSize = 16;
    MemoryPool pool(blockSize, numBlocks);
    
    assert(pool.getCapacity() == numBlocks);
    assert(pool.getFreeCount() == numBlocks);
    
    void* p1 = pool.allocate();
    assert(p1 != nullptr);
    assert(pool.getFreeCount() == numBlocks - 1);
    
    void* p2 = pool.allocate();
    assert(p2 != nullptr);
    assert(pool.getFreeCount() == numBlocks - 2);
    
    pool.deallocate(p1);
    assert(pool.getFreeCount() == numBlocks - 1);
    
    pool.deallocate(p2);
    assert(pool.getFreeCount() == numBlocks);
    
    // Test pool exhaustion
    std::vector<void*> allocated;
    for (size_t i = 0; i < numBlocks; ++i) {
        allocated.push_back(pool.allocate());
    }
    assert(pool.getFreeCount() == 0);
    
    bool exceptionThrown = false;
    try {
        pool.allocate();
    } catch (const std::runtime_error&) {
        exceptionThrown = true;
    }
    assert(exceptionThrown);
    
    for (void* ptr : allocated) {
        pool.deallocate(ptr);
    }
    assert(pool.getFreeCount() == numBlocks);
    
    std::cout << "✅ testMemoryPool passed!" << std::endl;
}

int main() {
    std::cout << "======= RUNNING UNIT TESTS =======" << std::endl;
    testMemoryTracker();
    testMemoryPool();
    std::cout << "🎉 ALL UNIT TESTS PASSED SUCCESSFULLY! 🎉" << std::endl;
    return 0;
}
