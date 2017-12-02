from cydecision_engines.cmonte_carlo import MonteCarlo

class CyDecisionEngineFactory:
    def __init__(self, agent):
        self.agent = agent
        self.engines = {
            "monte_carlo": MonteCarlo(self.agent)
        }

    def __getitem__(self, item):
        return self.engines[item]