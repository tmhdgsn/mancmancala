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
                    cmd << "java -jar 2012/ManKalah.jar \"java -jar 2012/JimmyPlayer.jar\" \"cppmancala/cmake-build-debug/main_app/cppmancala "
                        << " " << score
                        << " " << o_capture
                        << " " << d_capture
                        << " " << chains
                        << " \"";
                    system(cmd.str().c_str());
                }
            }
        }
    }
    return 0;
}