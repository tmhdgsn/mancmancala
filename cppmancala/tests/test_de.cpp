//
// Created by Harshdeep Singh on 13/12/17.
//

#include <gtest/gtest.h>
#include "../src/decision_engine.h"
#include <iostream>
#include <map>

namespace de {
    double score_weight = 1;
    double defence_weight = 1;
    double offence_weight = 1;
    double chain_weight = 1;

    // Test for game over - positive
    TEST(GameOver_Positive_Test, Positive) {
        EXPECT_EQ(true, game_over({0, 0, 0, 0, 0, 0, 0, 33, 1, 0, 0, 0, 0, 0, 0, 64}));
    }

    // Test for game over - negative
    TEST(GameOver_Negative_Test, Negative) {
        EXPECT_EQ(false, game_over({3, 2, 1, 2, 0, 0, 0, 25, 1, 0, 0, 0, 4, 0, 0, 60}));
    }

    // Test for game score - negative
    TEST(GameScore_TestN, ScoreN) {
        EXPECT_EQ(-32, game_score({3, 2, 1, 2, 0, 0, 0, 25, 1, 0, 0, 0, 4, 0, 0, 60}, NORTH));
    }

    //Test for game score - positive
    TEST(GameScore_TestP, ScoreP) {
        EXPECT_EQ(24, game_score({4, 3, 7, 2, 0, 0, 0, 45, 1, 3, 2, 0, 4, 0, 0, 27}, NORTH));
    }

    //Test for game score - negative - side change
    TEST(GameScore_TestNSide, ScoreNSide) {
        EXPECT_EQ(-24, game_score({4, 3, 7, 2, 0, 0, 0, 45, 1, 1, 2, 0, 2, 0, 0, 31}, SOUTH));
    }

    // Test for heuristic - north
    TEST(GameHeuristicNorth, HeuristicNorth) {
        EXPECT_EQ(-35, heuristic({3, 2, 1, 2, 0, 0, 0, 25, 1, 0, 0, 0, 4, 0, 0, 60}, NORTH));
    }

    // Test for heuristic - south
    TEST(GameHeuristicSouth, HeuristicSouth) {
        EXPECT_EQ(36, heuristic({3, 2, 1, 1, 0, 0, 0, 26, 1, 0, 0, 0, 2, 0, 0, 62}, SOUTH));
    }

    //
    TEST(GameHeuristicSouth, NewHeuristicSouth) {
        EXPECT_EQ(10, heuristic({5, 11, 1, 0, 12, 1, 0, 7, 6, 2, 15, 0, 0, 14, 14, 10}, SOUTH));
    }

    TEST(GameHeuristicNorth_HeuristicNorth_Test, Heuristic) {
        EXPECT_TRUE(heuristic({0, 2, 7, 14, 0, 14, 13, 4, 4, 0, 15, 6, 1, 0, 0, 18}, SOUTH) < 0);
    }

    TEST(GameHeuristicSouth_HeuristicSouth_Test, Heuristic) {
        EXPECT_TRUE(heuristic({0, 0, 3, 2, 2, 0, 9, 22, 2, 0, 2, 4, 2, 0, 15, 35}, SOUTH) < 0);
    }

    TEST(GameHeuristicSouth_HeuristicSouth_Test, Heuristic_Takes) {
        EXPECT_TRUE(heuristic({0, 11, 0, 11, 10, 10, 9, 2, 9, 1, 9, 0, 0, 10, 10, 6}, SOUTH) < 0);
    }

    // Test for game next board - south - no repeat
    TEST(GameNextBoard_1, NextBoard_1) {
        auto next_tuple = get_next_board({3, 2, 1, 1, 0, 0, 0, 26, 1, 0, 0, 0, 2, 0, 0, 62}, 4, SOUTH);
        std::array<int, 16> expected_board = {0, 2, 1, 1, 0, 0, 0, 26, 1, 0, 0, 0, 0, 1, 0, 66};
        bool expected_repeat = false;
        EXPECT_EQ(expected_repeat, std::get<1>(next_tuple));
        EXPECT_TRUE(expected_board == std::get<0>(next_tuple));
    }

    // Test for game next board - north - no repeat
    TEST(GameNextBoard_2, NextBoard_2) {
        auto next_tuple = get_next_board({3, 2, 1, 3, 0, 0, 0, 24, 1, 0, 0, 0, 0, 1, 1, 62}, 3, NORTH);
        std::array<int, 16> expected_board = {3, 2, 1, 0, 1, 1, 0, 26, 0, 0, 0, 0, 0, 1, 1, 62};
        bool expected_repeat = false;
        EXPECT_EQ(expected_repeat, std::get<1>(next_tuple));
        EXPECT_TRUE(expected_board == std::get<0>(next_tuple));
    }

    TEST(GameNextBoard_3, Nextboard_3) {
        auto next_tuple = get_next_board({3, 5, 11, 11, 1, 10, 0, 4, 2, 1, 4, 0, 14, 14, 13, 5}, 4, SOUTH);
        std::array<int, 16> expected_board = {4, 6, 12, 0, 2, 11, 1, 4, 3, 2, 5, 0, 0, 15, 14, 19};
        EXPECT_TRUE(expected_board == std::get<0>(next_tuple));
    }
}
