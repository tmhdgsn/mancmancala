from side import Side


class DecisionEngine:
    MANKALAH = 7

    def __init__(self, agent):
        self.agent = agent
        self.moves_made = 0

    def get_move(self, game, first=False):
        raise NotImplementedError()

    @classmethod
    def intermediate_score(cls, board, side):
        my_mankalah = board[side.value][cls.MANKALAH]
        opponent_mankalah = board[side.opposite().value][cls.MANKALAH]
        score = 0
        if my_mankalah != opponent_mankalah and (my_mankalah != 0 or opponent_mankalah != 0):
            higher_mankalah = max(my_mankalah, opponent_mankalah)
            lower_mankalah = min(my_mankalah, opponent_mankalah)
            score = (1 / higher_mankalah * (higher_mankalah - lower_mankalah) + 1) * higher_mankalah
            return score if higher_mankalah == my_mankalah else score * -1
        # return sum(board[side.value]) - sum(board[side.opposite().value])
        return score

    @classmethod
    def game_over(cls, board):
        return sum(board[Side.NORTH.value][:-1]) == 0 or sum(board[Side.SOUTH.value][:-1]) == 0

    @classmethod
    def game_score(cls, board, side):
        opponent_score = sum(board[side.opposite().value])
        my_score = sum(board[side.value])
        return my_score - opponent_score

    @classmethod
    def play_hole(cls, hole, board_copy, agent_side):
        seeds = board_copy[agent_side.value][hole]
        board_copy[agent_side.value][hole] = 0
        cur_hole = (hole + 1)
        current_side = agent_side
        while seeds > 0:
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

        # for the final move check if we get another go
        # if cur_hole = 0, last_hole = MANKALAH
        return current_side.opposite() == agent_side and cur_hole == 0

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
