CXXFLAGS := -fPIC -O3 --std=c++20 -Wall
CXXFLAGS += -Iexternal/pybind11/include
CXXFLAGS += $(shell python3-config --includes)

PYTHON := python3
PYTHON_CONFIG := python3-config
SO_SUFFIX := $(shell python3-config --extension-suffix)

SRC_DIR := src
# build directory for object files, artifact will be placed in the root directory
BUILD_DIR := build
TARGET := utils$(SO_SUFFIX)

SRCS := $(shell find $(SRC_DIR) -name '*.cpp')
OBJS := $(addsuffix .o,$(addprefix $(BUILD_DIR)/, $(notdir $(SRCS))))

$(shell mkdir -p $(BUILD_DIR))

$(BUILD_DIR)/$(TARGET): $(OBJS)
	$(CXX) -shared $(CXXFLAGS) -o $@ $^

$(BUILD_DIR)/%.cpp.o: $(SRC_DIR)/%.cpp
	$(CXX) -c $(CXXFLAGS) -o $@ $<

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
