import numpy as np
cimport numpy as np

DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef enum:
    NORTH = 0
    SOUTH = 1


cdef np.ndarray mk_board(int holes, int seeds):
    cdef np.ndarray board = np.ndarray(dtype=DTYPE, shape=(2, holes + 1))
    board.fill(seeds)
    board[:, -1] = 0
    return board