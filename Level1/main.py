import pygame
from map import Map
from seeker import Seeker
import seeker as sk
from hider import Hider

class MapGUI:
    def __init__(self, map_data, tile_size=20):
        self.map_data = map_data
        self.tile_size = tile_size
        self.colors = {
            1: (0, 0, 0),   # Wall
            2: (103, 198, 227), # Hider
            3: (255, 32, 78), # Seeker
            -1: (39, 55, 77), # Obstacle
            0: (255, 255, 255),  # Empty space (added color for value 0)
            4: (0, 34, 77), # observed square 
            5: (83, 86, 255) # signal square
        }
        self.signal_blink_interval = 500  # Blink interval in milliseconds
        self.last_blink_time = 0  # Track the time of the last blink
        # Calculate window size based on map size and tile size
        self.window_width = len(map_data[0]) * tile_size
        self.window_height = len(map_data) * tile_size
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Hide and Seek')

    def draw_map(self):
        # current_time = pygame.time.get_ticks()
        # if current_time - self.last_blink_time >= self.signal_blink_interval:
        #     self.last_blink_time = current_time
        #     self.toggle_signal_visibility()
        self.screen.fill((255, 255, 255))  # Fill background with white
        # Draw each tile based on map data
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                color = self.colors[self.map_data[y][x]]
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, color, rect)
                # Draw vertical grid lines
                pygame.draw.line(self.screen, (0, 0, 0), (x * self.tile_size, 0), (x * self.tile_size, self.window_height))
            # Draw horizontal grid lines
            pygame.draw.line(self.screen, (0, 0, 0), (0, y * self.tile_size), (self.window_width, y * self.tile_size))
        pygame.display.flip()  # Update the display

    def toggle_signal_visibility(self):
        # Toggle the color of the signal square between the original color and white
        if self.colors[5] == (83, 86, 255):
            self.colors[5] = (255, 255, 255)
        else:
            self.colors[5] = (83, 86, 255)

def search1(seeker, hider):
    result = seeker
    check = False
    while True:
        result = result.hillClimbing(hider, check)
        beginAStar = result
        if hider.hider_pos in result.observed:
            result = result.AStar(hider.hider_pos, hider)
            break
        elif hider.signal_pos in result.observed:
            check = True
            result = result.AStar(hider.signal_pos, hider)
            temp = result
            path = []
            while result.parent != None and result.parent != beginAStar:
                path.append(result)
                result = result.parent
            path.reverse()
            for i in range(len(path)):
                if hider.hider_pos in path[i].observed:
                    temp = path[i]
                    break
            result = temp
        else:
            for val in result.unobserved:
                goal_pos = val
                break
            list_unobserved = result.unobserved
            result = result.AStar(goal_pos, hider, list_unobserved)
            temp = result
            path = []
            while  result.parent != None and result.parent != beginAStar:
                path.append(result)
                result = result.parent
            path.reverse()
            for i in range(len(path)):
                if len(path[i].unobserved) < len(list_unobserved) or hider.hider_pos in path[i].observed:
                    temp = path[i]
                    break
            result = temp
            if hider.hider_pos in result.observed:
                result = result.AStar(hider.hider_pos, hider)
                break
    return result

def search2(seeker, hider):
    result = seeker
    check = False
    while True:
        result = result.hillClimbing(hider, check)
        beginAStar = result
        if hider.hider_pos in result.observed:
            result = result.AStar(hider.hider_pos, hider)
            break
        elif hider.signal_pos in result.observed:
            check = True
            result = result.AStar(hider.signal_pos, hider)
            temp = result
            path = []
            while result.parent != None and result.parent != beginAStar:
                path.append(result)
                result = result.parent
            path.reverse()
            for i in range(len(path)):
                if hider.hider_pos in path[i].observed:
                    temp = path[i]
                    break
            result = temp
        else:
            list_unobserved = result.unobserved
            result = result.BFS(hider, list_unobserved)
            temp = result
            path = []
            while  result.parent != None and result.parent != beginAStar:
                path.append(result)
                result = result.parent
            path.reverse()
            for i in range(len(path)):
                if path[i].seeker_pos in list_unobserved or hider.hider_pos in path[i].observed:
                    temp = path[i]
                    break
            result = temp
            if hider.hider_pos in result.observed:
                result = result.AStar(hider.hider_pos, hider)
                break
    return result

