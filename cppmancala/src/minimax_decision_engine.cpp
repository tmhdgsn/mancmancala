//
// Created by damel on 12/12/17.
// edited by tom h on 14/12/17
#include <tuple>
#include <iostream>
#include <ctime>
#include <array>
#include <limits>
#include "decision_engine.h"


namespace minimax {

    int get_move(std::array<int, 16> board, int side, bool has_moved) {
        int move = -1;
        bool game_over;
        double alpha;
        double beta;
        std::tuple<double, int, bool> reward_move;
        const auto now = std::time(nullptr) + 35;
        for (int depth = 6; depth < 40; depth++) {
            alpha = -std::numeric_limits<double>::infinity();
            beta = std::numeric_limits<double>::infinity();
            reward_move = max_min(board, side, alpha, beta, depth, has_moved);
            move = std::get<1>(reward_move);
            game_over = std::get<2>(reward_move);
            if (game_over or std::time(nullptr) >= now)
                break;
        }
        return move;
    }

    std::tuple<double, int, bool>
    max_min(std::array<int, 16> board, int agent_side, double alpha, double beta, int max_depth, bool agent_has_moved) {
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

        // Check SWAP path
        if (agent_side == de::NORTH && !agent_has_moved) {
            // copy the board to represent the child
            std::copy(board.begin(), board.end(), child_board.begin());

            // recurse with to the minimizer
            child_state = min_max(child_board, 8 - agent_side, alpha, beta, max_depth - 1, true);
            child_r = std::get<0>(child_state);
            game_over = std::get<2>(child_state);

            // update the reward if child reward is higher
            reward = std::max(reward, child_r);
            // update alpha
            alpha = std::max(alpha, reward);

            // exit if reward is bigger than beta
            if (reward >= beta) {
                return {reward, -1, game_over};
            }
        }

        for (auto &pit : de::sorted_mvs_by_heuristics(board, agent_side)) {
            // if legal move
            board_repeat_tuple = de::get_next_board(board, pit, agent_side);
            child_board = std::get<0>(board_repeat_tuple);
            repeat = std::get<1>(board_repeat_tuple);

            // if it's our go again repeat
            if (repeat && agent_has_moved) {
                child_state = max_min(child_board, agent_side, alpha, beta, max_depth - 1, true);
            } else {
                child_state = min_max(child_board, agent_side, alpha, beta, max_depth - 1, agent_has_moved);
            }

            child_r = std::get<0>(child_state);
            game_over = std::get<2>(child_state);

            // update the reward if child reward is higher
            if (child_r > reward) {
                reward = child_r;
                best_move = pit;
            }

            // update alpha
            alpha = std::max(alpha, reward);

            // exit if reward is bigger than beta
            if (reward >= beta) {
                return {reward, pit, game_over};
            }
        }
        return {reward, best_move, game_over};
    }

    std::tuple<double, int, bool>
    min_max(std::array<int, 16> board, int agent_side, double alpha, double beta, int max_depth, bool agent_has_moved) {
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

        // Check SWAP path for minimizer
        if (opp_side == de::NORTH && !agent_has_moved) {
            // copy the board to represent the child
            std::copy(board.begin(), board.end(), child_board.begin());

            // recurse with to the maximizer
            child_state = max_min(child_board, opp_side, alpha, beta, max_depth - 1, true);
            child_r = std::get<0>(child_state);
            game_over = std::get<2>(child_state);

            // update the reward if child reward is higher
            reward = std::min(reward, child_r);
            // update alpha
            beta = std::min(beta, reward);

            // exit if reward is bigger than beta
            if (reward <= alpha) {
                return {reward, -1, game_over};
            }
        }

        for (auto &pit : de::sorted_mvs_by_heuristics(board, opp_side)) {
            board_repeat_tuple = de::get_next_board(board, pit, opp_side);
            child_board = std::get<0>(board_repeat_tuple);
            repeat = std::get<1>(board_repeat_tuple);

            // if it's our go again repeat
            if (repeat) {
                child_state = min_max(child_board, agent_side, alpha, beta, max_depth - 1, true);
            } else {
                child_state = max_min(child_board, agent_side, alpha, beta, max_depth - 1, true);
            }

            child_r = std::get<0>(child_state);
            game_over = std::get<2>(child_state);

            // update the reward if child reward is lower
            if (child_r < reward) {
                reward = child_r;
                best_move = pit;
            }
            // update beta
            beta = std::min(reward, beta);

            // exit if less than the max seen by parent
            if (reward <= alpha) {
                return {reward, best_move, game_over};
            }
        }
        return {reward, best_move, game_over};
    };
}