from pathlib import Path

class Map:
    def __init__(self, row = 0, col = 0):
        self.row = row
        self.col = col
        self.map = []
        self.obstacles = []
    
    def read_map(self, file_name, level = 1):
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
        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] == 2:
                    return (i, j)
        return None
    
    def print_map(self):
        for i in range(self.row):
            for j in range(self.col):
                print(self.map[i][j], end = " ")
            print()