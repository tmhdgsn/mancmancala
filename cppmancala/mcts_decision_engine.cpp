//
// Created by t on 12/12/17.
//

#include <tuple>
#include <cmath>
#include <chrono>
#include <cstdlib>
#include "float.h"
#include <random>
#include "decision_engine.h"
#include "GameState.h"


namespace de_mcts {
    int SIM_MAX = 200;
    using namespace std;
    static const double UCT_CONSTANT = sqrt(2);

    class MCTS {
    public:
        typedef shared_ptr<GameState> ptr;
        int *side;
        int movesMade;
        random_device rnd;


        MCTS(int *agent_side) {
            side = agent_side;

        }

        const ptr *next_best_GameState(const GameState *currentState) {

            /// find move with best UTC-score
            float highest_score = numeric_limits<float>::max();
            const ptr *gameState = nullptr;

            /// for each of the resultant game states from our possible moves
            /// retrieve their scores
            for (const ptr &gs : currentState->_children()) {
                float uct_exploitation = gs->_score() / (gs->visits() + FLT_EPSILON);
                float uct_exploration = sqrt(log((float) currentState->visits() + 1) / (gs->visits() + FLT_EPSILON));
                auto uct_score = static_cast<float>(uct_exploitation + UCT_CONSTANT * uct_exploration);

                if (uct_score > highest_score) {
                    highest_score = uct_score;
                    gameState = &gs;
                }

            }
            return gameState;
        }


        void sim(const GameState *gs, array<int, 16> _board, int _side) {
            if (!de::game_over(_board)) {
                for (int sim = 0; sim < SIM_MAX; sim++) {
                    if (de::game_over(_board)) break;
                    // check we have any legal moves
                    auto moves = get_legal_moves(_board, gs->_side());
                    auto no_legal_moves = legal_moves_count(moves);
                    if (no_legal_moves != 0) break;
                    mt19937 random_move(rnd());
                    shuffle(moves.begin(), moves.end(), random_move);
                    auto move = moves[no_legal_moves % moves.size()];
                    auto data = de::get_next_board(_board, move, _side);
                    _board = get<0>(data);
                    bool repeat = get<1>(data);
                    if (_side == 8) { _side = 0; } else { _side = 8; }

                }
            }
        }

        /// given the current board and who's turn return move to agent.
        int get_move(array<int, 16> _board, int side, array<int, 16> board_cache = {}) {

            //initialise timer
            time_t start = time(nullptr);
            time_t limit;
            limit = start + seconds;

            GameState root_node = *new GameState(_board, side);

            while (true) {

                /// ____ SELECT PART OF MCTS ALGORITHM __________
                GameState *gs = &root_node;

                /// using our UTC policy we select the next best game state for us.
                while (!de::game_over(gs->get_board()) && isExpanded(gs)) {
                    gs = (GameState *) next_best_GameState(gs);
                }



                /// NOW EXPAND
                if ((isExpanded(gs)) && !(de::game_over(gs->get_board()))) {
                    array<int, 16> board = gs->get_board();

                    gs->expand_node();
                };

                /// SIMULATION FROM this board.
                sim(gs, gs->get_board(), side);


                float score = gs->_score();

                board_cache.

            }

        }


        bool is_legal(int move) { return move == -1; }

        long legal_moves_count(array<int, 7> moves) {
            return count_if(moves.begin(), moves.end(), is_legal);
        }


        bool isExpanded(GameState *gs) {
            vector<ptr> children = gs->_children();
            //TODO: improve get legal moves to return array of a better size to prevent count check. 
            auto moves = get_legal_moves(gs->get_board(), gs->_side());
            auto no_legal_moves = legal_moves_count(moves);

            bool child_nodes_explored = children.size() == no_legal_moves;
            return !children.empty() && child_nodes_explored;
        }

        int run_simulation(array<int, 16> state, vector<array<int, 16>> visited_boards) {

            GameState *best_GameState = NULL;
            //init root node GameState to be the current game state.);
            auto *rootGameState = new GameState(state, *side);


        }


    private:
        time_t seconds = 5;
    };
}