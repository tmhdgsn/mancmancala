
add_executable(cppmancala main.cpp)

target_include_directories(cppmancala PRIVATE ../src)

target_link_libraries(cppmancala framework)