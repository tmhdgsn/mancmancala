cmake_minimum_required(VERSION 3.9)
project(cplusmancala)

set(CMAKE_CXX_STANDARD 17)

add_executable(cplusmancala main.cpp utils.h utils.cpp decision_engine.h minimax_decision_engine.cpp decision_engine.cpp GameState.cpp GameState.h mcts_decision_engine.cpp mtd_decision_engine.cpp)
