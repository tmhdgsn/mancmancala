//
// Created by Harshdeep Singh on 14/12/17.
//

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../main/utils.h"
#include <array>


namespace utils {

    //Test for print board - one
    TEST(PrintBoard_Test, PrintBoardOne) {
        testing::internal::CaptureStdout();
        std::array<int, 16> dummy_board = {1, 1, 2, 1, 0, 4, 1, 23, 1, 2 ,1 ,0 , 3, 2, 2, 54};
        util::print_board(dummy_board);
        std::string output = testing::internal::GetCapturedStdout();
        ASSERT_EQ(output, "23 -- 1 4 0 1 2 1 1 \n1 2 1 0 3 2 2  -- 54\n");
    }
}
