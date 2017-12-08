import numpy as np
import pytest

import decision_engines.a3c_research.game_env as env

init_game = np.array([[7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0, 1]])
expected_state = np.array([[7, 7, 7, 7, 7, 7, 7, 0, 0, 8, 8, 8, 8, 8, 8, 1, 1]])


def test_reset_creates_the_initial_game_state():
    assert np.array_equal(env.reset(), init_game)


@pytest.mark.parametrize("initial_game, action, expected_game", [(init_game, 0, expected_state)])
def test_step_returns_the_correct_game_state(initial_game, action, expected_game):
    next_state, _, _ = env.step(initial_game, action)
    assert np.array_equal(expected_game[0], next_state[0])
