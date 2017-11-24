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


@pytest.mark.parametrize("game, side, move", [
    (Game(), Side.SOUTH, 1),
    (Game(board=[
        [0, 0, 0, 0, 0, 2, 7, 18],
        [0, 20, 13, 13, 12, 12, 0, 1]
    ]), Side.NORTH , 7)
])
def test_minimax_agent_makes_correct_decision(minimax_mock_agent, game, side, move):
    minimax_mock_agent.side = side
    assert move == minimax_mock_agent.decision_engine.get_move(game, depth=4)


@pytest.mark.parametrize("game, side, move", [
    (Game(), Side.SOUTH, 1),
])
def test_ab_minimax_agent_makes_correct_decision(ab_minimax_mock_agent, game, side, move):
    ab_minimax_mock_agent.side = side
    assert move == ab_minimax_mock_agent.decision_engine.get_move(game, depth=3)
