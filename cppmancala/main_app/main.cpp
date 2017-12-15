//
// Created by damel on 14/12/17.
//
#include <cstdlib>
#include "agent.h"
#include "opt_h.h"



int main(int argc, char* argv[]) {
    /*
     * retrieve cmd line options
     */
    opt_h::SCORE_WEIGHT = atof(argv[1]);
    opt_h::O_CAPTURE = atof(argv[2]);
    opt_h::D_CAPTURE = atof(argv[3]);
    opt_h::CHAINS_WEIGHT = atof(argv[4]);

    run();
    return 0;
}