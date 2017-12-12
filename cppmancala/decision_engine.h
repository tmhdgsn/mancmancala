//
// Created by damel on 12/12/17.
//

#ifndef CPLUSMANCALA_DECISION_ENGINE_H
#define CPLUSMANCALA_DECISION_ENGINE_H

#include <array>

namespace minimax {
    int get_move(std::array<int, 16> board, int side);
}

namespace de {
    bool game_over(std::array<int, 16> board);

    int game_score(std::array<int, 16> board, int side);

    double heuristic(std::array<int, 16> board, int side);

    std::tuple<std::array<int, 16>, bool> get_next_board(std::array<int, 16> board, int move, int side);

    static const int NORTH = 0;
    static const int SOUTH = 8;
    static const int MANKALAH = 7;
}
#endif //CPLUSMANCALA_DECISION_ENGINE_H
