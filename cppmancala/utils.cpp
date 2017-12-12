//
// Created by damel on 12/12/17.
//
#include <array>
#include <iostream>
#include <tuple>
#include "utils.h"

namespace util {
    void print_array(std::array<int, 16> arr) {
        // used int as int8_t didn't show properly
        for (int item : arr) {
            std::cout << item << " ";
        }
        std::cout << "\n";
    }

    void print_msg_args(std::tuple<std::string, std::string> msg_args) {
        std::cout << "msg_type: " << std::get<0>(msg_args)
                  << " args: " << std::get<1>(msg_args) << std::endl;
    }

    void print_board(std::array<int, 16> board) {
        // print north
        auto north = board.rbegin() + 8;
        std::cout << *north++ << " -- ";
        for (auto item = north; item < board.rend(); ++item) {
            std::cout << *item << " ";
        }

        std::cout << "\n";

        // print south
        auto south = board.begin() + 8;
        for (auto item = south; item < board.end() - 1; item++) {
            std::cout << *item << " ";
        }
        std::cout << " -- " << *(board.end() - 1) << std::endl;
    }


}
