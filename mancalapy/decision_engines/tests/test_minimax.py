import numpy as np
import pytest

from agent import Agent
from game import Game
from side import Side

SWAP = -1


@pytest.fixture(scope="function")
def minimax_mock_agent():
    return Agent("minimax")


@pytest.fixture(scope="function")
def ab_minimax_mock_agent():
    return Agent("ab_minimax")


test_games = [
    # (Game(), Side.SOUTH, False, 1), # not sure what this should be yet
    (Game(board=np.array([
        [7, 7, 7, 7, 7, 7, 7, 0],
        [0, 8, 8, 8, 8, 8, 8, 1]
    ])), Side.NORTH, False, SWAP),
    (Game(board=np.array([
        [0, 0, 0, 0, 0, 2, 7, 18],
        [0, 20, 13, 13, 12, 12, 0, 1]
    ])), Side.NORTH, True, 7),
    (Game(board=np.array([
        [1, 1, 2, 2, 2, 2, 1, 19],
        [1, 2, 1, 2, 0, 2, 0, 60]
    ], np.int32)), Side.SOUTH, True, 6)
]


@pytest.mark.parametrize("game, side,has_moved, expected_move", test_games)
def test_minimax_agent_makes_correct_decision(minimax_mock_agent, game, side, has_moved, expected_move):
    minimax_mock_agent.side = side
    minimax_mock_agent.has_moved = has_moved
    assert expected_move == minimax_mock_agent.decision_engine.get_move(game, depth=3)


@pytest.mark.parametrize("game, side,has_moved, expected_move", test_games)
def test_ab_minimax_agent_makes_correct_decision(ab_minimax_mock_agent, game, side, has_moved, expected_move):
    ab_minimax_mock_agent.side = side
    ab_minimax_mock_agent.has_moved = has_moved
    assert expected_move == ab_minimax_mock_agent.decision_engine.get_move(game, depth=3)
