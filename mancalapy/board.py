from side import Side

# constants that define side of board
NORTH_ROW = 0
SOUTH_ROW = 1


def check_seeds(seeds):
    if seeds < 0:
        raise ValueError("There has to be  non-negative number of seeds. But %s were requested." % seeds)


def idx_of_side(side):
    if side is Side.NORTH:
        return NORTH_ROW
    else:
        return SOUTH_ROW


class Board:
    def __init__(self, board=None):
        if board:
            self.board = board.board
            self.holes = board.holes
            self.seeds = board.seeds
        else:
            self.board = []
            self.holes = 0
            self.seeds = 0

    @classmethod
    def from_values(cls, holes=4, seeds=7):
        if holes < 1:
            raise ValueError("There has to be at least one hole.")
        if seeds < 1:
            raise ValueError("There has to be a non-negative number of seeds.")
        board = Board()
        board.board = [
            [seeds for _ in range(holes + 1)],
            [seeds for _ in range(holes + 1)]
        ]
        # set mancalah's to be empty
        board.board[NORTH_ROW][-1] = 0
        board.board[SOUTH_ROW][-1] = 0

        board.holes = holes
        board.seeds = seeds
        return cls(board)

    def check_hole(self, hole):
        if hole < 1 or hole > self.holes:
            raise ValueError("Hole number must be between 1 and %s" % (len(self.board[NORTH_ROW]) - 1))

    def get_seeds_in_hole(self, side, hole):
        self.check_hole(hole)
        side_idx = idx_of_side(side)
        return self.board[side_idx][hole]

    def set_seeds(self, side, hole, seeds):
        side_idx = self.check_then_fetch_idx(hole, seeds, side)
        self.board[side_idx][hole] = seeds

    def add_seeds(self, side, hole, seeds):
        side_idx = self.check_then_fetch_idx(hole, seeds, side)
        self.board[side_idx][hole] += seeds

    def check_then_fetch_idx(self, hole, seeds, side):
        self.check_hole(hole)
        check_seeds(seeds)
        side_idx = idx_of_side(side)
        return side_idx

    def get_opposite_seeds(self, side, hole):
        self.check_hole(hole)
        side_idx = idx_of_side(side)
        return self.board[1 - side_idx][self.holes + 1 - hole]

    def set_opposite_seeds(self, side, hole, seeds):
        side_idx = self.check_then_fetch_idx(hole, seeds, side)
        self.board[1 - side_idx][self.holes + 1 - hole] = seeds

    def add_opposite_seeds(self, side, hole, seeds):
        self.check_hole(hole)
        check_seeds(seeds)
        side_idx = idx_of_side(side)
        self.board[1 - side_idx][self.holes + 1 - hole] += seeds

    def get_seeds_in_store(self, side):
        side_idx = idx_of_side(side)
        return self.board[side_idx][0]

    def set_seeds_in_store(self, side, seeds):
        check_seeds(seeds)
        side_idx = idx_of_side(side)
        self.board[side_idx][0] = seeds

    def add_seeds_to_store(self, side, seeds):
        check_seeds(seeds)
        side_idx = idx_of_side(side)
        self.board[side_idx][0] += seeds

    def __repr__(self):
        north, south = self.board
        north = "%d -- %s" % (north[-1], " ".join(map(str, reversed(north[:7]))))
        south = "%s -- %d" % (" ".join(map(str, south[:7])), south[-1])
        return f"{north}\n{south}"
