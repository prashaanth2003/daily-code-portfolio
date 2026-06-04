#ifndef MEMORY_POOL_HPP
#define MEMORY_POOL_HPP

#include <cstddef>
#include <vector>
#include <stdexcept>
#include <cstdlib>

class MemoryPool {
public:
    MemoryPool(size_t blockSize, size_t numBlocks) 
        : blockSize(blockSize), numBlocks(numBlocks) {
        poolSize = blockSize * numBlocks;
        poolBuffer = reinterpret_cast<char*>(std::malloc(poolSize));
        if (!poolBuffer) {
            throw std::bad_alloc();
        }
        
        freeBlocks.reserve(numBlocks);
        for (size_t i = 0; i < numBlocks; ++i) {
            freeBlocks.push_back(poolBuffer + (i * blockSize));
        }
    }
    
    ~MemoryPool() {
        std::free(poolBuffer);
    }
    
    void* allocate() {
        if (freeBlocks.empty()) {
            throw std::runtime_error("MemoryPool exhausted");
        }
        void* ptr = freeBlocks.back();
        freeBlocks.pop_back();
        return ptr;
    }
    
    void deallocate(void* ptr) {
        char* charPtr = reinterpret_cast<char*>(ptr);
        if (charPtr < poolBuffer || charPtr >= poolBuffer + poolSize) {
            throw std::invalid_argument("Pointer is outside MemoryPool range");
        }
        freeBlocks.push_back(charPtr);
    }
    
    size_t getFreeCount() const {
        return freeBlocks.size();
    }
    
    size_t getCapacity() const {
        return numBlocks;
    }

private:
    size_t blockSize;
    size_t numBlocks;
    size_t poolSize;
    char* poolBuffer;
    std::vector<char*> freeBlocks;
};

#endif // MEMORY_POOL_HPP
