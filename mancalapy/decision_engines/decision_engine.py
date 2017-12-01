import numpy as np
from copy import deepcopy

from side import Side


class DecisionEngine:
    MANKALAH = 7

    def __init__(self, agent):
        self.cache = {}
        self.agent = agent

    def get_move(self, game=None) -> int:
        raise ()

    def hash(self, state) -> hash:
        return hash(str(state))

    def get_legal_moves(self, board, side) -> np.array:
        return board[side.value][:self.MANKALAH].nonzero()[0]

    @classmethod
    def intermediate_score(cls, board, side) -> float:
        # paper on heuristics: https://fiasco.ittc.ku.edu/publications/documents/Gifford_ITTC-FY2009-TR-03050-03.pdf
        # H0: Chooses  first valid move(going left to right)
        # H1: (My Mancala – Opponent’s Mancala)
        # H2: How close I am to winning
        # H3: How close my opponent is to winning
        # H4: #of stones close to my home (1/3)
        # H5: #of stones away from my home (1/3)
        # H6: #of stone in the middle (1/3)
        my_mankalah = board[side.value][cls.MANKALAH]
        opponent_mankalah = board[side.opposite().value][cls.MANKALAH]
        return sum(board[side.value]) - sum(board[side.opposite().value])

    @classmethod
    def game_over(cls, board):
        return np.sum(board[Side.NORTH.value][:-1]) == 0 or np.sum(board[Side.SOUTH.value][:-1]) == 0

    # TODO correctly annotate the return type
    def game_score(self, board) -> np.ndarray:
        opponent_score = np.sum(board[self.agent.side.opposite().value])
        my_score = np.sum(board[self.agent.side.value])
        return my_score - opponent_score

    def get_next_boards(self, agent_has_moved, side, board, play) -> (np.array, bool):
        board_hash = self.hash(board)
        if board_hash not in self.cache:
            self.cache[board_hash] = {}
        if play not in self.cache[board_hash]:
            board_copy = deepcopy(board)
            repeat = self.play_hole(play, board_copy, side) and (agent_has_moved or self.agent.side == Side.NORTH)
            self.cache[board_hash][play] = (board_copy, repeat)
            return board_copy, repeat
        return self.cache[board_hash][play]

    @classmethod
    def play_hole(cls, hole, board_copy, agent_side) -> bool:
        seeds = board_copy[agent_side.value][hole]
        board_copy[agent_side.value][hole] = 0
        cur_hole = (hole + 1)
        current_side = agent_side
        while seeds > 1:
            # only increment my mankalah
            if current_side != agent_side and cur_hole == cls.MANKALAH:
                cur_hole = (cur_hole + 1) % 8
                current_side = current_side.opposite()
                continue
            board_copy[current_side.value][cur_hole] += 1
            if cur_hole > 6:
                current_side = current_side.opposite()
            cur_hole = (cur_hole + 1) % 8
            seeds -= 1

        opposite_hole = cls.MANKALAH - 1 - hole
        # check if we can capture opponents pieces
        if cur_hole != cls.MANKALAH and current_side == agent_side \
                and board_copy[current_side.value][cur_hole] == 0 \
                and board_copy[current_side.opposite().value][opposite_hole] > 0:
            captured_seeds = board_copy[current_side.opposite().value][opposite_hole]
            board_copy[current_side.opposite().value][opposite_hole] = 0
            board_copy[current_side.value][cls.MANKALAH] += captured_seeds + 1  # current seed
            return False

        board_copy[current_side.value][cur_hole] += 1
        return current_side == agent_side and cur_hole == cls.MANKALAH

    def __repr__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class BasicStrategy(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def get_move(self, game=None):
        board_side = self.agent.board[self.agent.side.value]
        for i in range(self.MANKALAH - 1, -1, -1):
            if board_side[i] > 0:
                return i + 1

    def __repr__(self):
        return "Basic Strategy"

    def __str__(self):
        return "Basic Strategy"


class AwesomeTactics(DecisionEngine):
    """
    If you are not playing with the capture rule, a simple strategy is to pick a hole on
     your side of the board and never play any stones from it. If you can make your opponent run out of stones first,
     this assures that every stone which lands on that spot will be yours at the end of the game.
    """

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def get_move(self, game=None):
        pass
