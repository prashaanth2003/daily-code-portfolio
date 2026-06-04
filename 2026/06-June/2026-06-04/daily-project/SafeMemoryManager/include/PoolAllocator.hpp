#ifndef POOL_ALLOCATOR_HPP
#define POOL_ALLOCATOR_HPP

#include "MemoryPool.hpp"
#include <cstddef>
#include <stdexcept>

template <typename T>
class PoolAllocator {
public:
    using value_type = T;
    
    PoolAllocator(MemoryPool& pool) : pool(pool) {}
    
    template <typename U>
    PoolAllocator(const PoolAllocator<U>& other) : pool(other.pool) {}
    
    T* allocate(size_t n) {
        if (n != 1) {
            throw std::runtime_error("PoolAllocator only supports single-element allocations");
        }
        return reinterpret_cast<T*>(pool.allocate());
    }
    
    void deallocate(T* p, size_t n) {
        pool.deallocate(p);
    }
    
    MemoryPool& pool;
};

template <typename T, typename U>
bool operator==(const PoolAllocator<T>& a, const PoolAllocator<U>& b) {
    return &a.pool == &b.pool;
}

template <typename T, typename U>
bool operator!=(const PoolAllocator<T>& a, const PoolAllocator<U>& b) {
    return !(a == b);
}

#endif // POOL_ALLOCATOR_HPP
