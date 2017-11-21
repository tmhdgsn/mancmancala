from copy import deepcopy

from game import Game
from agent import play_hole
from side import Side


def test_can_play_a_hole():
    g = Game()
    board = g.board
    side = Side.SOUTH
    outcome = play_hole(5, board, side)

    print_board(outcome)


def test_play_hole():
    board = [
        [0, 0, 0, 0, 11, 11, 11, 4],
        [0, 14, 10, 10, 9, 9, 8, 1]
    ]
    print_board(board)
    print("------------------")

    side = Side.NORTH
    my_side = board[side.value]
    for i in range(len(my_side) - 1):
        if my_side[i] > 0:
            board_copy = deepcopy(board)
            print_board(play_hole(i, board_copy, side))
            print("------------------")


def print_board(board):
    north, south = board
    north = "%d -- %s" % (north[-1], " ".join(map(str, reversed(north[:7]))))
    south = "%s -- %d" % (" ".join(map(str, south[:7])), south[-1])
    print(f"{north}\n{south}")


if __name__ == '__main__':
    test_can_play_a_hole()
    test_play_hole()