def runMapGUI(beginningMap, path):
    map_gui = MapGUI(beginningMap)
    running = True
    step_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if step_index < len(path):
            map_gui.map_data = path[step_index].map.map
            map_gui.draw_map()
            pygame.time.wait(200)  # Wait for 1 second
            step_index += 1

if __name__ == "__main__":
    map2d = Map()
    map2d.read_map("map1.txt")
    seeker_pos = map2d.get_seeker_pos()
    hider_pos = map2d.get_hider_pos()
    seeker = Seeker(map2d = map2d, seeker_pos = seeker_pos)
    hider = Hider(hider_pos, 3, map2d)
    seeker.updateMap()
    # result = seeker
    # check = False
    # while True:
    #     result = result.hillClimbing(hider, check)
    #     beginAStar = result
    #     if hider.hider_pos in result.observed:
    #         result = result.AStar(hider.hider_pos, hider)
    #         break
    #     elif hider.signal_pos in result.observed:
    #         check = True
    #         result = result.AStar(hider.signal_pos, hider)
    #         temp = result
    #         path = []
    #         while result.parent != None and result.parent != beginAStar:
    #             path.append(result)
    #             result = result.parent
    #         path.reverse()
    #         for i in range(len(path)):
    #             if hider.hider_pos in path[i].observed:
    #                 temp = path[i]
    #                 break
    #         result = temp
    #     else:
    #         # for val in result.unobserved:
    #         #     goal_pos = val
    #         #     break
    #         # list_unobserved = result.unobserved.copy()
    #         # result = result.AStar(goal_pos, hider, result.unobserved)
    #         # temp = result
    #         # path = []
    #         # while  result.parent != None and result.parent != beginAStar:
    #         #     path.append(result)
    #         #     result = result.parent
    #         # path.reverse()
    #         # for i in range(len(path)):
    #         #     if path[i].seeker_pos in list_unobserved or hider.hider_pos in path[i].observed:
    #         #         temp = path[i]
    #         #         break
    #         # result = temp
    #         # if hider.hider_pos in result.observed:
    #         #     result = result.AStar(hider.hider_pos, hider)
    #         #     break
    #         list_unobserved = result.unobserved
    #         result = result.BFS(hider, list_unobserved)
    #         temp = result
    #         path = []
    #         while  result.parent != None and result.parent != beginAStar:
    #             path.append(result)
    #             result = result.parent
    #         path.reverse()
    #         for i in range(len(path)):
    #             if path[i].seeker_pos in list_unobserved or hider.hider_pos in path[i].observed:
    #                 temp = path[i]
    #                 break
    #         result = temp
    #         if hider.hider_pos in result.observed:
    #             result = result.AStar(hider.hider_pos, hider)
    #             break
    result = search2(seeker, hider)

    path = sk.findSolution(seeker, result)
    runMapGUI(map2d.map, path)
    print(len(path) * -1 + 20)
# if __name__ == "__main__":
#     map2d = Map()
#     map2d.read_map("map2.txt")
#     seeker_pos = map2d.get_seeker_pos()
#     hider_pos = map2d.get_hider_pos()
#     seeker = Seeker(map2d = map2d, seeker_pos = seeker_pos)
#     hider = Hider(hider_pos, 3, map2d)
#     seeker.updateMap()
#     map_gui = MapGUI(seeker.map.map)
#     while True:
#         map_gui.draw_map()
#         if pygame.event.get(pygame.QUIT):
#             break