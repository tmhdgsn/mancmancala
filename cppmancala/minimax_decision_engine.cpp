//
// Created by damel on 12/12/17.
//
#include <tuple>
#include "decision_engine.h"


namespace minimax {
    std::tuple<double, int> max_min(std::array<int, 16> board,
                                    int side, double alpha, double beta);

    std::tuple<double, int> min_max(std::array<int, 16> board,
                                    int side, double alpha, double beta);

    int get_move(std::array<int, 16> board, int side) {
        auto alpha = -std::numeric_limits<double>::infinity();
        auto beta = std::numeric_limits<double>::infinity();
        auto reward_move = max_min(board, side, alpha, beta);
        return std::get<1>(reward_move);
    }

    std::tuple<double, int> max_min(std::array<int, 16> board,
                                    int side, double alpha, double beta) {
        int move = 0;
        for (int i = 0; i < 7; i++) {
            if (board[i + side] > 0) {
                move = i;
                break;
            }
        }
        return {10, move};
    }

    std::tuple<double, int> min_max(std::array<int, 16> board,
                                    int side, double alpha, double beta){

        return {10, 1};
    };
}

