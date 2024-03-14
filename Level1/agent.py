UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP_RIGHT = (1, 1)
UP_LEFT = (-1, 1)
DOWN_RIGHT = (1, -1)
DOWN_LEFT = (-1, -1)
WAIT = (0, 0)


class Agent :
    def __init__(self, start_pos, range, map = None) -> None:
        self.range = range
        self.start_pos = start_pos
        self.current_pos = self.start_pos
        self.map = map
    def check_valid_move(self, action):
        pass
    def move(self, action):
        if self.check_valid_move(action):
            self.current_pos = (self.current_pos[0] + action[0], self.current_pos[1] + action[1])



