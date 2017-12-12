//
// Created by damel on 12/12/17.
//

#ifndef CPLUSMANCALA_DECISION_ENGINE_H
#define CPLUSMANCALA_DECISION_ENGINE_H

#include <array>

namespace minimax{
    int get_move(std::array<int, 16> board, int side);
}

#endif //CPLUSMANCALA_DECISION_ENGINE_H
