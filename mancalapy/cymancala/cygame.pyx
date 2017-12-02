import numpy as np
cimport numpy as np

DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef enum:
    NORTH = 0
    SOUTH = 1


cdef np.ndarray create_board(int holes, int seeds):
    cdef np.ndarray board = np.ndarray(dtype=DTYPE, shape=(2, holes + 1))
    board.fill(seeds)
    board[:, -1] = 0
    return board



def print_board(board):
    north, south = board
    north = "%d -- %s" % (north[-1], " ".join(map(str, reversed(north[:7]))))
    south = "%s -- %d" % (" ".join(map(str, south[:7])), south[-1])
    print(f"{north}\n{south}")


def update_board(board, raw_state):
    state = raw_state.split(",")
    board[NORTH] = np.array(list(map(int, state[:8])))
    board[SOUTH] = np.array(list(map(int, state[8:])))