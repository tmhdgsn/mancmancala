
class DecisionEngine:
    MANKALAH = 7

    def __init__(self, agent):
        self.agent = agent

    def get_move(self):
        raise NotImplementedError()

    @classmethod
    def intermediate_score(cls, board, side):
        return board[side.value][cls.MANKALAH] - board[side.opposite().value][cls.MANKALAH]

    @classmethod
    def game_score(cls, board, side):
        opponent_score = sum(board[side.opposite().value])
        my_score = board[side.value][cls.MANKALAH]
        return my_score - opponent_score

    @classmethod
    def play_hole(cls, hole, board_copy, agent_side):
        seeds = board_copy[agent_side.value][hole]
        board_copy[agent_side.value][hole] = 0
        cur_hole = (hole + 1)
        current_side = agent_side if cur_hole < 8 else agent_side.opposite()
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
        return current_side == agent_side and cur_hole == 0

    def __repr__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class BasicStrategy(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def get_move(self):
        board_side = self.agent.game[self.agent.side.value]
        for i in range(self.MANKALAH - 1, -1, -1):
            if board_side[i] > 0:
                return i + 1

    def __repr__(self):
        return "Basic Strategy"

    def __str__(self):
        return "Basic Strategy"
