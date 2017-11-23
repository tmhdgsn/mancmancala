import pytest

from game import Game
from side import Side

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

# TODO: Create test cases for minimax
