# constants that define side of board
NORTH = 0
SOUTH = 1


class Board:
    def __init__(self, holes, seeds):
        self.holes = holes
        self.seeds = seeds
        self.board = [
            [seeds for _ in range(holes + 1)],
            [seeds for _ in range(holes + 1)]
        ]

        # set mancalah's to be empty
        self.board[NORTH][0] = 0
        self.board[SOUTH][0] = 0

    def get_holes(self):
        return self._holes

    def set_holes(self, value):
        self._holes = value

    holes = property(get_holes, set_holes)

    def add_seeds(self, side, hole, seeds):
        if hole < 1 or hole > self.holes or seeds < 0:
            raise ValueError
        self.board[side][hole] += seeds
