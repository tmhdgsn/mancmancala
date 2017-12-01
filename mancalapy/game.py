from side import Side
import numpy as np


def hash_board(board):
    return hash(board)


def print_board(board):
    north, south = board
    north = "%d -- %s" % (north[-1], " ".join(map(str, reversed(north[:7]))))
    south = "%s -- %d" % (" ".join(map(str, south[:7])), south[-1])
    print(f"{north}\n{south}")


def create_board(holes: int = 7, seeds: int = 7) -> np.array:
    board = np.ndarray(dtype=int, shape=(2, holes + 1))
    board.fill(seeds)
    board[:, -1] = 0
    return board


def update_board(board, raw_state):
    state = raw_state.split(",")
    board[Side.NORTH.value] = np.array(list(map(int, state[:8])))
    board[Side.SOUTH.value] = np.array(list(map(int, state[8:])))
