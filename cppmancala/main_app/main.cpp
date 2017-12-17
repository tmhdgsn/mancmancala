//
// Created by damel on 14/12/17.
//
#include <iostream>
#include "agent.h"

int main(int argc, char *argv[]) {

    if (argc < 5) {
        run(1.5, 2, 1.3, 0.8);
    } else {
        run(std::stod(argv[1]), std::stod(argv[2]), std::stod(argv[3]), std::stod(argv[4]));
    }
}