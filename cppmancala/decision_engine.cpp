//
// Created by damel on 12/12/17.
//
#include <tuple>
#include "decision_engine.h"

namespace de {
    bool game_over(std::array<int, 16> board) {
        auto north_mankalah = board.begin() + MANKALAH;
        // minus one as the final element is the south mankalah
        for (auto pit = board.begin(); pit < board.end() - 1; pit++) {
            if (pit != north_mankalah && *pit > 0)
                return false;
        }
        return true;
    }

    bool play_move(std::array<int, 16> board, int move, int side) {
        auto hole = board.begin() + move + side;
        int seeds = *hole;
        *hole++ = 0;
        int opp_side = (8 - side);
        auto opponents_mankalah = board.begin() + opp_side + de::MANKALAH;
        auto my_mankalah = board.begin() + side + de::MANKALAH;
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
        auto opposite_hole = board.begin() + (my_mankalah - hole + opp_side);
        if (*hole == 0 && *opposite_hole > 0) {
            *my_mankalah += *opposite_hole;
            (*my_mankalah)++;
            return false;
        }
        // play final bead
        (*hole)++;
        // my go again if I finish in my mankalah
        return hole == my_mankalah;
    }

    std::tuple<std::array<int, 16>, bool> get_next_board(std::array<int, 16> board,
                                                         int move, int side) {
        std::array<int, 16> board_copy{};
        std::copy(board.begin(), board.end(), board_copy.begin());
        auto repeat = play_move(board_copy, move, side);
        return {board_copy, repeat};
    };
}

