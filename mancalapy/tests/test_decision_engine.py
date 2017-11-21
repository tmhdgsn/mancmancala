from agent import Agent
from decision_engines import DecisionEngineFactory
from game import Game


def test_can_get_engine():

    factory = DecisionEngineFactory(Agent("basic"))
    e = (factory["basic"])
    g = Game()
    print(e)
    e.get_move()


if __name__ == '__main__':
    test_can_get_engine()