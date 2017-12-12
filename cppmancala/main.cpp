#include <iostream>
#include <sstream>
#include <tuple>
#include "utils.h"
#include "decision_engine.h"


static const int NORTH = 0;

static const int SOUTH = 8;

std::tuple<std::string, std::string> getmessage() {
    std::string input;
    std::cin >> input;
    std::size_t sep = input.find(';');
    return {input.substr(0, sep), input.substr(sep + 1)};
};

void make_move(int move) {
    if (move < 0)
        std::cout << "SWAP\n";
    printf("MOVE;%d\n", move + 1);
}

//CHANGE;3;1,11,10,9,9,8,8,1,8,0,0,9,1,10,10,3;YOU
int main() {
    std::tuple<std::string, std::string> msg_args;
    std::array<int, 16> board{};
    int move;
    char sep;
    int side = NORTH;
    std::string msg_type, args, player;
    while (true) {
        msg_args = getmessage();
        msg_type = std::get<0>(msg_args);
        args = std::get<1>(msg_args);
        if (msg_type == "START") {
            if (args == "South")
                side = SOUTH;
        } else if (msg_type == "CHANGE") {
            auto arg_stream = std::stringstream(args);
            arg_stream >> move;
            arg_stream >> sep;
            for (int i = 0; i < 16; i++) {
                arg_stream >> board[i];
                arg_stream >> sep;
            }
            arg_stream >> player;
            if (player == "YOU") {
                move = minimax::get_move(board, side);
                make_move(move);
            }
        } else if (msg_type == "END") {
            break;
        }
    }

    return 0;
}

