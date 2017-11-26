import numpy as np
cimport numpy as np
import sys

from cydecision_engines.cydecision_engine import CyDecisionEngine
from cygame import mk_board
from cyside import Side, opposite

cdef class Agent:
    cdef np.ndarray board
    cdef int side
    cdef CyDecisionEngine engine
    def __init__(self, CyDecisionEngine engine):
        self.board = mk_board(7, 7)
        self.side = Side.SOUTH
        self.engine = engine


    @classmethod
    def get_msg(cls):
        from_engine = input().strip()
        args = from_engine.split(";")
        return args[0], args[1:]


    @classmethod
    def send_msg(cls, msg):
        print(msg)

    cdef update_board(self, str raw_state):
        cdef str board_state = raw_state.split(",")
        self.board[Side.NORTH] = np.array(list(map(int, board_state[:8])))
        self.board[Side.SOUTH.value] = np.array(list(map(int, board_state[8:])))

    cdef play(self):
        our_turn = False
        while True:
            msg_type, args = self.get_msg()
            if msg_type.upper() == "START":
                    if args[0].upper() == "SOUTH":
                        self.side = Side.SOUTH
                        our_turn = True
                    else:
                        self.side = Side.NORTH
            if msg_type.upper() == "END":
                break
            if msg_type.upper() == "CHANGE":
                our_turn = args[-1].upper() == "YOU"
                self.update_board(args[-2])
                if args[0].upper() == "SWAP":
                    self.side = opposite(self.side)
            if our_turn:
                move = self.engine.get_move()
                self.send_msg(f"MOVE;{move}")


if __name__ == '__main__':
    agent = Agent("ab_minimax")
    if len(sys.argv) > 1:
        if sys.argv[1] in agent.factory.engines:
            agent = Agent(sys.argv[1])
    agent.play()
