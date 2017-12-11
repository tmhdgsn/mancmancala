import math
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np

from .decision_engine import DecisionEngine


class MonteCarloDecisionEngine(DecisionEngine):
    def __init__(self, agent, **kwargs):
        """
        Takes an agent and some states from which the rewards and node visitation count is appended.
        :param agent:
        :param kwargs:
        """
        super().__init__(agent)
        # number of simulations to run from a given state
        self.max_sims = 1000
        # keep track of visits for each node and rewards they get
        self.visits = defaultdict(lambda: 0)
        self.scores = defaultdict(lambda: 0)

        # Time taken for the calculation to happen - timeout for calculation
        self.calc_timeout = timedelta(seconds=kwargs.get('time', 1))

        # Constant which is empirically correct to be root of 2
        self.C = kwargs.get('C', math.sqrt(2))

    def __repr__(self):
        return "Monte Carlo Engine"

    def __str__(self):
        return "Monte Carlo Engine"

    def get_move(self, game=None):
        simulation_count = 0
        begin = datetime.utcnow()

        # This allows for us to isolate get_move for testing a given game state
        init_state = game if game is not None else self.agent.board

        best_move = -1  # no move
        while datetime.utcnow() - begin < self.calc_timeout:
            best_move = self.mcts(init_state)
            simulation_count += 1
        return best_move + 1

    def ucb_value(self, side, ln_parent_visits, state):
        exploration = self.scores[(side, self.hash(state))] / self.visits[(side, self.hash(state))]
        exploitation = self.C * math.sqrt((2 * ln_parent_visits) / self.visits[(side, self.hash(state))])
        return exploitation + exploration

    def mcts(self, root):
        """
        Implements UCT algorithm as defined here: http://mcts.ai/pubs/mcts-survey-master.pdf

        IMPORTANT!!
        state = (move, side, board) or (side, board) depending on context
        :param root:
        :return:
        """
        for sim in range(self.max_sims):
            cur_side = self.agent.side
            state = root
            path = [(cur_side, self.hash(root))]  # records the path taken down the tree

            # select child, expanding unexpanded children
            move, side, child_board = self.select_child(cur_side, state)

            # add child to the path
            path.append((side, self.hash(child_board)))

            # run simulation from this state and backprop reward
            self.default_policy_backprop(side, child_board, path)

        return move

    def default_policy_backprop(self, side, board, path):
        """ runs simulation playing out game to leaf node from current state """
        while not self.game_over(board):
            random_move = np.random.choice(self.get_legal_moves(board, side))
            board, repeat = self.get_next_board(True, side, board, random_move)
            side = side if repeat else side.opposite()
            # add node to the path down the tree
            path.append((side, self.hash(board)))

        # model game as simple zero sum game
        # Possibly consider changing this to prioritise high scoring paths
        game_score = self.game_score(board)
        reward = game_score if game_score == 0 else game_score / abs(game_score)
        self.backpropagate_rewards(reward, path)

    def select_child(self, cur_side, board):
        """ selects a child node from the current state to play out """
        untried_moves = self.untried_moves(board, cur_side)
        if len(untried_moves) > 0:
            return self.expand(cur_side, board, untried_moves)

        return self.best_child(cur_side, board)

    def backpropagate_rewards(self, reward, path):
        for state_hash in reversed(path):
            # increment the visit
            self.visits[state_hash] += 1
            # increment the reward of this node
            self.scores[state_hash] += reward

    def expand(self, cur_side, board, untried_moves):
        # pick and play a random untried move
        move = np.random.choice(untried_moves)
        new_board, repeat_go = self.get_next_board(True, cur_side, board, move)
        side = cur_side if repeat_go else cur_side.opposite()
        return move, side, new_board

    def untried_moves(self, board, side):
        state_hash = (side, self.hash(board))
        played_moves = self.cache.get(state_hash, {})
        legal_moves = self.get_legal_moves(board, side)
        return [move for move in legal_moves if move not in played_moves]

    def best_child(self, cur_side, board):
        best_move = -1
        best_val = -float('inf')
        best_side = cur_side
        best_board = board
        log_visits = math.log(self.visits[(cur_side, self.hash(board))])
        for move in self.get_legal_moves(board, cur_side):
            child_board, repeat = self.get_next_board(True, cur_side, board, move)
            child_side = cur_side if repeat else cur_side.opposite()
            value = self.ucb_value(child_side, log_visits, child_board)
            if value > best_val:
                best_move, best_val, best_side, best_board = move, value, child_side, child_board
        return best_move, best_side, best_board
