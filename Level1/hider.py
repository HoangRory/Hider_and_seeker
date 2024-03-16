from agent import Agent
import random

class Hider(Agent) :
    def __init__(self, start_pos, range, map=None) -> None:
        super().__init__(start_pos, range, map)

    #check if cell is in bound
    def is_in_bound(self, x, y):
        return 0 <= x < len(self.map) and 0 <= y < len(self.map[0])
    
    #check if cell is empty
    def is_empty_cell(self, x, y):
        return self.map[x][y] == 0

    #choose random cell after a unit of time
    def signal(self, seeker):
        location_around = []
        for dx in range (-3, 4): #range of 3
            for dy in range (-3, 4):
                self_x = self.current_pos[0] + dx
                self_y = self.current_pos[1] + dy

                if self.is_in_bound(self_x, self_y) and self.is_empty_cell(self_x, self_y):
                    location_around.append((self_x, self_y))

        if location_around:
            #random use for later
            # signal_location = random.choice(location_around)
            # print(f"Signal sent at {signal_location}")
            # return signal_location
            
            return location_around[0] #return the first location for now

        return None
    

def test_hider_signal():
    test_map = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 2, 0, 0, 0],  # Hider (2) is placed in the middle
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    
    hider = Hider((3, 3), 2, test_map)

    signal_location = hider.signal(None)

    print(signal_location)

test_hider_signal()
