from cyagent import Agent
import sys

if __name__ == '__main__':
    agent = Agent("ab_minimax")
    if len(sys.argv) > 1:
        if sys.argv[1] in agent.factory.engines:
            agent = Agent(sys.argv[1])
    agent.play()
