from agent import Agent

class Hider(Agent) :
    def __init__(self, start_pos, range, map=None) -> None:
        super().__init__(start_pos, range, map)
    def signal(self, seeker):
        pass