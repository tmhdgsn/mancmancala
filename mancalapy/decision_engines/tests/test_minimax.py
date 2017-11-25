import numpy as np
import pytest

from agent import Agent
from game import Game
from side import Side


@pytest.fixture(scope="function")
def minimax_mock_agent():
    return Agent("minimax")


@pytest.fixture(scope="function")
def ab_minimax_mock_agent():
    return Agent("minimax")


test_games = [
    (Game(), Side.SOUTH, 1),
    (Game(board=np.array([
        [0, 0, 0, 0, 0, 2, 7, 18],
        [0, 20, 13, 13, 12, 12, 0, 1]
    ])), Side.NORTH, 7),
    (Game(board=np.array([
        [1, 1, 2, 2, 2, 2, 1, 19],
        [1, 2, 1, 2, 0, 2, 0, 60]
    ], np.int32)), Side.SOUTH, 6)
]


@pytest.mark.parametrize("game, side, move", test_games)
def test_minimax_agent_makes_correct_decision(minimax_mock_agent, game, side, move):
    minimax_mock_agent.side = side
    assert move == minimax_mock_agent.decision_engine.get_move(game, depth=4)


@pytest.mark.parametrize("game, side, move", test_games)
def test_ab_minimax_agent_makes_correct_decision(ab_minimax_mock_agent, game, side, move):
    ab_minimax_mock_agent.side = side
    assert move == ab_minimax_mock_agent.decision_engine.get_move(game, depth=3)
