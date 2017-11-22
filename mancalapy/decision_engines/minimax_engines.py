from .decision_engine import DecisionEngine
from copy import deepcopy


class MiniMaxDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def __repr__(self):
        return "Minimax Engine"

    def __str__(self):
        return "Minimax Engine"

    def get_move(self):
        move, reward = self.max_min(self.agent.game, max_depth=6)
        return move + 1

    def min_max(self, board, max_depth=3):
        # if the sum of all holes - mankalah is 0 game over
        if sum(board[self.agent.side.opposite().value][:self.MANKALAH]) == 0:
            return -1, self.game_score(board, self.agent.side.opposite())

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        best_r = 1
        best_hole = -1
        for i, hole in enumerate(board[self.agent.side.opposite().value][:self.MANKALAH]):
            # if Opponent can play then play
            if hole > 0:
                board_copy = deepcopy(board)
                repeat = self.play_hole(i, board_copy, self.agent.side.opposite())
                _, reward = self.min_max(board_copy, max_depth - 1) \
                    if repeat else self.max_min(board_copy, max_depth - 1)

                # minimize the reward
                if best_hole == -1 or reward > best_r:
                    best_hole = i
                    best_r = reward
        return best_hole, best_r

    def max_min(self, board, max_depth=3):
        # if the sum of all holes - mankalah is 0 game over
        if sum(board[self.agent.side.value][:self.MANKALAH]) == 0:
            return -1, self.game_score(board, self.agent.side)

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # else we traverse game tree
        best_r = -1
        best_hole = -1
        # for each hole on my side
        for i, hole in enumerate(board[self.agent.side.value][:self.MANKALAH]):
            # if I can play that hole
            # play it and then let my opponent play
            if hole > 0:
                board_copy = deepcopy(board)
                repeat = self.play_hole(i, board_copy, self.agent.side)
                _, reward = self.max_min(board_copy, max_depth - 1) \
                    if repeat else self.min_max(board_copy, max_depth - 1)
                # maximize the reward
                if best_hole == -1 or reward > best_r:
                    best_hole = i
                    best_r = reward
        return best_hole, best_r


class AlphaBetaMiniMaxDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def __repr__(self):
        return "Minimax Engine"

    def __str__(self):
        return "Minimax Engine"

    def get_move(self):
        move, reward = self.max_min(self.agent.game, alpha=-50, beta=50, max_depth=6)
        return move + 1

    def min_max(self, board, alpha, beta, max_depth=3):
        # if the sum of all holes - mankalah is 0 game over
        if sum(board[self.agent.side.opposite().value][:self.MANKALAH]) == 0:
            return -1, self.game_score(board, self.agent.side.opposite())

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        best_r = 1
        best_hole = -1
        for i, hole in enumerate(board[self.agent.side.opposite().value][:self.MANKALAH]):
            # if Opponent can play then play
            if hole > 0:
                board_copy = deepcopy(board)
                self.play_hole(i, board_copy, self.agent.side.opposite())
                # back to our go
                _, reward = self.max_min(board_copy, alpha, beta, max_depth - 1)

                # minimize the reward
                if best_hole == -1 or reward > best_r:
                    best_hole = i
                    best_r = reward
                beta = min(beta, best_r)
                if best_r <= alpha:
                    return best_hole, best_r
        return best_hole, best_r

    def max_min(self, board, alpha, beta, max_depth=3):
        # if the sum of all holes - mankalah is 0 game over
        if sum(board[self.agent.side.value][:self.MANKALAH]) == 0:
            return -1, self.game_score(board, self.agent.side)

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # else we traverse game tree
        best_r = -1
        best_hole = -1
        # for each hole on my side
        for i, hole in enumerate(board[self.agent.side.value][:self.MANKALAH]):
            # if I can play that hole
            # play it and then let my opponent play
            if hole > 0:
                board_copy = deepcopy(board)
                self.play_hole(i, board_copy, self.agent.side)
                _, reward = self.min_max(board_copy, alpha, beta, max_depth - 1)
                # maximize the reward
                if best_hole == -1 or reward > best_r:
                    best_hole = i
                    best_r = reward
                alpha = min(alpha, best_r)
                if best_r >= beta:
                    return best_hole, best_r
        return best_hole, best_r
