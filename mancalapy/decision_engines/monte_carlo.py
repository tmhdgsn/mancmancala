import math
import random
from datetime import datetime
from .decision_engine import DecisionEngine

class MonteCarloDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)

    def __repr__(self):
        return "Monte Carlo Engine"

    def __str__(self):
        return "Monte Carlo Engine"

    def initialize_mc(self, game, states=[], **kwargs):
        """
        Takes an instance of the Game and some states to which the rewards
        and how many times the node gets visited is appended.

        :param: game: instance of the Kalah Game.
        :param: states: data structure for preserving history, rewards.
        :param: kwargs: For additional parameters
        """
        self.game = game
        self.states = states

        # Time taken for the calculation to happen - timeout for calculation
        # TODO: Could be reduced
        self.calc_timeout = timedelta(seconds=kwargs.get('time', 30))
        # Number of moves to be done while simulating till the END
        self.max_moves = kwargs.get('moves', 100)
        # Keep track of wins and play for each state run during simulation
        self.wins = {}
        self.plays = {}
        # Constant which is empirically correct to be root of 2
        self.C = math.sqrt(2)

    def update(self, state):
        """
        Once a game state has been played, and appends it to the tree/history.

        :param: state: current state of the game
        """
        self.states.append(state)

    def get_best_move(self):
        """
        Calculates the best move from the current game state and returns it.
        """
        # TODO:
        self.max_depth = 0
        state, player = self.states[-1], self.states[-1]
        legal_moves_by_index = self.game.get_legal_moves(self.states[:])

        # Check for the legal moves if it is None, return, return 1 if there is one
        if not legal_moves_by_index:
            return
        if len(legal_moves_by_index) == 1:
            return legal_move[0]

        # Get all the possible move states from the current state
        moves_states = [
            (p, self.game.next_state(state, p)) for p in legal_moves_by_index
        ]
        percentage_wins, best_move = max(
            (self.wins.get((player, S), 0) / self.plays.get((player, S), 1), p)
            for p, S in moves_states
        )
        
        games = 0
        begin = datetime.utcnow()
        while datetime.utcnow() - begin < self.calc_timeout:
            self.run_simulation()
            games += 1

        return best_move

    def run_simulation(self):
        """
        Samples a random move and plays the game out from that position, then
        updats the table with the rewards.
        """
        expand = True
        visited_states = set()
        states_copy = self.states[:]
        # Since we don't want to change the main one
        state, currently_player_at = states_copy[-1], states_copy[-1]

        for t in xrange(self.max_moves + 1):
            # Needs to take a the last game state and should return the list
            # of legal moves the players
            legal_moves_by_index = self.game.get_legal_moves(states_copy)
            # Returns the new game state by applying any of the next possible moves
            moves_states = [
                (p, self.game.next_state(state, p)) for p in legal_moves_by_index
            ]

            # Apply the UCB formula to check which state needs to be picked
            # for simulation
            # Formula is v + sqrt(ln N / n)
            # v is the mean reward for the node, 'N' is the number of times
            # parent node was visited and 'n' is the number of times the
            # current node is visited.
            if all(self.plays.get((player, S)) for p, S in moves_states):
                log_total = log(
                    sum(self.plays[(player, S)] for p, S in moves_states))
                value, next_move, state = max(
                    ((self.wins[(player, S)] / self.plays[(player, S)]) +
                     self.C * sqrt(log_total / self.plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Make random choice if no states given
                next_move, state = random.choice(moves_states)

            states_copy.append(state)

            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            # Update the state of the player with the above state
            player = states_copy[-1]

            # Check if the game has been won (1) or drawn (-1) or still(0) ongoing
            winner = self.game.winner(states_copy)
            if winner:
                break

        # So we update the plays and the wins depending upon whether it has won or not
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] += 1
