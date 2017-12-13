//
// Created by t on 12/12/17.
//

#ifndef CPLUSMANCALA_GAMESTATE_H
#define CPLUSMANCALA_GAMESTATE_H

#include <random>
#include <vector>
#include <cmath>
#include <array>
#include <memory>
#include <tuple>
#include <algorithm>
#include "decision_engine.h"


array<int, 7> get_legal_moves(array<int, 16> board, int side) {
    array<int, 7> moves{};
    for (int i = 0; i < 8; i++){
        moves[i] = (board[i + side] != 0) ? i : -1;
    }
    return moves;
};


using namespace std;

class GameState {
    typedef shared_ptr<GameState> ptr;
public:


    explicit GameState(array<int, 16> _board, int _side, GameState* _parent = nullptr, int _move = NULL){
        copy(_board.begin(), _board.end(), board.begin());
        side = _side;
        parent = _parent;
        move = _move;

        score = 0.0;
        no_visits = 0;
    }

    array<int, 16> get_board() const { return board; }
    int _side() const { return side; }
    int _move() const { return move; }
    int visits() const {return no_visits; }
    float _score() const { return score; }

    GameState* get_parent() const { return parent; }
    GameState* get_child(int idx) { return children[idx].get(); }


    GameState* expand_node() {
        auto moves = get_legal_moves(this->board, this->side);
        shuffle(moves.begin(), moves.end(), std::mt19937(std::random_device()()));
        return gen_child_node(moves[0]);
    }

    void update_score(const vector<float>& scores) {
        this->score = scores[this->side];
        no_visits++;
    }

    bool is_node_game_over(){
        return de::game_over(this->board);
    }


    vector<ptr> _children()const {
        return this->children;
    }

private:
    GameState* parent;
    vector<ptr> children;
    array<int, 16> board{};
    int side;
    int move;


    // to calculate UTC value
    int no_visits;
    float score;



    GameState* gen_child_node(const int _move){
        auto * child = new GameState(board, side, this, _move);
        de::play_move(child->board, _move, side);
        children.emplace_back(child);
        return child;
    }

};


#endif //CPLUSMANCALA_GAMESTATE_H
