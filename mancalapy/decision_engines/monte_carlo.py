import math
import random
import numpy as np
from datetime import datetime, timedelta

import game
from game import Game
from side import Side
from copy import deepcopy

from .decision_engine import DecisionEngine


class MonteCarloDecisionEngine(DecisionEngine):
    def __init__(self, agent, **kwargs):
        """
        Takes an agent and some states from which the rewards and node visitation count is appended.
        :param agent:
        :param kwargs:
        """
        super().__init__(agent)
        # Keep track of wins and play for each state run during simulation
        self.plays = {}
        self.wins = {}
        self.initialize_mc(**kwargs)

    def __repr__(self):
        return "Monte Carlo Engine"

    def __str__(self):
        return "Monte Carlo Engine"

    def initialize_mc(self, **kwargs):
        """
        :param: kwargs: For additional parameters
        """
        # Time taken for the calculation to happen - timeout for calculation
        # TODO: Could be reduced
        self.calc_timeout = timedelta(seconds=kwargs.get('time', 1))

        # Number of moves to be done while simulating till the END
        self.max_moves = kwargs.get('moves', 100)
        # Constant which is empirically correct to be root of 2
        self.C = kwargs.get('C', math.sqrt(2))

    def get_legal_moves(self, board, side):
        return board[side.value][:self.MANKALAH].nonzero()[0]

    def get_move(self, game=None, first=False):
        self.max_depth = 0
        simulation_count = 0
        begin = datetime.utcnow()

        # This allows for us to isolate get_move for testing a given game state
        init_state = game.board if game else self.agent.game.board

        while datetime.utcnow() - begin < self.calc_timeout:
            self.run_simulation(init_state=init_state)
            simulation_count += 1

        legal_moves_by_index = self.get_legal_moves(self.agent.game.board, self.agent.side)

        # Check for the legal moves if it is None, return, return 1 if there is one
        if not len(legal_moves_by_index):
            return
        if len(legal_moves_by_index) == 1:
            return legal_moves_by_index[0]

        # Get all the possible move states from the current state
        moves_states = self.get_move_states(self.agent.game.board, legal_moves_by_index, self.agent.side)
        return self.get_best_move(self.agent.side, moves_states)

    def get_best_move(self, player, moves_states):
        stats = [
            (self.wins.get((player, hash(str(state))), 0) / self.plays.get((player, hash(str(state))), 1), move_idx)
            for move_idx, state, _ in moves_states]
        _, best_move = max(stats, key=lambda x: x[0])

        return best_move + 1

    def get_move_states(self, board, legal_moves, side):
        moves_states = []
        for move_idx in legal_moves:
            board_copy = deepcopy(board)
            ourTurn = self.play_hole(move_idx, board_copy, side)
            new_side = side if ourTurn else side.opposite()
            moves_states.append((move_idx, board_copy, new_side))
        return moves_states

    def ucb_value(self, side, log_total, state):
        exploration = self.wins.get(hash(str(state)), 0) / self.plays.get(hash(str(state)), 1)
        exploitation = self.C * math.sqrt(log_total / self.plays[(side, hash(str(state)))])
        return (exploitation + exploration) * (1 if side == self.agent.side else -1)

    def run_simulation(self, init_state):
        """
        Samples a random move and plays the game out from that position, then
        updates the table with the rewards.
        """
        expand = True
        visited_states = dict()
        state = init_state
        for m in range(self.max_moves + 1):
            legal = self.get_legal_moves(board=state, side=self.agent.side)
            moves_states = self.get_move_states(board=state, legal_moves=legal, side=self.agent.side)

            if all(self.plays.get((side, hash(str(state)))) for _, state, side in moves_states):
                log_total = math.log(sum(self.plays[(side, hash(str(state)))] for _, state, side in moves_states))
                bound_plays = [
                    (self.ucb_value(log_total, state), move_idx, hash(str(state))) for move_idx, state, side in moves_states
                ]
                _, move_idx, state = max(bound_plays)

            else:
                # Make random choice if no states given
                _, state, side = random.choice(moves_states)

            visited_states[hash(str(state))] = state
            if expand and not hash(str(state)) in self.plays:
                expand = False
                self.plays[hash(str(state))] = 0
                self.wins[hash(str(state))] = 0

                if m > self.max_depth:
                    self.max_depth = m

            if self.game_over(state):
                break
        for state_hash, state in visited_states.items():
            if state_hash in self.plays:
                self.plays[state_hash] += 1
                self.wins[state_hash] = self.game_score(state, self.agent.side)
