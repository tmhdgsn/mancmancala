import sys

from decision_engines import DecisionEngineFactory
from game import Game
from side import Side
from util import log_output


class Agent:
    def __init__(self, engine):
        self.factory = DecisionEngineFactory(self)
        self.game = Game()
        self.side = Side.NORTH
        self.decision_engine = self.factory[engine] if engine in self.factory.engines else self.factory["basic"]

    @classmethod
    def get_msg(cls):
        from_engine = input().strip()
        log_output(f"from engine: {from_engine}")
        args = from_engine.split(";")
        return args[0], args[1:]

    @classmethod
    def send_msg(cls, msg):
        log_output(f"from agent: {msg}")
        print(msg)

    def play(self):
        our_turn = False
        while True:
            msg_type, args = self.get_msg()
            if msg_type.upper() == "START":
                if args[0].upper() == "SOUTH":
                    self.side = Side.SOUTH
                    our_turn = True
                else:
                    self.side = Side.NORTH
            if msg_type.upper() == "END":
                break
            if msg_type.upper() == "CHANGE":
                our_turn = args[-1].upper() == "YOU"
                self.game.update_board(args[-2])
                if args[0].upper() == "SWAP":
                    self.side = self.side.opposite()
                log_output(repr(self.game))
            if our_turn:
                move = self.decision_engine.get_move()
                self.send_msg(f"MOVE;{move}")


if __name__ == '__main__':
    agent = Agent("ab_minimax")
    if len(sys.argv) > 1:
        if sys.argv[1] in agent.factory.engines:
            agent = Agent(sys.argv[1])
    agent.play()
