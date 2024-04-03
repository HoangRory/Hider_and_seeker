from pathlib import Path
import random

class Map:
    def __init__(self, row = 0, col = 0, step = 0, timeSignal = 5, hider_radius = 3):
        self.row = row
        self.col = col
        self.map = []
        self.obstacles = []
        self.step = step
        self.timeSignal = timeSignal
        self.hider = []
        self.hider_signal = set()
        self.hider_pos = set()
        self.hider_radius = hider_radius
    
    def read_map(self, file_name, level = 2):
        #read map from file with name file_name in folder "Input/Level{level}" 
        #The map will be a 2D array, with 1 being the wall, 2 being the hider, 3 being the seeker, -1 being the obstacle.
        file_path = Path(__file__).parent.parent / f"Input/Level{level}/{file_name}"
        print(file_path)
        with open(file_path, 'r') as f:
            print(f"Reading map from {file_name}")
            self.row, self.col = map(int, f.readline().strip().split())

            for _ in range(self.row):
                self.map.append(list(map(int, f.readline().strip().split())))
            # #read obstacle
            for line in f:
                top_left_x, top_left_y, bot_right_x, bot_right_y = map(int, line.strip().split())
                self.obstacles.append((top_left_x, top_left_y, bot_right_x, bot_right_y))
            #set obstacle to -1
            for ob in self.obstacles:
                for i in range(ob[0], ob[2] + 1):
                    for j in range(ob[1], ob[3] + 1):
                        self.map[i][j] = -1
        
    def get_seeker_pos(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] == 3:
                    return (i, j)
        return None
    
    def get_hider_pos(self):
        hider_pos_list = []
        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] == 2:
                    hider_pos_list.append((i, j))
        return hider_pos_list
        
    
    def print_map(self):
        for i in range(self.row):
            for j in range(self.col):
                print(self.map[i][j], end = " ")
            print()
    
    def signal(self, hider_pos):
        area = []
        for i in range(hider_pos[0] - self.hider_radius, hider_pos[0] + self.hider_radius + 1):
             for j in range(hider_pos[1] - self.hider_radius, hider_pos[1] + self.hider_radius + 1):
                if i >= 0 and i < self.row and j >= 0 and j < self.col:
                    if self.map[i][j] == 0 or self.map[i][j] == 4:
                        area.append((i, j))
        return random.choice(area)
    
    def get_walls_and_obstacles(self):
        self.obstacles = set()
        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] == -1 or self.map[i][j] == 1:
                    self.obstacles.add((i, j))