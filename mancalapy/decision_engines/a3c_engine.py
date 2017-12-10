from decision_engines import DecisionEngine
from decision_engines.a3c_research.a3c_model import ActorCriticNetwork
import numpy as np


class A3CDecisionEngine(DecisionEngine):
    def __init__(self, agent):
        super().__init__(agent)
        self.model = ActorCriticNetwork(param_file="best-weights")

    @staticmethod
    def flatten_game(game_board, side):
        """
        Flatten the game board and concatenate the side
        and return a new numpy array with the side on the end

        :param side:
        :param game_board:
        :return:
        """
        return np.expand_dims(np.concatenate((game_board.flatten(), [side.value])), axis=0)

    def get_move(self, game=None) -> int:
        game = game if game is not None else self.agent.board
        _, actor_output = self.model(self.flatten_game(game, self.agent.side))
        actor_output = np.squeeze(actor_output)
        legal_moves = self.get_legal_moves(game, self.agent.side)
        legal_set = set(legal_moves)
        actor_output = [prob if i in legal_set else 0 for i, prob in enumerate(actor_output)]
        actor_output /= sum(actor_output)
        mv = np.random.choice(np.arange(7), p=actor_output)
        return int(mv) + 1

    def __str__(self):
        return "AC3 Engine"

    def __repr__(self):
        return "AC3 Engine"
