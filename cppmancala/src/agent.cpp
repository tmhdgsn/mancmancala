#include <iostream>
#include <sstream>
#include <tuple>
#include "decision_engine.h"
#include <fstream>
#include "agent.h"
#include "heuristic_params.h"

// declares global reference to heuristic params
double score_weight;
double defence_weight;
double chain_weight;
double capture_weight;

void write_to_file(const std::string &input) {
    const char *path = "/home/damel/git/mancmancala/output.txt";
    std::ofstream output_file(path, std::ios_base::app);
    output_file << input << std::endl;
    output_file.close();
};

std::tuple<std::string, std::string> getmessage() {
    std::string input;
    std::cin >> input;
    std::size_t sep = input.find(';');
    return {input.substr(0, sep), input.substr(sep + 1)};
};

void make_move(int move) {
    if (move < 0)
        std::cout << "SWAP\n";
    else {
        printf("MOVE;%d\n", move + 1);
    }
}

void run(double new_score_weight, double new_defence_weight, double new_chain_weight, double new_capture_weight) {
    // update heuristic params
    score_weight = new_score_weight;
    defence_weight = new_defence_weight;
    chain_weight = new_chain_weight;
    capture_weight = new_capture_weight;

    std::tuple<std::string, std::string> msg_args;
    std::array<int, 16> board{7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0};
    int move;
    std::string last_move;
    char sep;
    int side = de::NORTH;
    std::string msg_type, args, player;
    bool our_go = false;
    bool has_moved = false;
    while (true) {
        msg_args = getmessage();
        msg_type = std::get<0>(msg_args);
        args = std::get<1>(msg_args);
        if (msg_type == "START") {
            if (args == "South") {
                side = de::SOUTH;
                our_go = true;
            }
        } else if (msg_type == "CHANGE") {
            auto pos = args.find(';');
            last_move = args.substr(0, pos);
            if (last_move == "SWAP") {
                our_go = true;
                side = de::NORTH;
            } else {
                auto remaining_args = args.substr(pos + 1);
                auto arg_stream = std::stringstream(remaining_args);
                for (auto pit = board.begin(); pit < board.end(); pit++) {
                    arg_stream >> *pit;
                    arg_stream >> sep;
                }
                arg_stream >> player;
                our_go = player == "YOU";
            }
        } else if (msg_type == "END") {
            break;
        }
        if (our_go) {
            move = minimax::get_move(board, side, has_moved);
            if (move < 0)
                side = 8 - side;
            make_move(move);
            if(!has_moved)
                has_moved = true;
        }
    }
}

