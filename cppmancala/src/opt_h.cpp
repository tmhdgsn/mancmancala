#include <iostream>
#include <sstream>
#include "opt_h.h"

int main() {
    /*
     * for each parameter in the heuristic function

        iterate through potential weights playing the game for each set of weights
     */
    const double MAX = 2.0;

    for (double x1 = opt_h::SCORE_WEIGHT; x1 <= MAX; x1 + 0.1){
        for (double x2 = opt_h::O_CAPTURE; x2 <= MAX; x2 + 0.1){
            for (double x3 = opt_h::D_CAPTURE; x3 <= MAX; x3 + 0.1){
                for (double x4 = opt_h::CHAINS_WEIGHT; x4 <= MAX; x4 + 0.1){

                    // run game with these weights
                    std::stringstream cmd;
                    cmd << "java -jar 2012/ManKalah.jar \"java -jar 2012/JimmyPlayer.jar\" \"cppmancala/cmake-build-debug/main_app/cppmancala "
                        << " " << x1
                        << " " << x2
                        << " " << x3
                        << " " << x4
                        << " \"";
                    system(cmd.str().c_str());
                }
            }
        }
    }
    return 0;
}