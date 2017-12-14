//
// Created by Harshdeep Singh on 13/12/17.
//


#include <gtest/gtest.h>
#include "../src/decision_engine.h"

namespace minimax {

    // Test for get_move - minimax - for other side - has moved
    TEST(GetMove_Test, GetMoveSideMoved) {
        EXPECT_EQ(5, get_move({0, 1, 2, 1, 4, 0, 0, 25, 1, 2, 0, 3, 2, 2, 0, 55}, 8, true));
    };

    // Test for get_move - minimax - for side - has not moved
    TEST(GetMove_Test, GetMoveSideNotMoved) {
        EXPECT_EQ(-1, get_move({1, 1, 2, 1, 4, 1, 1, 22, 1, 2 ,1 ,3 , 2, 2, 1, 53}, 0, false));
    };

    //Test for min max - safe
    TEST(MinMax_Test, MinMaxSafe) {
        auto actual_result = min_max({1, 1, 2, 1, 0, 4, 1, 23, 1, 2 ,1 ,0 , 3, 2, 2, 54}, 0, 1, 1, 5, false);
        std::tuple <double, int, bool> expected_result = {-31, 6, false};
        EXPECT_TRUE(expected_result == actual_result);
    }

    //Test for min max - if game over
    TEST(MinMax_Test, MinMaxSafe_GameOver) {
        auto actual_result = min_max({0, 0, 0, 0, 0, 0, 0, 33, 1, 2 ,1 ,0 , 3, 2, 2, 54}, 0, 1, 1, 5, false);
        std::tuple <double, int, bool> expected_result = {-32, -1, true};
        EXPECT_TRUE(expected_result == actual_result);
    }
}
