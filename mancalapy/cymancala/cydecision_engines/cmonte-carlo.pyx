import cygame
from cydecision_engine import CyDecisionEngine
from cyagent import Agent

cdef class MonteCarlo(CyDecisionEngine):
    def __init__(self, Agent agent):
        super().__init__(agent)
