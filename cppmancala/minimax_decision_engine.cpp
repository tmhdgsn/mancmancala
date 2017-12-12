//
// Created by damel on 12/12/17.
//
#include <tuple>
#include <iostream>
#include "decision_engine.h"



namespace minimax {
    std::tuple<double, int, bool>
    max_min(std::array<int, 16> board, int agent_side, double alpha, double beta, int max_depth);

    std::tuple<double, int, bool>
    min_max(std::array<int, 16> board, int agent_side, double alpha, double beta, int max_depth);

    int get_move(std::array<int, 16> board, int side) {
        auto alpha = -std::numeric_limits<double>::infinity();
        auto beta = std::numeric_limits<double>::infinity();
        auto reward_move = max_min(board, side, alpha, beta, 6);
        return std::get<1>(reward_move);
    }

    std::tuple<double, int, bool>
    max_min(std::array<int, 16> board, int agent_side, double alpha, double beta, int max_depth) {
        auto reward = -std::numeric_limits<double>::infinity();
        int best_move = -1;
        bool game_over = false;
        if (de::game_over(board)) {
            return {(de::game_score(board, 0)), -1, true};
        } else if (max_depth == 0) {
            return {(de::heuristic(board, agent_side)), -1, false};
        }

        // tuple that holds next board and repeat
        std::tuple<std::array<int, 16>, bool> board_repeat_tuple;
        std::array<int, 16> child_board{};
        bool repeat;
        std::tuple<double, int, bool> child_state;
        double child_r;

        for (int pit_ind = 0; pit_ind < de::MANKALAH; pit_ind++) {
            // if legal move
            if (board[pit_ind + agent_side] > 0) {
                board_repeat_tuple = de::get_next_board(board, pit_ind, agent_side);
                child_board = std::get<0>(board_repeat_tuple);
                repeat = std::get<1>(board_repeat_tuple);

                // if it's our go again repeat
                if (repeat) {
                    child_state = max_min(child_board, agent_side, alpha, beta, max_depth - 1);
                } else {
                    child_state = min_max(child_board, agent_side, alpha, beta, max_depth - 1);
                }

                child_r = std::get<0>(child_state);
                game_over = std::get<2>(child_state);

                // update the reward if child reward is higher
                if (child_r > reward) {
                    reward = child_r;
                    best_move = pit_ind;
                }

                // update alpha
                alpha = std::max(alpha, child_r);

                // exit if reward is bigger than beta
                if (reward > beta) {
                    return {reward, pit_ind, game_over};
                }
            }
        }

        return {reward, best_move, game_over};
    }

    std::tuple<double, int, bool>
    min_max(std::array<int, 16> board, int agent_side, double alpha, double beta, int max_depth) {
        auto reward = std::numeric_limits<double>::infinity();
        int best_move = -1;
        bool game_over = false;
        if (de::game_over(board)) {
            return {(de::game_score(board, 0)), -1, true};
        } else if (max_depth == 0) {
            return {(de::heuristic(board, agent_side)), -1, false};
        }

        // tuple that holds next board and repeat
        std::tuple<std::array<int, 16>, bool> board_repeat_tuple;
        std::array<int, 16> child_board{};
        bool repeat;
        std::tuple<double, int, bool> child_state;
        double child_r;
        int opp_side = 8 - agent_side;
        for (int pit_ind = 0; pit_ind < de::MANKALAH; pit_ind++) {
            // if legal move
            if (board[pit_ind + opp_side] > 0) {
                board_repeat_tuple = de::get_next_board(board, pit_ind, opp_side);
                child_board = std::get<0>(board_repeat_tuple);
                repeat = std::get<1>(board_repeat_tuple);

                // if it's our go again repeat
                if (repeat) {
                    child_state = min_max(child_board, agent_side, alpha, beta, max_depth - 1);
                } else {
                    child_state = max_min(child_board, agent_side, alpha, beta, max_depth - 1);
                }

                child_r = std::get<0>(child_state);
                game_over = std::get<2>(child_state);

                // update the reward if child reward is lower
                if (child_r < reward) {
                    reward = child_r;
                    best_move = pit_ind;
                }
                // update beta
                beta = std::min(reward, beta);

                // exit if less than the max seen by parent
                if (reward < alpha) {
                    return {reward, best_move, game_over};
                }
            }
        }
        return {reward, best_move, game_over};
    };
}