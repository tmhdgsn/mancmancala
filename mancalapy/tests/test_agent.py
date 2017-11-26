from unittest import mock

import pytest
from io import StringIO

from agent import Agent
from side import Side


@pytest.fixture(scope="module")
def mock_agent():
    return Agent("basic")


@mock.patch('builtins.input')
def test_can_run_agent(mock_input, mock_agent):
    mock_input.side_effect = ["START;SOUTH", "END"]
    mock_agent.play()


@mock.patch('builtins.input')
@mock.patch('sys.stdout', new_callable=StringIO)
def test_agent_swaps_sides(mock_output, mock_input, mock_agent):
    mock_input.side_effect = [
        "START;South",
        "CHANGE;2;8,7,7,7,7,7,7,0,7,0,8,8,8,8,8,1;OPP",
        "CHANGE;SWAP;8,7,7,7,7,7,7,0,7,0,8,8,8,8,8,1;YOU",
        "END"
    ]
    mock_agent.play()
    assert mock_agent.side == Side.NORTH
