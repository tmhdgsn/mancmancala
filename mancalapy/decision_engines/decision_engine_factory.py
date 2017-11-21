from decision_engines import BasicStrategy
from decision_engines.minimax_engines import MiniMaxDecisionEngine, AlphaBetaMiniMaxDecisionEngine


class DecisionEngineFactory:
    def __init__(self, agent):
        self.agent = agent

        self.engines = {
            "basic": BasicStrategy(self.agent),
            "minimax": MiniMaxDecisionEngine(self.agent),
            "ab_minimax": AlphaBetaMiniMaxDecisionEngine(self.agent),
        }

    def __getitem__(self, item):
        return self.engines[item]

