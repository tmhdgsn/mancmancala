from unittest import mock

import pytest

from agent import Agent


@pytest.fixture(scope="module")
def mock_agent():
    return Agent("minimax")


def basic_func():
    k = input()
    print(k)


@mock.patch('builtins.input')
def test_can_run_agent(mock_input, mock_agent):
    mock_input.side_effect = ["START;SOUTH", "END"]
    # mock_agent.play() # Will loop infinitely

