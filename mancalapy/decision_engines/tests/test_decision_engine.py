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
    ])))
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
    my_turn = mock_agent.decision_engine.play_hole(hole, initial_game, side)
    assert my_turn and initial_game == expected_game


@pytest.mark.parametrize("game, hole,side", test_repeat_games)
def test_play_hole_repeats_go_if_last_seed_lands_in_mancala(mock_agent, game, hole, side):
    assert mock_agent.decision_engine.play_hole(hole, game, side)


@pytest.mark.parametrize("game, hole,side", test_non_repeat_games)
def test_play_hole_doesnt_repeat_go_if_last_seed_doesnt_land_in_mancala(mock_agent, game, hole, side):
    assert not mock_agent.decision_engine.play_hole(hole, game, side)
