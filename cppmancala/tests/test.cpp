//
// Created by Harshdeep Singh on 13/12/17.
//

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../decision_engine.h"

namespace de {
    TEST(GameOver_Positive_Test, Positive) {
        EXPECT_EQ(true, game_over({0, 0, 0, 0, 0, 0, 0, 33, 1, 0 ,0 ,0 , 0, 0, 0, 64}));
    }

    TEST(GameOver_Negative_Test, Negative) {
        EXPECT_EQ(false, game_over({3, 2, 1, 2, 0, 0, 0, 25, 1, 0 ,0 ,0 ,4, 0, 0, 60}));
    }
}