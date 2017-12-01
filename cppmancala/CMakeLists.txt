cmake_minimum_required(VERSION 3.9)
project(cplusmancala)

set(CMAKE_CXX_STANDARD 17)

add_executable(cplusmancala main.cpp foo.cpp foo.h decision_engine.cpp decision_engine.h board.cpp)