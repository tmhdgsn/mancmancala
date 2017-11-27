from copy import deepcopy

from side import Side
from .decision_engine import DecisionEngine


class MiniMaxDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)
        self.depth = 7

    def __repr__(self):
        return "Minimax Engine"

    def __str__(self):
        return "Minimax Engine"

    def get_move(self, game=None, depth=None):
        game = game if game else self.agent.game
        depth = depth if depth else self.depth
        move, reward = self.max_min(game, max_depth=depth, agent_has_moved=self.agent.has_moved)
        return move

    def min_max(self, board, max_depth=3, agent_has_moved=True):
        # if the sum of all holes - mankalah is 0 game over
        if self.game_over(board):
            return -1, self.game_score(board)

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # initialize best reward and best play
        best_r = float("inf")
        best_move = -1

        # see if we can get a better result if we swap
        if not agent_has_moved and self.agent.side == Side.SOUTH:
            # recurse with swapped side
            self.agent.side = Side.NORTH
            board_copy = deepcopy(board)
            _, reward = self.max_min(board_copy, max_depth - 1)
            self.agent.side = Side.SOUTH
            best_r = reward
            best_move = "SWAP"

        for i, hole in enumerate(board[self.agent.side.opposite().value][:self.MANKALAH]):
            # if Opponent can play then play
            if hole > 0:
                board_copy = deepcopy(board)
                repeat = self.play_hole(i, board_copy, self.agent.side.opposite()) and \
                        (agent_has_moved and self.agent.side == Side.SOUTH or self.agent.side == Side.NORTH)
                _, reward = self.min_max(board_copy, max_depth - 1) \
                    if repeat else self.max_min(board_copy, max_depth - 1)

                # minimize the reward
                if best_move == -1 or reward < best_r:
                    best_move = i + 1
                    best_r = reward

        return best_move, best_r

    def max_min(self, board, max_depth=3, agent_has_moved=True):
        # if the sum of all holes - mankalah is 0 game over
        if self.game_over(board):
            return -1, self.game_score(board)

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # initialize best reward and best play
        best_r = -float('inf')
        best_play = -1

        # see if we can get a better result if we swap
        if not agent_has_moved and self.agent.side == Side.NORTH:
            # recurse with swapped side
            self.agent.side = Side.SOUTH
            board_copy = deepcopy(board)
            _, reward = self.min_max(board_copy, max_depth - 1)
            self.agent.side = Side.NORTH
            best_r = reward
            best_play = "SWAP"

        # for each hole on my side
        for i, hole in enumerate(board[self.agent.side.value][:self.MANKALAH]):
            # if I can play that hole
            # play it and then let my opponent play
            if hole > 0:
                board_copy = deepcopy(board)
                repeat = self.play_hole(i, board_copy, self.agent.side) and \
                         (agent_has_moved and self.agent.side == Side.SOUTH or self.agent.side == Side.NORTH)
                _, reward = self.max_min(board_copy, max_depth - 1) \
                    if repeat else self.min_max(board_copy, max_depth - 1, agent_has_moved)
                # maximize the reward
                if best_play == -1 or reward > best_r:
                    best_play = i + 1
                    best_r = reward
        return best_play, best_r


class AlphaBetaMiniMaxDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)
        self.depth = 7

    def __repr__(self):
        return "AlphaBetaMinimax Engine"

    def __str__(self):
        return "AlphaBetaMinimax Engine"

    def get_move(self, game=None, depth=None):
        game = game if game else self.agent.game
        depth = depth if depth else self.depth
        move, reward = self.max_min(game, alpha=-float('inf'), beta=float('inf'), max_depth=depth,
                                    agent_has_moved=self.agent.has_moved)
        return move

    def min_max(self, board, alpha, beta, max_depth=3, agent_has_moved=True):
        # if the sum of all holes - mankalah is 0 game over
        if self.game_over(board):
            return -1, self.game_score(board)

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # initialize best reward and best play
        best_r = float('inf')
        best_play = -1

        # see if we can get a better result if we swap
        if not agent_has_moved and self.agent.side == Side.SOUTH:
            # recurse with swapped side
            board_copy = deepcopy(board)
            self.agent.side = Side.NORTH
            _, reward = self.max_min(board_copy, alpha, beta, max_depth - 1)
            self.agent.side = Side.SOUTH
            best_r = reward
            beta = min(beta, best_r)
            best_play = "SWAP"

        for i, hole in enumerate(board[self.agent.side.opposite().value][:self.MANKALAH]):
            # if Opponent can play then play
            if hole > 0:
                # copy board and play move
                board_copy = deepcopy(board)
                repeat = self.play_hole(i, board_copy, self.agent.side.opposite()) and \
                         (agent_has_moved and self.agent.side == Side.SOUTH or self.agent.side == Side.NORTH)
                _, reward = self.min_max(board_copy, alpha, beta, max_depth - 1) \
                    if repeat else self.max_min(board_copy, alpha, beta, max_depth - 1)

                # minimize the reward
                if best_play == -1 or reward < best_r:
                    best_play = i + 1
                    best_r = reward
                beta = min(beta, best_r)
                if best_r <= alpha:
                    return best_play, best_r
        return best_play, best_r

    def max_min(self, board, alpha, beta, max_depth=3, agent_has_moved=True):
        # if the sum of all holes - mankalah is 0 game over
        if self.game_over(board):
            return -1, self.game_score(board)

        # shitty depth control to prevent death of CPU
        if max_depth == 0:
            return -1, self.intermediate_score(board, self.agent.side)

        # initialize best reward and best play
        best_r = -float('inf')
        best_play = -1

        # see if we can get a better result by swapping as first move
        if not agent_has_moved and self.agent.side == Side.NORTH:
            board_copy = deepcopy(board)
            # recurse with swapped side
            self.agent.side = Side.SOUTH
            _, reward = self.min_max(board_copy, alpha, beta, max_depth - 1)
            self.agent.side = Side.NORTH
            best_r = reward
            best_play = "SWAP"
            alpha = max(alpha, best_r)

        # for each hole on my side
        for i, hole in enumerate(board[self.agent.side.value][:self.MANKALAH]):
            # if I can play that hole
            # play it and then let my opponent play
            if hole > 0:
                # copy board and make move
                board_copy = deepcopy(board)
                repeat = self.play_hole(i, board_copy, self.agent.side) and \
                         (agent_has_moved and self.agent.side == Side.SOUTH or self.agent.side == Side.NORTH)
                _, reward = self.max_min(board_copy, alpha, beta, max_depth - 1) \
                    if repeat else self.min_max(board_copy, alpha, beta, max_depth - 1, agent_has_moved)

                # maximize the reward
                if best_play == -1 or reward > best_r:
                    best_play = i + 1
                    best_r = reward
                alpha = max(alpha, best_r)
                if best_r >= beta:
                    return best_play, best_r
        return best_play, best_r
