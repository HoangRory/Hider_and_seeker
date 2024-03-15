from agent import Agent
import numpy as np

adjacent = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
adjacent_of_last_step = [((-1, 0), (1, 0)), ((-1, 0), (1, 0)), ((0, -1), (0, 1)), ((0, -1), (0, 1)), ((-1, 0), (0, -1)), ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((1, 0), (0, 1))]

two_steps_away = [(-2, 0), (-2, 1), (-2, 2), (-1, 2), (0, 2)] # a quarter of the surounding tiles
tiles_to_remove = [((-1, 0)), ((-1, 0), (-1, 1)), ((-1, 1)), ((-1, 1), (0, 1)), ((0, 1))] # the tiles to remove from the observable set if corresponding tile two steps away is blocked
quarter_offset = [(1, 1), (-1, 1), (-1, -1), (1, -1)] # the offset of the tiles in the quarter

class Seeker(Agent) :
    def __init__(self, start_pos, range, map = None) -> None:
        super().__init__(start_pos, range, map)
        self.observable = set()
        
    def update_observable(self):
        self.observable.clear()
        for i in range(max(self.current_pos[0] - self.range, 0), min((self.current_pos[0] + self.range + 1), self.map.row)):
            for j in range(max(self.current_pos[1] - self.range, 0), min((self.current_pos[1] + self.range + 1), self.map.col)):
                self.observable.add((i, j))
        # check if tile adjacent to the seeker is blocked
        for i in adjacent:
            if self.current_pos[0] + i[0] >= 0 and self.current_pos[0] + i[0] < self.map.row and self.current_pos[1] + i[1] >= 0 and self.current_pos[1] + i[1] < self.map.col:
                if self.map.map[self.current_pos[0] + i[0], self.current_pos[1] + i[1]] == -1:
                    for step in range(2, self.range + 1):
                        self.observable.remove((self.current_pos[0] + i[0] * step, self.current_pos[1] + i[1] * step))
                        # at the last step, also remove the adjacent tiles
                        if step == self.range:
                            for j in adjacent_of_last_step[adjacent.index(i)]:
                                self.observable.remove((self.current_pos[0] + i[0] * step + j[0], self.current_pos[1] + i[1] * step + j[1]))
        # check if tile two steps away from the seeker is blocked
        for offset in quarter_offset:    
            for i in two_steps_away:
                if ((self.current_pos[0] + i[0] * offset[0] >= 0 and self.current_pos[0] + i[0] * offset[0] < self.map.row)
                    and (self.current_pos[1] + i[1] * offset[1] >= 0 and self.current_pos[1] + i[1] * offset[1] < self.map.col)):
                    if self.map.map[self.current_pos[0] + i[0] * offset[0], self.current_pos[1] + i[1] * offset[1]] == -1:
                        for j in tiles_to_remove[two_steps_away.index(i)]:
                            self.observable.remove((self.current_pos[0] + (i[0] + j[0]) * offset[0], self.current_pos[1] + (i[1] + j[1]) * offset[1]))
                                    
    def print_observable(self): # for testing only
        print(self.observable)
        
    def search(self):
        pass



   
class map: # dummy class for testing
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.map = np.zeros((row, col))
    def print_map(self):
        print(self.map)
        print()
        
# test       
if __name__ == "__main__":
    m = map(7, 7)
    sk = Seeker((3, 3), 3, m)
    
    m.map[1, 4] = -1
    m.map[2, 5] = -1
    m.map[2, 1] = -1
    print("map:")
    m.print_map()
    sk.update_observable()
    sk.print_observable()