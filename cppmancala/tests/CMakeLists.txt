#project(test)

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
add_executable(test_de test_de.cpp)
add_executable(test_minimax test_minimax.cpp)

target_link_libraries(test_de framework ${GTEST_BOTH_LIBRARIES})

target_link_libraries(test_minimax framework  ${GTEST_BOTH_LIBRARIES})

