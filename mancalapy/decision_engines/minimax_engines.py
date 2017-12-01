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

    def get_move(self, game=None, depth=None) -> int:
        game = game if game else self.agent.game
        depth = depth if depth else self.depth
        move, reward = self.max_min(game, max_depth=depth, agent_has_moved=self.agent.has_moved)
        return move

    def min_max(self, board, max_depth=3, agent_has_moved=True) -> (int, float):
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
            _, reward = self.max_min(deepcopy(board), max_depth - 1)
            self.agent.side = Side.SOUTH
            best_r = reward
            best_move = -1

        for play in self.get_legal_moves(board, self.agent.side.opposite()):
            next_board, repeat = self.get_next_boards(agent_has_moved, self.agent.side.opposite(), board, play)
            _, reward = self.min_max(next_board, max_depth - 1) \
                if repeat else self.max_min(next_board, max_depth - 1)

            # minimize the reward
            if reward < best_r:
                best_move = play + 1
                best_r = reward

        return best_move, best_r

    def max_min(self, board, max_depth=3, agent_has_moved=True) -> (int, float):
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
            _, reward = self.min_max(deepcopy(board), max_depth - 1)
            self.agent.side = Side.NORTH
            best_r = reward
            best_play = -1

        # for each hole on my side
        for play in self.get_legal_moves(board, self.agent.side):
            next_board, repeat = self.get_next_boards(agent_has_moved, self.agent.side, board, play)
            _, reward = self.max_min(next_board, max_depth - 1) \
                if repeat else self.min_max(next_board, max_depth - 1, agent_has_moved)
            # maximize the reward
            if reward > best_r:
                best_play = play + 1
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

    def get_move(self, game=None, depth=None) -> int:
        game = game if game else self.agent.game
        depth = depth if depth else self.depth
        move, reward = self.max_min(game, alpha=-float('inf'), beta=float('inf'), max_depth=depth,
                                    agent_has_moved=self.agent.has_moved)
        return move

    def min_max(self, board, alpha, beta, max_depth=3, agent_has_moved=True) -> (int, float):
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
            self.agent.side = Side.NORTH
            _, reward = self.max_min(deepcopy(board), alpha, beta, max_depth - 1)
            self.agent.side = Side.SOUTH
            best_r = reward
            beta = min(beta, best_r)
            best_play = -1

        for play in self.get_legal_moves(board, self.agent.side.opposite()):
            # copy board and play move
            next_board, repeat = self.get_next_boards(agent_has_moved, self.agent.side.opposite(), board, play)
            _, reward = self.min_max(next_board, alpha, beta, max_depth - 1) \
                if repeat else self.max_min(next_board, alpha, beta, max_depth - 1)

            # minimize the reward
            if reward < best_r:
                best_play = play + 1
                best_r = reward
            beta = min(beta, best_r)
            if best_r <= alpha:
                return best_play, best_r
        return best_play, best_r

    def max_min(self, board, alpha, beta, max_depth=3, agent_has_moved=True) -> (int, float):
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
            # recurse with swapped side
            self.agent.side = Side.SOUTH
            _, reward = self.min_max(deepcopy(board), alpha, beta, max_depth - 1)
            self.agent.side = Side.NORTH
            best_r = reward
            alpha = max(alpha, best_r)
            best_play = -1

        # for each hole on my side
        for play in self.get_legal_moves(board, self.agent.side):
            next_board, repeat = self.get_next_boards(agent_has_moved, self.agent.side, board, play)
            _, reward = self.max_min(next_board, alpha, beta, max_depth - 1) \
                if repeat else self.min_max(next_board, alpha, beta, max_depth - 1, agent_has_moved)

            # maximize the reward
            if reward > best_r:
                best_play = play + 1
                best_r = reward
            alpha = max(alpha, best_r)
            if best_r >= beta:
                return best_play, best_r
        return best_play, best_r
