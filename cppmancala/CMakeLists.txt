cmake_minimum_required(VERSION 3.9)
project(cplusmancala)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(lib/googletest)
include_directories(lib/googletest/googletest/include)
include_directories(lib/googletest/googlemock/include)

add_executable(cplusmancala main.cpp utils.h utils.cpp decision_engine.h minimax_decision_engine.cpp decision_engine.cpp mtd_decision_engine.cpp tests/test_de.cpp)

target_link_libraries(cplusmancala gtest gtest_main)