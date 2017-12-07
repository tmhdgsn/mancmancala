import numpy as np
import pytest

from agent import Agent
from game import create_board
from side import Side

test_games = [
    (create_board(), Side.SOUTH),
]


@pytest.fixture(scope="module")
def mock_agent():
    return Agent("a3c")


@pytest.mark.parametrize("initial_game, side", test_games)
def test_a3c_can_use_model(mock_agent, initial_game, side):
    mock_agent.side = side
    assert isinstance(mock_agent.decision_engine.get_move(initial_game), int)
