from copy import deepcopy

MANKALAH = 7


class DecisionEngineFactory:
    def __init__(self, agent):
        self.agent = agent

        self.engines = {
            "basic": BasicStrategy(self.agent),
            "minimax": MiniMaxDecisionEngine(self.agent)
        }

    def __getitem__(self, item):
        return self.engines[item]


class DecisionEngine:
    def __init__(self, agent):
        self.agent = agent

    def get_move(self):
        raise NotImplementedError()

    @classmethod
    def intermediate_score(cls, board, side):
        return board[side.value][MANKALAH] - board[side.opposite().value][MANKALAH]

    @classmethod
    def game_score(cls, board, side):
        opponent_score = sum(board[side.opposite().value])
        my_score = board[side.value][MANKALAH]
        return my_score - opponent_score

    @classmethod
    def play_hole(cls, hole, board_copy, agent_side):
        seeds = board_copy[agent_side.value][hole]
        board_copy[agent_side.value][hole] = 0
        cur_hole = (hole + 1)
        current_side = agent_side if cur_hole < 8 else agent_side.opposite()
        while seeds > 0:
            # only increment my mankalah
            if current_side != agent_side and cur_hole == MANKALAH:
                cur_hole = (cur_hole + 1) % 8
                current_side = current_side.opposite()
                continue
            board_copy[current_side.value][cur_hole] += 1
            if cur_hole > 6:
                current_side = current_side.opposite()
            cur_hole = (cur_hole + 1) % 8
            seeds -= 1

        return board_copy

    def __repr__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class BasicStrategy(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def get_move(self):
        board_side = self.agent.game[self.agent.side.value]
        for i in range(MANKALAH - 1, -1, -1):
            if board_side[i] > 0:
                return i + 1

    def __repr__(self):
        return "Basic Strategy"

    def __str__(self):
        return "Basic Strategy"

class MiniMaxDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def __repr__(self):
        return "Minimax Engine"

    def __str__(self):
        return "Minimax Engine"

    def get_move(self):
        move, reward = self.max_min(self.agent.game.board, 4)
        return move + 1

    def min_max(self, board, remaining_depth=3):
        # if the sum of all holes - mankalah is 0 game over
        if sum(board[self.agent.side.opposite().value][:MANKALAH]) == 0:
            return -1, self.game_score(board, self.agent.side.opposite())

        # shitty depth control to prevent death of CPU
        if remaining_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        best_r = 1
        best_hole = -1
        for i, hole in enumerate(board[self.agent.side.opposite().value][:MANKALAH]):
            # if Opponent can play then play
            if hole > 0:
                board_copy = deepcopy(board)
                self.play_hole(i, board_copy, self.agent.side.opposite())
                # back to our go
                _, reward = self.max_min(board_copy, remaining_depth - 1)

                # minimize the reward
                if best_hole == -1 or reward > best_r:
                    best_hole = i
                    best_r = reward
        return best_hole, best_r

    def max_min(self, board, remaining_depth=3):
        # if the sum of all holes - mankalah is 0 game over
        if sum(board[self.agent.side.value][:MANKALAH]) == 0:
            return -1, self.game_score(board, self.agent.side)

        # shitty depth control to prevent death of CPU
        if remaining_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # else we traverse game tree
        best_r = -1
        best_hole = -1
        # for each hole on my side
        for i, hole in enumerate(board[self.agent.side.value][:MANKALAH]):
            # if I can play that hole
            # play it and then let my opponent play
            if hole > 0:
                board_copy = deepcopy(board)
                self.play_hole(i, board_copy, self.agent.side)
                _, reward = self.min_max(board_copy, remaining_depth - 1)
                # maximize the reward
                if best_hole == -1 or reward > best_r:
                    best_hole = i
                    best_r = reward

        return best_hole, best_r
