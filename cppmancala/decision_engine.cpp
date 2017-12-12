//
// Created by damel on 12/12/17.
//
#include <tuple>
#include "decision_engine.h"

namespace de {
    
    bool game_over(std::array<int, 16> board) {
        auto north_mankalah = board.begin() + MANKALAH;
        bool north_done = true, south_done = true;
        // check if north player is finished
        for (auto pit = board.begin(); pit < north_mankalah; pit++) {
            if (*pit > 0)
                north_done = false;
        }

        // check if south player is finished
        auto south_mankalah = board.begin() + SOUTH + MANKALAH;
        for (auto pit = board.begin()+SOUTH; pit < south_mankalah; pit++){
            if (*pit > 0)
                south_done = false;
        }

        return north_done || south_done;
    }

    int game_score(std::array<int, 16> board, int side) {
        int opp_side = 8 - side;
        int my_score = 0;
        int opponent_score = 0;
        for (auto pit = board.begin() + side; pit < board.begin() + side + de::MANKALAH + 1; pit++) {
            my_score += *pit;
        }
        for (auto pit = board.begin() + opp_side; pit < board.begin() + opp_side + de::MANKALAH; pit++) {
            opponent_score += *pit;
        }
        return my_score - opponent_score;
    }

    double heuristic(std::array<int, 16> board, int side) {
        int opp_side = 8 - side;
        auto opponents_mankalah = board.begin() + opp_side + de::MANKALAH;
        auto my_mankalah = board.begin() + side + de::MANKALAH;
        return double(*my_mankalah - *opponents_mankalah);
    }

    std::tuple<std::array<int, 16>, bool>  get_next_board(std::array<int, 16> board, int move, int side) {
        auto hole = board.begin() + move + side;
        int seeds = *hole;
        *(hole++) = 0;
        int opp_side = (8 - side);
        auto opponents_mankalah = board.begin() + opp_side + de::MANKALAH;
        auto my_mankalah = board.begin() + side + de::MANKALAH;
        auto my_start_hole = board.begin() + side;
        while (seeds > 1) {
            // don't put seeds in opponent mankalah
            if (hole != opponents_mankalah) {
                (*hole)++;
                seeds--;
            }
            // cycle back to the beginning
            if (++hole == board.end()) {
                hole = board.begin();
            }
        }
        auto opposite_hole = board.begin() + (my_mankalah - 1 - hole + opp_side);
        if (hole < my_mankalah && hole >= my_start_hole && *hole == 0 && *opposite_hole > 0) {
            *my_mankalah += *opposite_hole;
            (*my_mankalah)++;
            return {board, false};
        }
        // play final bead
        (*hole)++;
        // my go again if I finish in my mankalah
        return {board, hole == my_mankalah};
    }
}

