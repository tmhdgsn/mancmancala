import numpy as np
import pytest

from agent import Agent
from game import create_board
from side import Side


@pytest.fixture(scope="function")
def monte_mock_agent():
    return Agent("monte_carlo")


test_legal_moves = [
    (create_board(), Side.SOUTH, np.array([0, 1, 2, 3, 4, 5, 6])),
    (np.array([
        [1, 1, 2, 2, 2, 2, 1, 19],
        [1, 2, 1, 2, 0, 2, 0, 60]
    ], np.int32), Side.SOUTH, np.array([0, 1, 2, 3, 5]))
]

test_moves_states = [
    # (Game(), Side.SOUTH, np.array([
    #     np.array([[7, 7, 7, 7, 7, 7, 7, 0],
    #     [0, 8, 8, 8, 8, 8, 8, 1]]),
    #     np.array([[8, 7, 7, 7, 7, 7, 7, 0],
    #     [7, 0, 8, 8, 8, 8, 8, 1]]),
    #     np.array([[8, 8, 7, 7, 7, 7, 7, 0],
    #     [7, 7, 0, 8, 8, 8, 8, 1]]),
    #     np.array([[8, 8, 8, 7, 7, 7, 7, 0],
    #     [7, 7, 7, 0, 8, 8, 8, 1]]),
    #     np.array([[8, 8, 8, 8, 7, 7, 7, 0],
    #     [7, 7, 7, 7, 0, 8, 8, 1]]),
    #     np.array([[8, 8, 8, 8, 8, 7, 7, 0],
    #     [7, 7, 7, 7, 7, 0, 8, 1]]),
    #     np.array([[8, 8, 8, 8, 8, 8, 7, 0],
    #     [7, 7, 7, 7, 7, 7, 0, 1]])])),
    (np.array([
        [1, 1, 2, 2, 2, 2, 1, 19],
        [1, 2, 1, 2, 0, 2, 0, 60]
    ], np.int32), Side.SOUTH,
     [np.array([[1, 1, 2, 2, 2, 2, 1, 19],
                [0, 3, 1, 2, 0, 2, 0, 60]], dtype=np.int32),
      np.array([[1, 1, 2, 2, 2, 2, 1, 19],
                [1, 0, 2, 3, 0, 2, 0, 60]], dtype=np.int32),
      np.array([[1, 1, 2, 2, 2, 2, 1, 19],
                [1, 2, 0, 3, 0, 2, 0, 60]], dtype=np.int32),
      np.array([[1, 1, 2, 2, 2, 2, 1, 19],
                [1, 2, 1, 0, 1, 3, 0, 60]], dtype=np.int32),
      np.array([[1, 1, 2, 2, 2, 2, 1, 19],
                [1, 2, 1, 2, 0, 0, 1, 61]], dtype=np.int32)]
    )
]

test_best_moves = [
    (np.array([
        [1, 1, 2, 2, 2, 2, 1, 19],
        [1, 2, 1, 2, 0, 2, 0, 60]
    ], np.int32), Side.SOUTH, 1)
]


@pytest.mark.parametrize("board, side, expected_legal_moves", test_legal_moves)
def test_monte_carlo_get_legal_moves(monte_mock_agent, board, side, expected_legal_moves):
    pass


@pytest.mark.parametrize("game, side, expected_states", test_moves_states)
def test_monte_carlo_moves_states(monte_mock_agent, game, side, expected_states):
    pass


@pytest.mark.parametrize("game, side, expected_best_move", test_best_moves)
def test_monte_carlo_best_move(monte_mock_agent, game, side, expected_best_move):
    pass
