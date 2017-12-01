import numpy as np
import pytest

from game import create_board, update_board


@pytest.mark.parametrize("raw_game,expected_game", [
    ("0,0,9,9,9,9,9,2,1,9,8,8,8,8,8,1", np.array([
        [0, 0, 9, 9, 9, 9, 9, 2],
        [1, 9, 8, 8, 8, 8, 8, 1]
    ], np.int32))
])
def test_update_board_generates_correct_board(raw_game, expected_game):
    board = create_board()
    update_board(board, raw_game)
    assert np.array_equal(board, expected_game)
