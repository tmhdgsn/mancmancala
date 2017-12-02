from cydecision_engine import CyDecisionEngine
from cyagent import Agent
from datetime import datetime, timedelta
import numpy as np
cimport numpy as np
from copy import deepcopy
import random
import math

cdef enum:
    MANCALA = 7

cdef class MonteCarlo(CyDecisionEngine):
    cdef int max_moves
    cdef int max_depth

    def __init__(self, Agent agent):
        super().__init__(agent)
        self.plays = {}
        self.wins = {}
        self.calc_timeout = timedelta(seconds=3)
        self.max_moves = 100
        self.max_depth = 0
        self.C = math.sqrt(2)


    def __repr__(self):
        return "Monte Carlo Engine"

    def __str__(self):
        return "Monte Carlo Engine"

    cdef np.ndarray get_legal_moves(self, np.ndarray board, int side):
        return board[side][:MANCALA].nonzero()[0]

    cdef int get_move(self):
        cdef int sim_count = 0
        begin = datetime.utcnow()

        cdef np.ndarray init_state = self.agent.board

        while datetime.utcnow() - begin < self.calc_timeout:
            self.run_simulation(init_state)
            sim_count += 1

        cdef np.ndarray legal_moves = self.get_legal_moves(self.agent.game, self.agent.side)
        cdef np.ndarray move_states = self.get_move_states(self.agent.game, legal_moves, self.agent.side)
        return self.get_best_move(self.agent.side, move_states)

    cdef run_simulation(self, init_state):
        expand = True
        visited_states = dict()
        cdef np.ndarray state = init_state
        for m in range(self.max_moves + 1):
            cdef np.ndarray legal = self.get_legal_moves(state, self.agent.side)
            move_states = self.get_move_states
            if all(self.plays.get((side, self.hash(state))) for _, state, side in move_states):
                log_total = math.log(sum(self.plays[(side, self.hash(state))] for _, state, side in move_states))
                bound_plays = [
                    (self.ucb_value(side, log_total, state), move_idx, self.hash(state)) for move_idx, state, side in
                    move_states
                ]
                _, move_idx, state = max(bound_plays)

        else:
            # Make random choice if no states given
            _, state, side = random.choice(move_states)

            visited_states[self.hash(state)] = state
            if expand and not self.hash(state) in self.plays:
                expand = False
                self.plays[self.hash(state)] = 0
                self.wins[self.hash(state)] = 0

                if m > self.max_depth:
                    self.max_depth = m

            if self.game_over(state):
                break
        for state_hash, state in visited_states.items():
            if state_hash in self.plays:
                self.plays[state_hash] += 1
                self.wins[state_hash] = self.game_score(state)

    cdef get_move_states(self, board, legal_moves, side):
            moves_states = []
            for move_idx in legal_moves:
                board_copy = deepcopy(board)
                our_turn = self.play_hole(move_idx, board_copy, side)
                new_side = side if our_turn else side.opposite()
                moves_states.append((move_idx, board_copy, new_side))
            return moves_states

    cdef get_best_move(self, player, moves_states):
        stats = [
            (self.wins.get((player, self.hash(state)), 0) / self.plays.get((player, self.hash(state)), 1), move_idx)
            for move_idx, state, _ in moves_states]
        _, best_move = max(stats, key=lambda x: x[0])

        return best_move + 1

    def ucb_value(self, side, log_total, state):
        exploration = self.wins.get(self.hash(state), 0) / self.plays.get(self.hash(state), 1)
        exploitation = self.C * math.sqrt(log_total / self.plays[(side, self.hash(state))])
        return (exploitation + exploration) * (1 if side == self.agent.side else -1)

    def hash(self, state):
        pass

