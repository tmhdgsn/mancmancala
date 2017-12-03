import numpy as np

from side import Side
from decision_engines.decision_engine import DecisionEngine
from decision_engines.a3c_engine import AC3DecisionEngine


def reset():
    return np.array([7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0, 1])


def score(init_game_state, new_state):
    """
    Returns the change in mankalah given a move
    :param init_game_state:
    :param new_state:
    :return:
    """
    # init_side
    if init_game_state[-1] == 1:
        return init_game_state[15] - new_state[15]
    return init_game_state[7] - new_state[7]


def step(init_game_state, action):
    """
    Takes a game state transforms it into a format that playhole
    can understand, executes playhole then returns the next game state,
    reward and whether or not the game is over
    :param init_game_state:
    :param action:
    :return:
    """

    # last index is side
    side = Side(init_game_state[-1])
    board = np.reshape(init_game_state[:-1], (2, 8))
    repeat_go = DecisionEngine.play_hole(action, board, side)
    side = side if repeat_go else side.opposite()
    new_state = AC3DecisionEngine.flatten_game(board, side)

    # calculate reward
    reward = score(init_game_state, new_state)

    # game_over
    game_over = DecisionEngine.game_over(board)

    return new_state, reward, game_over