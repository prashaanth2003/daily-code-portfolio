#include "MemoryTracker.hpp"
#include <iostream>
#include <cstdlib>

MemoryTracker& MemoryTracker::getInstance() {
    static MemoryTracker instance;
    return instance;
}

void MemoryTracker::registerAllocation(void* ptr, size_t size, const char* file, int line) {
    std::lock_guard<std::mutex> lock(mtx);
    if (ptr) {
        allocations[ptr] = {size, file, line};
        activeBytes += size;
        totalAllocated += size;
    }
}

void MemoryTracker::registerDeallocation(void* ptr) {
    std::lock_guard<std::mutex> lock(mtx);
    auto it = allocations.find(ptr);
    if (it != allocations.end()) {
        activeBytes -= it->second.size;
        allocations.erase(it);
    }
}

void MemoryTracker::reportLeaks() {
    std::lock_guard<std::mutex> lock(mtx);
    std::cout << "\n============================================\n";
    std::cout << "🔍  MEMORY TRACKER ANALYSIS REPORT  🔍\n";
    std::cout << "============================================\n";
    if (allocations.empty()) {
        std::cout << "🎉 SUCCESS: No memory leaks detected. Clean exit!\n";
        std::cout << "============================================\n";
        return;
    }

    std::cout << "⚠️  WARNING: " << allocations.size() << " active memory leak(s) detected!\n\n";
    size_t totalLeaked = 0;
    for (const auto& [ptr, alloc] : allocations) {
        std::cout << "👉 Address: " << ptr 
                  << " | Size: " << alloc.size << " bytes\n"
                  << "   Allocated in: " << (alloc.file ? alloc.file : "unknown") 
                  << " at line " << alloc.line << "\n\n";
        totalLeaked += alloc.size;
    }
    std::cout << "Total Leaked Memory: " << totalLeaked << " bytes\n";
    std::cout << "============================================\n";
}

size_t MemoryTracker::getActiveAllocationsCount() {
    std::lock_guard<std::mutex> lock(mtx);
    return allocations.size();
}

size_t MemoryTracker::getActiveBytesCount() {
    std::lock_guard<std::mutex> lock(mtx);
    return activeBytes;
}

// Global operator overloads
void* operator new(size_t size, const char* file, int line) {
    void* ptr = std::malloc(size);
    if (!ptr) throw std::bad_alloc();
    MemoryTracker::getInstance().registerAllocation(ptr, size, file, line);
    return ptr;
}

void* operator new[](size_t size, const char* file, int line) {
    void* ptr = std::malloc(size);
    if (!ptr) throw std::bad_alloc();
    MemoryTracker::getInstance().registerAllocation(ptr, size, file, line);
    return ptr;
}

// Fallback standard overloads (for standard std:: allocations or external libs)
void* operator new(size_t size) {
    void* ptr = std::malloc(size);
    if (!ptr) throw std::bad_alloc();
    MemoryTracker::getInstance().registerAllocation(ptr, size, "unknown", -1);
    return ptr;
}

void* operator new[](size_t size) {
    void* ptr = std::malloc(size);
    if (!ptr) throw std::bad_alloc();
    MemoryTracker::getInstance().registerAllocation(ptr, size, "unknown", -1);
    return ptr;
}

void operator delete(void* ptr) noexcept {
    MemoryTracker::getInstance().registerDeallocation(ptr);
    std::free(ptr);
}

void operator delete[](void* ptr) noexcept {
    MemoryTracker::getInstance().registerDeallocation(ptr);
    std::free(ptr);
}
