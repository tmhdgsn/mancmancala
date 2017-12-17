//
// Created by damel on 14/12/17.
//
#include <iostream>
#include "agent.h"

int main(int argc, char *argv[]) {

    if (argc < 5) {
        run(.45, .1, .3, .1);
    } else {
        run(std::stod(argv[1]), std::stod(argv[2]), std::stod(argv[3]), std::stod(argv[4]));
    }
}