from pathlib import Path
class Map:
    def __init__(self, row = 0, col = 0) -> None:
        self.row = row
        self.col = col
        self.map = []
        self.obstacle = []
        pass
    def get_map(self):
        return self.map
        pass
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
            #read obstacle
            for line in f:
                top_left_x, top_left_y, bot_right_x, bot_right_y = map(int, line.strip().split())
                self.obstacle.append((top_left_x, top_left_y, bot_right_x, bot_right_y))
            #set obstacle to -1
            for ob in self.obstacle:
                for i in range(ob[0], ob[2] + 1):
                    for j in range(ob[1], ob[3] + 1):
                        self.map[i][j] = -1

    def print_map(self):
        for row in self.map:
            print(row)

def test_map():
    map = Map()
    map.read_map('map1.txt', 1)
    map.print_map()

if __name__ == "__main__":
    test_map()