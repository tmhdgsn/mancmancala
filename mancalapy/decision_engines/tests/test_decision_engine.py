import numpy as np

from agent import Agent
from game import Game
from side import Side
import pytest

test_games = [
    (Game(), 0, Side.SOUTH, (Game(board=[
        [7, 7, 7, 7, 7, 7, 7, 0],
        [0, 8, 8, 8, 8, 8, 8, 1]
    ]))),
    (Game(), 0, Side.NORTH, (Game(board=[
        [0, 8, 8, 8, 8, 8, 8, 1],
        [7, 7, 7, 7, 7, 7, 7, 0]
    ]))),
    (Game(board=[
        [0, 0, 0, 0, 0, 0, 8, 19],
        [0, 20, 13, 13, 12, 12, 1, 1]
    ]), 6, Side.NORTH, Game(board=[
        [0, 0, 0, 0, 0, 0, 0, 20],
        [1, 21, 14, 14, 13, 13, 2, 1]
    ])),
    (Game(board=np.array([
        [0, 0, 1, 1, 2, 12, 12, 5],
        [1, 15, 11, 10, 10, 9, 8, 1]
    ])), 1, Side.SOUTH, Game(board=[
        [1, 1, 2, 2, 3, 0, 13, 5],
        [2, 0, 12, 11, 11, 10, 9, 16]
    ]))
]

# (games, actions) that should make it your go again
test_repeat_games = [
    (Game(), 0, Side.SOUTH)
]

# (games, actions) that should not make it your go again
test_non_repeat_games = [
    (Game(), 1, Side.SOUTH)
]


@pytest.fixture(scope="module")
def mock_agent():
    return Agent("basic")


@pytest.mark.parametrize("initial_game, hole, side,expected_game", test_games)
def test_play_hole_updates_mancala_correctly(mock_agent, initial_game, hole, side, expected_game):
    mock_agent.decision_engine.play_hole(hole, initial_game, side)
    assert initial_game == expected_game


@pytest.mark.parametrize("game, hole,side", test_repeat_games)
def test_play_hole_repeats_go_if_last_seed_lands_in_mancala(mock_agent, game, hole, side):
    assert mock_agent.decision_engine.play_hole(hole, game, side)


@pytest.mark.parametrize("game, hole,side", test_non_repeat_games)
def test_play_hole_doesnt_repeat_go_if_last_seed_doesnt_land_in_mancala(mock_agent, game, hole, side):
    assert not mock_agent.decision_engine.play_hole(hole, game, side)
