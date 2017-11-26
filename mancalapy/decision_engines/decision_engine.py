import numpy as np

from side import Side


class DecisionEngine:
    MANKALAH = 7

    def __init__(self, agent):
        self.agent = agent

    def get_move(self, game=None, first=False):
        raise NotImplementedError()

    @classmethod
    def intermediate_score(cls, board, side):
        my_mankalah = board[side.value][cls.MANKALAH]
        opponent_mankalah = board[side.opposite().value][cls.MANKALAH]
        score = 0
        # if my_mankalah != opponent_mankalah:
        #     higher_mankalah = max(my_mankalah, opponent_mankalah)
        #     lower_mankalah = min(my_mankalah, opponent_mankalah)
        #     score = (1 / higher_mankalah * (higher_mankalah - lower_mankalah) + 1) * higher_mankalah
        #     return score if higher_mankalah == my_mankalah else score * -1
        return sum(board[side.value]) - sum(board[side.opposite().value])
        # return score

    @classmethod
    def game_over(cls, board):
        return np.sum(board[Side.NORTH.value][:-1]) == 0 or np.sum(board[Side.SOUTH.value][:-1]) == 0

    ## TODO: game_score should always be from the agent perspective
    @classmethod
    def game_score(cls, board, side):
        opponent_score = np.sum(board[side.opposite().value])
        my_score = np.sum(board[side.value])
        return my_score - opponent_score

    @classmethod
    def play_hole(cls, hole, board_copy, agent_side):
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
        if cur_hole != cls.MANKALAH and current_side == agent_side and board_copy[current_side.value][cur_hole] == 0 and \
                board_copy[current_side.opposite().value][opposite_hole] > 0:
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

    def get_move(self, game=None, first=False):
        board_side = self.agent.game[self.agent.side.value]
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

    def get_move(self, first=False):
        pass
