from cyagent import Agent

cdef class CyDecisionEngine:
    cdef Agent agent
    def __init__(self, Agent agent):
        self.agent = agent
        self.engines = {
            "basic": BasicStrategy(self.agent),
        }