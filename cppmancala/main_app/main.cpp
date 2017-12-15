//
// Created by damel on 14/12/17.
//
#include <cstdlib>
#include "agent.h"

// declare global weights
double SCORE_WEIGHT;
double O_CAPTURE;
double D_CAPTURE;
double CHAINS_WEIGHT;


int main(int argc, char* argv[]) {
    /*
     * retrieve cmd line options
     */
    SCORE_WEIGHT = atof(argv[0]);
    O_CAPTURE = atof(argv[1]);
    D_CAPTURE = atof(argv[2]);
    CHAINS_WEIGHT = atof(argv[3]);

    run();
    return 0;
}