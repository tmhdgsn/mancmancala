import numpy as np
cimport numpy as np

DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef class Game(object):
    cdef int holes, seeds

    def __init__(self, holes, seeds):
        self.holes = holes
        self.seeds = seeds
