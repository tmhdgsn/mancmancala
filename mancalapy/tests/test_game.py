import pytest
import numpy as np
from game import Game


@pytest.mark.parametrize("raw_game,expected_game", [
    ("0,0,9,9,9,9,9,2,1,9,8,8,8,8,8,1", Game(board=np.array([
        [0, 0, 9, 9, 9, 9, 9, 2],
        [1, 9, 8, 8, 8, 8, 8, 1]
    ], np.int32)))
])
def test_update_board_generates_correct_board(raw_game, expected_game):
    board = Game()
    board.update_board(raw_game)
    assert board == expected_game
