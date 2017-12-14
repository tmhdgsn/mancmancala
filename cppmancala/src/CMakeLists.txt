
file(GLOB sources
{CMAKE_CURRENT_SOURCE_DIR}/*.h
{CMAKE_CURRENT_SOURCE_DIR}/*.cpp
)
add_library(framework SHARED agent.cpp agent.h utils.h utils.cpp decision_engine.h minimax_decision_engine.cpp decision_engine.cpp
        mcts_decision_engine.cpp mtd_decision_engine.cpp)