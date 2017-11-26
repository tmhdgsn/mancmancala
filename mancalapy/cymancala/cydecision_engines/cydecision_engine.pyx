import numpy as np
cimport numpy as np
from cyagent import Agent
from cyside import Side, opposite

cdef enum:
    MANCALA = 7

cdef class CyDecisionEngine:
    cdef Agent agent

    def __init__(self, Agent agent):
        self.agent = agent

    @classmethod
    cdef int game_over(cls, np.ndarray board):
        if np.sum(board[Side.NORTH][:-1]) == 0 or np.sum(board[Side.SOUTH][:-1]) == 0:
            return 1
        else:
            return 0


    @classmethod
    cdef int game_score(cls, np.ndarray board):
        cdef int opponent = np.sum(board[Side.NORTH])
        cdef int agent = np.sum(board[Side.SOUTH])
        return agent - opponent

    @classmethod
    cdef int play_hole(cls, int hole, np.ndarray board_copy, int agent_side):
        cdef int seeds = board_copy[agent_side][hole]
        board_copy[agent_side][hole] = 0
        cdef int cur_hole = hole + 1
        cdef int current_side = agent_side

        while seeds > 1:
            if current_side != agent_side and cur_hole == MANCALA:
                cur_hole = (cur_hole + 1) % 8
                current_side = opposite(current_side)
                continue
            board_copy[current_side][cur_hole] += 1
            if cur_hole > 6:
                current_side = opposite(current_side)
            cur_hole = (cur_hole + 1) % 8
            seeds -= 1

        cdef int opposite_hole = MANCALA - 1 -hole

        # check if we can capture opponent pieces
        if cur_hole != MANCALA and current_side == agent_side and board_copy[current_side][cur_hole] == 0 and \
                        board_copy[opposite(current_side)][opposite_hole] > 0:
            cdef int captured_seeds = board_copy[opposite(current_side)][opposite_hole]
            board_copy[opposite(current_side)][opposite_hole] = 0
            board_copy[current_side][MANCALA] += captured_seeds + 1
            return 0

        board_copy[current_side][cur_hole] += 1
        if current_side == agent_side and cur_hole == MANCALA:
            return 1
        else:
            return 0

    @classmethod
    def get_move(cls):
        pass
