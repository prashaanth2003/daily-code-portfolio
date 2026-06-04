CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Iinclude -O3

SRC_DIR = src
TEST_DIR = tests
OBJ_DIR = obj

# Main executable
TARGET = memory_manager_demo
SRC = $(SRC_DIR)/main.cpp $(SRC_DIR)/MemoryTracker.cpp
OBJ = $(SRC:%.cpp=$(OBJ_DIR)/%.o)

# Test executable
TEST_TARGET = run_tests
TEST_SRC = $(TEST_DIR)/test_memory_manager.cpp $(SRC_DIR)/MemoryTracker.cpp
TEST_OBJ = $(TEST_SRC:%.cpp=$(OBJ_DIR)/%.o)

all: $(TARGET) $(TEST_TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(TEST_TARGET): $(TEST_OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -rf $(OBJ_DIR) $(TARGET) $(TEST_TARGET)

.PHONY: all clean
