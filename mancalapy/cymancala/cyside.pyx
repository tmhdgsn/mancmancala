
cdef enum Side:
    NORTH = 0
    SOUTH = 1

cdef Side opposite(int x):
    return Side.SOUTH if x == Side.NORTH else Side.NORTH