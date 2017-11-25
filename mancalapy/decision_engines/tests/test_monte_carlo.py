import numpy as np
import pytest

from agent import Agent
from game import Game
from side import Side


@pytest.fixture(scope="function")
def monte_mock_agent():
    return Agent("monte_carlo")


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
def test_monte_carlo_agent_makes_correct_decision(monte_mock_agent, game, side, move):
    monte_mock_agent.side = side
    guessedove = monte_mock_agent.decision_engine.get_move()
    print(guessedove)
    assert move == guessedove
