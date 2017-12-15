//
// Created by t on 15/12/17.
//

#include "opt_h.h"
#include <iostream>
#include <sstream>

int main() {
    /*
     * for each parameter in the heuristic function

        iterate through potential weights playing the game for each set of weights
     */
    const double MAX = 10.0;

    for (int x1 = 1; x1 <= MAX; x1++){
        for (int x2 = 1; x2 <= MAX; x2++){
            for (int x3 = 1; x3 <= MAX; x3++){
                for (int x4 = 1; x4 <= MAX; x4++){

                    double score = x1 / MAX;
                    double o_capture = x2 / MAX;
                    double d_capture = x3 / MAX;
                    double chains = x4 / MAX;

                    // run game with these weights
                    std::stringstream cmd;
                    cmd << "java -jar ../2012/ManKalah.jar \"java -jar ../2012/JimmyPlayer.jar\" \"/cmake-build-debug/main_app/cppmancala "
                        << "-s " << score
                        << " -o " << o_capture
                        << " -d " << d_capture
                        << " -c " << chains
                        << " \"";
                    system(cmd.str().c_str());
                }
            }
        }
    }
    return 0;
}