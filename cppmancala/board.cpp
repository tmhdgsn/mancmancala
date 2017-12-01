//
// Created by t on 01/12/17.
//
#include <cstdio>
#include <malloc.h>
#include <string>
#include <valarray>     // std::valarray, std::slice
#include <iostream>
#include <cstring>
#include <vector>

const int MANCALA = 7;

typedef enum {
    NORTH = 0,
    SOUTH = 1,
} Side;


void Tokenize(const std::string& str,
              std::vector<std::string>& tokens,
              const std::string& delimiters = ",")
{
    // Skip delimiters at beginning.
    std::string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    std::string::size_type pos = str.find_first_of(delimiters, lastPos);

    while (std::string::npos != pos || std::string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}


void print_board(int** board) {
    printf("%d -- ", board[0][MANCALA]);
    for (int i = 6; i >= 0; i--) {
        printf("%d ", board[0][i]);
    }
    printf("\n");
    for (int i = 0; i < 7; i++) {
        printf("%d ", board[1][i]);
    }
    printf("-- %d\n", board[1][7]);
}

int** create_board(int holes, int seeds) {

    int** board = 0;
    board = new int *[2];
    board[0] = new int[8];
    board[1] = new int[8];

    for (int i = 0; i < 7; i++) {
        board[0][i] = seeds;
        board[1][i] = seeds;
    }
    print_board(board);
    return board;
}

void print_array(int *array, int array_length) {
    for (int i = 0; i < array_length; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}


void update_board(int** board, std::string raw_state) {
    std::string delimiter = ",";
    unsigned long place = 0;
    std::vector<std::string> tokens;
    Tokenize(raw_state, tokens);

    for (int i = 0; i < 8; i++) {
        place += i;
        board[NORTH][i] = (tokens[place]);
    }

    for (int i = 0; i < 8; i++) {
        place += i;
        board[SOUTH][i] = std::stoi(tokens[place]);
    }
}
#include <algorithm>
#include <regex>

int main(int argc, char *argv[]) {
    int **board = create_board(7, 7);
    update_board(board, "0,0,9,9,9,9,9,2,1,9,8,8,8,8,8,1");

    return 0;
};