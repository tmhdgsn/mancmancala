import math
import random
from datetime import datetime, timedelta

from copy import deepcopy

from .decision_engine import DecisionEngine


class MonteCarloDecisionEngine(DecisionEngine):
    def __init__(self, agent, states=None, **kwargs):
        """
        Takes an agent and some states from which the rewards and node visitation count is appended.
        :param agent:
        :param: states: data structure for preserving history, rewards.
        :param kwargs:
        """
        super().__init__(agent)
        # Keep track of wins and play for each state run during simulation
        self.plays = {}
        self.wins = {}

        self.max_depth = 0
        self.states = states
        self.current_state = states[0]
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
        self.calc_timeout = timedelta(seconds=kwargs.get('time', 30))

        # Number of moves to be done while simulating till the END
        self.max_moves = kwargs.get('moves', 100)
        # Constant which is empirically correct to be root of 2
        self.C = kwargs.get('C', math.sqrt(2))

    def get_move(self, game=None, first=False):
        """
        Calculates the best move from the current game state and returns it.
        """
        state, player = self.current_state[self.agent.side.value], self.current_state[self.agent.side.value]
        legal_moves_by_index = self.get_legal_moves()

        # Check for the legal moves if it is None, return, return 1 if there is one
        if not len(legal_moves_by_index):
            return
        if len(legal_moves_by_index) == 1:
            return legal_moves_by_index[0]

        # Get all the possible move states from the current state
        moves_states = []
        state_copy = deepcopy(self.current_state)

        for move in legal_moves_by_index:
            our_move = self.play_hole(move, state_copy, self.agent.side.value)
            moves_states.append(state_copy)
            state_copy = deepcopy(self.current_state)

        _, best_move = max(
            (self.wins.get((player, S), 0) / self.plays.get((player, S), 1), p)
            for p, S in moves_states
        )
        
        simulation_count = 0
        begin = datetime.utcnow()
        while datetime.utcnow() - begin < self.calc_timeout:
            self.run_simulation()
            simulation_count += 1

        return best_move

    def get_legal_moves(self):
        return self.agent.game.board[self.agent.side.value].nonzero()[0]

    def run_simulation(self):
        """
        Samples a random move and plays the game out from that position, then
        updates the table with the rewards.
        """
        expand = True
        visited_states = set()
        # Since we don't want to change the main one
        state_copy = deepcopy(self.current_state)
        state, player = state_copy[self.agent.side.value], state_copy[self.agent.side.value]

        for t in range(self.max_moves + 1):
            # Needs to take a the last game state and should return the list
            # of legal moves the players
            moves_states = []
            legal_moves_by_index = self.get_legal_moves()
            for move in legal_moves_by_index:
                moves_states.append(self.play_hole(move, state_copy, self.agent.side.value))
                state_copy = deepcopy(self.current_state)

            # Apply the UCB formula to check which state needs to be picked
            # for simulation
            # Formula is v + sqrt(ln N / n)
            # v is the mean reward for the node, 'N' is the number of times
            # parent node was visited and 'n' is the number of times the
            # current node is visited.
            if all(self.plays.get((player, S)) for p, S in moves_states):
                log_total = math.log(
                    sum(self.plays[(player, S)] for p, S in moves_states))
                value, next_move, state = max(
                    ((self.wins[(player, S)] / self.plays[(player, S)]) +
                     self.C * math.sqrt(log_total / self.plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Make random choice if no states given
                next_move, state = random.choice(moves_states)

            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            # Update the state of the player with the above state
            player = state

            # Check if the game has been won (1) or drawn (-1) or still(0) ongoing
            winner = state
            if winner:
                break

        # So we update the plays and the wins depending upon whether it has won or not
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] += 1
