from agent import Agent

class Seeker(Agent) :
    def __init__(self, start_pos, range, map=None) -> None:
        super().__init__(start_pos, range, map)
        self.observed = []
    def update_observed(self):
        pass
    def search(self):
        pass