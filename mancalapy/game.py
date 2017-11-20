from side import Side


def check_seeds(seeds):
    if seeds < 0:
        raise ValueError("There has to be  non-negative number of seeds. But %s were requested." % seeds)


class Game:
    def __init__(self, holes=7, seeds=7, board=None):
        self.holes = holes
        self.seeds = seeds
        self.board = board if board else self.create_board(holes, seeds)

    def update_board(self, raw_state):
        state = raw_state.split(",")
        north = [int(i) for i in state[:8]]
        south = [int(i) for i in state[8:]]
        self.board = [north, south]

    @classmethod
    def create_board(cls, holes=7, seeds=7):
        if holes < 1:
            raise ValueError("There has to be at least one hole.")
        if seeds < 1:
            raise ValueError("There has to be a non-negative number of seeds.")

        board = [
            [seeds for _ in range(holes + 1)],
            [seeds for _ in range(holes + 1)]
        ]

        # set mancalah's to be empty
        board[Side.NORTH.value][-1] = 0
        board[Side.SOUTH.value][-1] = 0
        return board

    @classmethod
    def from_values(cls):
        return cls(board=cls.create_board())

    def check_hole(self, hole):
        if hole < 1 or hole > self.holes:
            raise ValueError("Hole number must be between 1 and %s" % (len(self.board[0])))

    def get_seeds_in_hole(self, side, hole):
        self.check_hole(hole)
        side_idx = side.value
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
        side_idx = side.value
        return side_idx

    def get_opposite_seeds(self, side, hole):
        self.check_hole(hole)
        side_idx = side.value
        return self.board[1 - side_idx][self.holes + 1 - hole]

    def set_opposite_seeds(self, side, hole, seeds):
        side_idx = self.check_then_fetch_idx(hole, seeds, side)
        self.board[1 - side_idx][self.holes + 1 - hole] = seeds

    def add_opposite_seeds(self, side, hole, seeds):
        self.check_hole(hole)
        check_seeds(seeds)
        side_idx = side.value
        self.board[1 - side_idx][self.holes + 1 - hole] += seeds

    def get_seeds_in_store(self, side):
        side_idx = side.value
        return self.board[side_idx][0]

    def set_seeds_in_store(self, side, seeds):
        check_seeds(seeds)
        side_idx = side.value
        self.board[side_idx][0] = seeds

    def add_seeds_to_store(self, side, seeds):
        check_seeds(seeds)
        side_idx = side.value
        self.board[side_idx][0] += seeds

    def state(self):
        return self.__repr__()

    def __repr__(self):
        north, south = self.board
        north = "%d -- %s" % (north[-1], " ".join(map(str, reversed(north[:7]))))
        south = "%s -- %d" % (" ".join(map(str, south[:7])), south[-1])
        return f"{north}\n{south}"
