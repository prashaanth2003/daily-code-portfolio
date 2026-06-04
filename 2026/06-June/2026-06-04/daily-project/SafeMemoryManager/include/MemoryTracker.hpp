#ifndef MEMORY_TRACKER_HPP
#define MEMORY_TRACKER_HPP

#include <cstddef>
#include <unordered_map>
#include <mutex>

struct Allocation {
    size_t size;
    const char* file;
    int line;
};

class MemoryTracker {
public:
    static MemoryTracker& getInstance();
    
    void registerAllocation(void* ptr, size_t size, const char* file, int line);
    void registerDeallocation(void* ptr);
    void reportLeaks();
    size_t getActiveAllocationsCount();
    size_t getActiveBytesCount();

private:
    MemoryTracker() = default;
    ~MemoryTracker() = default;
    MemoryTracker(const MemoryTracker&) = delete;
    MemoryTracker& operator=(const MemoryTracker&) = delete;

    std::unordered_map<void*, Allocation> allocations;
    size_t totalAllocated = 0;
    size_t activeBytes = 0;
    std::mutex mtx;
};

// Overload of new with file/line tracking
void* operator new(size_t size, const char* file, int line);
void* operator new[](size_t size, const char* file, int line);

// Standard deletes
void operator delete(void* ptr) noexcept;
void operator delete[](void* ptr) noexcept;

#define safe_new new(__FILE__, __LINE__)

#endif // MEMORY_TRACKER_HPP
