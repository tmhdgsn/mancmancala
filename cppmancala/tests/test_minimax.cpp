//
// Created by Harshdeep Singh on 13/12/17.
//


#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../decision_engine.h"

namespace minimax {

    // Test for get_move - minimax - for other side - has moved
    TEST(GetMove_Test, GetMoveSideMoved) {
        EXPECT_EQ(5, get_move({0, 1, 2, 1, 4, 0, 0, 25, 1, 2, 0, 3, 2, 2, 0, 55}, 8, true));
    };

    // Test for get_move - minimax - for side - has not moved
    TEST(GetMove_Test, GetMoveSideNotMoved) {
        EXPECT_EQ(-1, get_move({1, 1, 2, 1, 4, 1, 1, 22, 1, 2 ,1 ,3 , 2, 2, 1, 53}, 0, false));
    };
}