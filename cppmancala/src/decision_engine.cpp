//
// Created by damel on 12/12/17.
//
#include <tuple>
#include "decision_engine.h"

namespace de {

    int number_of_seeds_i_can_capture(std::array<int, 16> board, int side);

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
        for (auto pit = board.begin() + SOUTH; pit < south_mankalah; pit++) {
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
        for (auto pit = board.begin() + opp_side; pit < board.begin() + opp_side + de::MANKALAH + 1; pit++) {
            opponent_score += *pit;
        }
        return my_score - opponent_score;
    }

    double heuristic(std::array<int, 16> board, int side) {
        int opp_side = 8 - side;
        // increase general score
        auto opponents_mankalah = board.begin() + opp_side + de::MANKALAH;
        auto my_mankalah = board.begin() + side + de::MANKALAH;
        int score = (*my_mankalah - *opponents_mankalah);

        // hoard stones close to mankalah as they're harder to steal
        int hoard_size = *(my_mankalah - 1) + *(my_mankalah - 2);
        // reduce the number of easy captures
        int easy_caps = number_of_seeds_i_can_capture(board, 8 - side);
        // incentivize chaining
        int chaining_opportunities = 0;
        // incentivize capture opps
        int capture_opportunities = number_of_seeds_i_can_capture(board, side);

        for (auto hole = board.begin() + side; hole < my_mankalah; hole++) {
            if (my_mankalah - hole == *hole) {
                chaining_opportunities++;
            }
        }

        // TODO experiment with the game to learn good parameters
        double w1 = 1.5, w2 = 1.2, w3 = 1, w4 = 1, w5 = 1;
        return w1 * score + w2 * hoard_size - w3 * easy_caps + w4 * chaining_opportunities + w5 * capture_opportunities;
    }

    int number_of_seeds_i_can_capture(std::array<int, 16> board, int side) {
        int captures = 0;
        int distance;
        int opp_side = 8 - side;
        auto my_mankalah = board.begin() + side + MANKALAH;
        std::array<int, 16>::iterator land_place;
        std::array<int, 16>::iterator opp_land_place;
        for (auto hole = board.begin() + side; hole < my_mankalah; hole++) {
            distance = int(my_mankalah - hole);
            land_place = board.begin() + side + (*hole - distance - 8);
            opp_land_place = board.begin() + (my_mankalah - 1 - hole + opp_side);
            if (*hole < 16 && (*hole < distance || *hole - distance > 7)
                && (*hole == 15 || *land_place > 0)) {
                captures += *opp_land_place;
            }
        }
        return captures;
    }

    std::tuple<std::array<int, 16>, bool> get_next_board(std::array<int, 16> board, int move, int side) {
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
        // capture if possible
        auto opposite_hole = board.begin() + (my_mankalah - 1 - hole + opp_side);
        if (hole >= my_start_hole && hole < my_mankalah && *hole == 0 && *opposite_hole > 0) {
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

