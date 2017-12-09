import math
import random
from copy import deepcopy
from datetime import datetime, timedelta

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

        # Time taken for the calculation to happen - timeout for calculation
        # TODO: Could be reduced
        self.calc_timeout = timedelta(seconds=kwargs.get('time', 3))

        # Number of moves to be done while simulating till the END
        self.max_moves = kwargs.get('moves', 300)
        # Constant which is empirically correct to be root of 2
        self.C = kwargs.get('C', math.sqrt(2))

        self.max_depth = 0

    def __repr__(self):
        return "Monte Carlo Engine"

    def __str__(self):
        return "Monte Carlo Engine"

    def get_move(self, board=None):
        simulation_count = 0
        begin = datetime.utcnow()

        # This allows for us to isolate get_move for testing a given game state
        init_state = board if board else self.agent.board

        while datetime.utcnow() - begin < self.calc_timeout:
            self.run_simulation(init_state=init_state)
            simulation_count += 1

        legal_moves_by_index = self.get_legal_moves(self.agent.board, self.agent.side)
        # Get all the possible move states from the current state
        moves_states = self.get_move_states(self.agent.board, legal_moves_by_index, self.agent.side)
        return self.get_best_move(self.agent.side, moves_states)

    def get_best_move(self, player, moves_states):
        stats = [
            (self.wins.get((player, self.hash(state)), 0) / self.plays.get((player, self.hash(state)), 1), move_idx)
            for move_idx, state, _ in moves_states]
        _, best_move = max(stats, key=lambda x: x[0])

        return best_move + 1

    def get_move_states(self, board, legal_moves, side):
        moves_states = []
        for move_idx in legal_moves:
            board_copy = deepcopy(board)
            our_turn = self.play_hole(move_idx, board_copy, side)
            new_side = side if our_turn else side.opposite()
            moves_states.append((move_idx, board_copy, new_side))
        return moves_states

    def ucb_value(self, side, log_total, state):
        exploration = self.wins.get(self.hash(state), 0) / self.plays.get(self.hash(state), 1)
        exploitation = self.C * math.sqrt(log_total / self.plays[(side, self.hash(state))])
        return (exploitation + exploration) * (1 if side == self.agent.side else -1)

    def run_simulation(self, init_state):
        """
        Samples a random move and plays the game out from that position, then
        updates the table with the rewards.
        """
        expand = True
        visited_states = dict()
        state = init_state
        current_side =  self.agent.side
        for m in range(self.max_moves + 1):
            legal = self.get_legal_moves(board=state, side=self.agent.side)
            moves_states = self.get_move_states(board=state, legal_moves=legal, side=self.agent.side)

            if all(self.plays.get((side, self.hash(future_state))) for _, future_state, side in moves_states):
                log_total = math.log(sum(self.plays[(side, self.hash(future_state))] for _, future_state, side in moves_states))
                bound_plays = [
                    (self.ucb_value(current_side, log_total, future_state), move_idx, self.hash(future_state)) for move_idx, future_state, _ in
                    moves_states
                ]
                _, move_idx, state = max(bound_plays)

            else:
                # Make random choice if no states given
                _, state, side = random.choice(moves_states)

            visited_states[self.hash(state)] = state
            if expand and not self.hash(state) in self.plays:
                expand = False
                self.plays[self.hash(state)] = 0
                self.wins[self.hash(state)] = 0

                if m > self.max_depth:
                    self.max_depth = m

            if self.game_over(state):
                break
        for state_hash, visited_state in visited_states.items():
            if state_hash in self.plays:
                self.plays[state_hash] += 1
                self.wins[state_hash] = self.game_score(visited_state)
