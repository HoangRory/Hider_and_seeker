import random
from map import Map

class Hider:
    def __init__(self, hider_pos, radius, map2d):
        self.hider_pos = hider_pos
        self.radius = radius
        self.map2d = map2d
        self.signal_pos = self.signal()
    
    def signal(self):
        area = []
        for i in range(self.hider_pos[0] - self.radius, self.hider_pos[0] + self.radius + 1):
            for j in range(self.hider_pos[1] - self.radius, self.hider_pos[1] + self.radius + 1):
                if i >= 0 and i < self.map2d.row and j >= 0 and j < self.map2d.col:
                    if self.map2d.map[i][j] == 0:
                        area.append((i, j))
        return random.choice(area)
    


