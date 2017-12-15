//
// Created by damel on 13/12/17.
// inspired by https://arxiv.org/pdf/1404.1511.pdf
//

#include <tuple>
#include <ctime>
#include <array>
#include <limits>
#include "decision_engine.h"

namespace mtd {

    std::tuple<double, int, bool> mtdf(double firstguess, std::array<int, 16> board, int side, int depth, bool has_moved);

    double firstguess = 0;

    int get_move(std::array<int, 16> board, int side, bool has_moved) {
        std::tuple<double, int, bool> first_guess_move;
        auto move = -1;
        bool game_over; // have we reached a terminal node
        std::tuple<double, int, bool> reward_move;
        const auto now = std::time(nullptr) + 30;
        for (int depth = 5; depth < 24; depth++) {
            first_guess_move = mtdf(firstguess, board, side, depth, has_moved);
            firstguess = std::get<0>(first_guess_move);
            move = std::get<1>(first_guess_move);
            game_over = std::get<2>(first_guess_move);
            if (game_over or std::time(nullptr) >= now)
                break;
        }
        return move;
    }

    std::tuple<double, int, bool> mtdf(double firstguess, std::array<int, 16> board, int side, int depth, bool has_moved) {
        auto upperbound = std::numeric_limits<double>::infinity();
        auto lowerbound = -std::numeric_limits<double>::infinity();
        auto g = firstguess;
        std::tuple<double, int, bool> full_game_state_tuple;
        double beta;
        while (lowerbound < upperbound) {
            beta = g == lowerbound ? g + 1 : g;
                full_game_state_tuple = minimax::max_min(board, side, beta - 5, beta, depth, has_moved);
            g = std::get<0>(full_game_state_tuple);

            if(g < beta) {
                upperbound = g;
            } else {
                lowerbound = g;
            }
        }
        return full_game_state_tuple;
    }
}