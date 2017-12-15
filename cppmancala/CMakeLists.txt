cmake_minimum_required(VERSION 3.9)
project(cppmancala)

set(CMAKE_CXX_STANDARD 11)

# Set the default build type to 'Release'
if (NOT CMAKE_BUILD_TYPE)
	set(default_build_type "Release")
	message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
	set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE STRING "Choose the type of build." FORCE)
endif()

option(TEST "Build tests." OFF)

# Now simply link against gtest or gtest_main as needed. Eg
add_subdirectory(src)
add_subdirectory(main_app)

if(TEST)
    add_subdirectory(tests)
endif(TEST)

