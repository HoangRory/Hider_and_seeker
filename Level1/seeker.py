from agent import Agent
import map

adjacent = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
adjacent_of_last_step = [((-1, 0), (1, 0)), ((-1, 0), (1, 0)), ((0, -1), (0, 1)), ((0, -1), (0, 1)), ((-1, 0), (0, -1)), ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((1, 0), (0, 1))]

two_steps_away = [(-2, 0), (-2, 1), (-2, 2), (-1, 2), (0, 2)] # a quarter of the surounding tiles
tiles_to_remove = [((-1, 0)), ((-1, 0), (-1, 1)), ((-1, 1)), ((-1, 1), (0, 1)), ((0, 1))] # the tiles to remove from the observable set if corresponding tile two steps away is blocked
quarter_offset = [(1, 1), (-1, 1), (-1, -1), (1, -1)] # the offset of the tiles in the quarter

class Seeker(Agent):
    def __init__(self, start_pos, range, map = None, parent = None):
        super().__init__(start_pos, range, map)
        self.observable = set()
        self.update_observable()
        self.parent = parent
        self.update_map()
        
    def update_observable(self):
        self.observable.clear()
        for i in range(max(self.current_pos[0] - self.range, 0), min((self.current_pos[0] + self.range + 1), self.map.row)):
            for j in range(max(self.current_pos[1] - self.range, 0), min((self.current_pos[1] + self.range + 1), self.map.col)):
                self.observable.add((i, j))
        # check if tile adjacent to the seeker is blocked
        for i in adjacent:
            if self.current_pos[0] + i[0] >= 0 and self.current_pos[0] + i[0] < self.map.row and self.current_pos[1] + i[1] >= 0 and self.current_pos[1] + i[1] < self.map.col:
                if self.map.map[self.current_pos[0] + i[0]][self.current_pos[1] + i[1]] == -1:
                    for step in range(2, self.range + 1):
                        index_remove = (self.current_pos[0] + i[0] * step, self.current_pos[1] + i[1] * step)
                        if index_remove in self.observable:
                            print(index_remove)
                            self.observable.remove(index_remove)
                        # at the last step, also remove the adjacent tiles
                        if step == self.range:
                            for k in adjacent_of_last_step[adjacent.index(i)]:
                                index_remove = (self.current_pos[0] + i[0] * step + k[0], self.current_pos[1] + i[1] * step + k[1])
                                if index_remove in self.observable:
                                    print(index_remove)
                                    self.observable.remove(index_remove)
        # check if tile two steps away from the seeker is blocked
        for offset in quarter_offset:    
            for i in two_steps_away:
                if ((self.current_pos[0] + i[0] * offset[0] >= 0 and self.current_pos[0] + i[0] * offset[0] < self.map.row)
                    and (self.current_pos[1] + i[1] * offset[1] >= 0 and self.current_pos[1] + i[1] * offset[1] < self.map.col)):
                    if self.map.map[self.current_pos[0] + i[0] * offset[0]][self.current_pos[1] + i[1] * offset[1]] == -1:
                        for k in tiles_to_remove[two_steps_away.index(i)]:
                            index_remove = (self.current_pos[0] + (i[0] + k[0]) * offset[0], self.current_pos[1] + (i[1] + k[1]) * offset[1])
                            if index_remove in self.observable:
                                print(index_remove)
                                self.observable.remove(index_remove)
    
    def update_map(self):
        list_observable = list(self.observable.copy())
        for i in range(len(self.observable)):
            self.map.map[list_observable[i][0]][list_observable[i][1]] = 4
        self.map.map[self.current_pos[0]][self.current_pos[1]] = 3
                                    
    def print_observable(self): # for testing only
        print(self.observable)
        

if __name__ == "__main__":
    map2d = map.Map()
    map2d.read_map('map1.txt', 1)
    map2d.print_map()
    seeker_pos = map2d.get_seeker_pos()
    s = Seeker(seeker_pos, 3, map2d)
    s.print_observable()
    s.map.print_map()
