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
            pygame.time.wait(200) # Delay between steps
            step_index += 1

def encounterHider(seeker, list_hider_pos, list_hider_signal):
    found = list_hider_pos.intersection(seeker.observed)
    while found != set():
        for _ in found:
            min_pos = _
            break
        min_distance = seeker.calculateManhattanDistance(min_pos)
        for pos in found:
            val = seeker.calculateManhattanDistance(pos)
            if val < min_distance:
                min_distance = val
                min_pos = pos
        seeker = seeker.AStar(min_pos, list_hider_pos, list_hider_signal)
        for i in range(len(list_hider_signal["hider"])):
            if list_hider_signal["hider"][i].hider_pos == min_pos:
                hider = list_hider_signal["hider"][i]
                break
        list_hider_signal["hider_signal"].discard(hider.signal_pos)
        list_hider_pos.discard(hider.hider_pos)
        found = list_hider_pos.intersection(seeker.observed)
    return {"seeker": seeker, "list_hider_pos": list_hider_pos, "list_hider_signal": list_hider_signal}

def encounterSignal(seeker, list_hider_pos, list_hider_signal):
    found = list_hider_signal["hider_signal"].intersection(seeker.observed)
    checkEncounterHider = False
    while found != set():
        for _ in found:
            min_pos = _
            break
        min_distance = seeker.calculateManhattanDistance(min_pos)
        for pos in found:
            val = seeker.calculateManhattanDistance(pos)
            if val < min_distance:
                min_distance = val
                min_pos = pos
        seeker = seeker.AStar(min_pos, list_hider_pos, list_hider_signal)
        temp = seeker
        path = []
        while seeker.parent != None:
            path.append(seeker)
            seeker = seeker.parent
        path.reverse()
        for i in range(len(path)):
            if list_hider_pos.intersection(path[i].observed) != set():
                temp = path[i]
                checkEncounterHider = True
                break
        seeker = temp
        if checkEncounterHider == True:
            return encounterHider(seeker, list_hider_pos, list_hider_signal)
        for i in range(len(list_hider_signal["hider"])):
            if list_hider_signal["hider"][i].signal_pos == min_pos:
                hider = list_hider_signal["hider"][i]
                break
        list_hider_signal["hider_signal"].discard(min_pos)
        found = list_hider_signal["hider_signal"].intersection(seeker.observed)
    return {"seeker": seeker, "list_hider_pos": list_hider_pos, "list_hider_signal": list_hider_signal}

def search(seeker, list_hider_pos, list_hider_signal):
    result = seeker
    check = False
    while list_hider_pos != set():
        result = result.hillClimbing(list_hider_pos, list_hider_signal, check)
        beginAStar = result
        if list_hider_pos.intersection(result.observed) != set():
            res_dict = encounterHider(result, list_hider_pos, list_hider_signal)
            result = res_dict["seeker"]
            list_hider_pos = res_dict["list_hider_pos"]
            list_hider_signal = res_dict["list_hider_signal"]
        elif list_hider_signal["hider_signal"].intersection(result.observed) != set():
            res_dict = encounterSignal(result, list_hider_pos, list_hider_signal)
            result = res_dict["seeker"]
            list_hider_pos = res_dict["list_hider_pos"]
            list_hider_signal = res_dict["list_hider_signal"]
        else:
            list_unobserved = result.unobserved
            result = result.BFS(list_hider_pos, list_hider_signal, list_unobserved)
            temp = result
            path = []
            while  result.parent != None and result.parent != beginAStar:
                path.append(result)
                result = result.parent
            path.reverse()
            for i in range(len(path)):
                if path[i].seeker_pos in list_unobserved or list_hider_pos.intersection(path[i].observed) != set():
                    temp = path[i]
                    break
            result = temp
            if list_hider_pos.intersection(result.observed) != set():
                res_dict = encounterHider(result, list_hider_pos, list_hider_signal)
                result = res_dict["seeker"]
                list_hider_pos = res_dict["list_hider_pos"]
                list_hider_signal = res_dict["list_hider_signal"]
    return result
        
if __name__ == "__main__":
    map2d = Map()
    map2d.read_map("map1.txt")
    seeker_pos = map2d.get_seeker_pos()
    list_hider = map2d.get_hider_pos()
    list_hider_pos = set()
    for hider in list_hider:
        list_hider_pos.add(hider)
    list_hider_signal = {
        "hider_signal": set(),
        "hider" : []
    }
    for hider_pos in list_hider_pos:
        hider = Hider(hider_pos, 3, map2d)
        list_hider_signal["hider_signal"].add(hider.signal_pos)
        list_hider_signal["hider"].append(hider)
    seeker = Seeker(map2d, seeker_pos)  
    seeker.updateMap()
    result = seeker
    result = search(result, list_hider_pos, list_hider_signal)
    path =sk.findSolution(seeker, result)
    runMapGUI(map2d.map, path)
    print(len(path) * -1 + 20 * len(list_hider_signal["hider"]))

