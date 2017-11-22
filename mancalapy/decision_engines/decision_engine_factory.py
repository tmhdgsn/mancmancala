from decision_engines import BasicStrategy
from decision_engines.minimax_engines import (
    MiniMaxDecisionEngine, AlphaBetaMiniMaxDecisionEngine
)
from decision_engines.monte_carlo import MonteCarloDecisionEngine


class DecisionEngineFactory:
    def __init__(self, agent):
        self.agent = agent

        self.engines = {
            "basic": BasicStrategy(self.agent),
            "minimax": MiniMaxDecisionEngine(self.agent),
            "ab_minimax": AlphaBetaMiniMaxDecisionEngine(self.agent),
            "monte_carlo": MonteCarloDecisionEngine(self.agent)
        }

    def __getitem__(self, item):
        return self.engines[item]

