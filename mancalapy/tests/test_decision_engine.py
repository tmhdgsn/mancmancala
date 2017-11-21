from agent import Agent
from decision_engine import DecisionEngineFactory
from game import Game


def test_can_get_engine():

    factory = DecisionEngineFactory(Agent("minimax"))
    e = (factory["minimax"])
    g = Game()
    print(e)
    e.get_move(g.board)


if __name__ == '__main__':
    test_can_get_engine()