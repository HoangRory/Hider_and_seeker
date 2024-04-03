import pygame
from map import Map
from seeker import Seeker
import seeker as sk

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
            pygame.time.wait(200)  # Wait for 1 second
            step_index += 1

def encounterHider(seeker, beginAStar, hider_pos):
    result = seeker
    result = result.AStar(hider_pos)
    path = []
    temp = result
    while result.parent != None and result.parent != beginAStar:
        path.append(result)
        result = result.parent
    path.reverse()
    for i in range(len(path)):
        if path[i].seeker_pos in path[i].map.hider_pos:
            temp = path[i]
            break
        if path[i].map.step > path[i].map.timeSignal and path[i].map.step % path[i].map.timeSignal == 0:
            path[i].map.hider_signal = set()
            for hider_signal in path[i].map.hider:
                if path[i].seeker_pos == hider_signal["signal_pos"]:
                    pass
                elif hider_signal["signal_pos"] in path[i].observed:
                    path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 4
                else:
                    path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 0
                hider_signal["signal_pos"] = path[i].map.signal(hider_signal["hider_pos"])
                path[i].map.hider_signal.add(hider_signal["signal_pos"])
                path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 5
            temp = path[i]
            break
    result = temp
    foundHider = result.map.hider_pos.intersection(result.observed)
    if foundHider != set():
        hider_pos = None
        min_distance = 1e9
        for pos in foundHider:
            hider_pos = pos
            distance = result.calculateManhattanDistance(pos)
            if distance < min_distance:
                min_distance = distance
        for pos in foundHider:
            distance = result.calculateManhattanDistance(pos)
            if distance == min_distance:
                hider_pos = pos
                break
        result = result.AStar(hider_pos)
        result.map.hider_pos.discard(hider_pos)
        for hider in result.map.hider:
            if hider["hider_pos"] == hider_pos:
                result.map.hider.remove(hider)
                result.map.hider_signal.discard(hider["signal_pos"])
                break
    return result

def encounterSignal(seeker, beginAStar, hider_signal_pos):
    result = seeker
    result = result.AStar(hider_signal_pos)
    path = []
    temp = result
    while result.parent != None and result.parent != beginAStar:
        path.append(result)
        result = result.parent
    path.reverse()
    for i in range(len(path)):
        if path[i].map.step > path[i].map.timeSignal and path[i].map.step % path[i].map.timeSignal == 0:
            path[i].map.hider_signal = set()
            for hider_signal in path[i].map.hider:
                if path[i].seeker_pos == hider_signal["signal_pos"]:
                    pass
                elif hider_signal["signal_pos"] in path[i].observed:
                    path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 4
                else:
                    path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 0
                hider_signal["signal_pos"] = path[i].map.signal(hider_signal["hider_pos"])
                path[i].map.hider_signal.add(hider_signal["signal_pos"])
                path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 5
            temp = path[i]
            break
        if path[i].map.hider_pos.intersection(path[i].observed) != set():
            temp = path[i]
            break
    result = temp
    foundHider = result.map.hider_pos.intersection(result.observed)
    if foundHider != set():
        hider_pos = None
        min_distance = 1e9
        for pos in foundHider:
            hider_pos = pos
            distance = result.calculateManhattanDistance(pos)
            if distance < min_distance:
                min_distance = distance
        for pos in foundHider:
            distance = result.calculateManhattanDistance(pos)
            if distance == min_distance:
                hider_pos = pos
                break
        result = encounterHider(result, result, hider_pos)
        return result
    foundHiderSignal = result.map.hider_signal.intersection(result.observed)
    if foundHiderSignal != set():
        hider_signal_pos = None
        min_distance = 1e9
        for pos in foundHiderSignal:
            hider_signal_pos = pos
            distance = result.calculateManhattanDistance(pos)
            if distance < min_distance and distance <= 2 * result.map.hider_radius:
                min_distance = distance
        for pos in foundHiderSignal:
            distance = result.calculateManhattanDistance(pos)
            if distance == min_distance:
                hider_signal_pos = pos
                break
        result = encounterSignal(result, result, hider_signal_pos)
        return result
    return result

def encounterLocalMaximum(seeker, beginAStar):
    result = seeker
    list_unobserved = result.unobserved
    result = result.BFS(list_unobserved)
    temp = result
    path = []
    while  result.parent != None and result != beginAStar:
        path.append(result)
        result = result.parent
    path.reverse()
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal and path[i].map.step % path[i].map.timeSignal == 0:
            path[i].map.hider_signal = set()
            for hider_signal in path[i].map.hider:
                if path[i].seeker_pos == hider_signal["signal_pos"]:
                    pass
                elif hider_signal["signal_pos"] in path[i].observed:
                    path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 4
                else:
                    path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 0
                hider_signal["signal_pos"] = path[i].map.signal(hider_signal["hider_pos"])
                path[i].map.hider_signal.add(hider_signal["signal_pos"])
                path[i].map.map[hider_signal["signal_pos"][0]][hider_signal["signal_pos"][1]] = 5
            temp = path[i]
            break
        if len(path[i].unobserved) < len(list_unobserved) or path[i].map.hider_pos.intersection(path[i].observed) != set():
            temp = path[i]
            break
    result = temp
    foundHider = result.map.hider_pos.intersection(result.observed)
    if foundHider != set():
        hider_pos = None
        min_distance = 1e9
        for pos in foundHider:
            hider_pos = pos
            distance = result.calculateManhattanDistance(pos)
            if distance < min_distance:
                min_distance = distance
        for pos in foundHider:
            distance = result.calculateManhattanDistance(pos)
            if distance == min_distance:
                hider_pos = pos
                break
        result = encounterHider(result, result, hider_pos)
        return result
    return result

def search(seeker):
    result = seeker
    check = False
    while result.map.hider_pos != set():
        result = result.hillClimbing(check)
        beginAStar = result
        foundHider = result.map.hider_pos.intersection(result.observed)
        if foundHider != set():
            hider_pos = None
            min_distance = 1e9
            for pos in foundHider:
                hider_pos = pos
                distance = result.calculateManhattanDistance(pos)
                if distance < min_distance:
                    min_distance = distance
            for pos in foundHider:
                distance = result.calculateManhattanDistance(pos)
                if distance == min_distance:
                    hider_pos = pos
                    break
            result = encounterHider(result, beginAStar, hider_pos)
            continue
        foundHiderSignal = result.map.hider_signal.intersection(result.observed)
        if foundHiderSignal != set():
            check = True
            hider_signal_pos = None
            min_distance = 1e9
            for pos in foundHiderSignal:
                hider_signal_pos = pos
                distance = result.calculateManhattanDistance(pos)
                if distance < min_distance and distance <= 2 * result.map.hider_radius:
                    min_distance = distance
            hider_signal_pos = None
            for pos in foundHiderSignal:
                distance = result.calculateManhattanDistance(pos)
                if distance == min_distance:
                    hider_signal_pos = pos
                    break
            if  hider_signal_pos != None:
                result = encounterSignal(result, beginAStar, hider_signal_pos)
                continue
        result = encounterLocalMaximum(result, beginAStar)
    return result

if __name__ == "__main__":
    map2d = Map()
    map2d.read_map("map1.txt")
    seeker_pos = map2d.get_seeker_pos()
    map2d.get_hider_pos()
    map2d.get_walls_and_obstacles()
    hider_pos_list = map2d.get_hider_pos()
    for hider_pos in hider_pos_list:
        hider = {
            "hider_pos": hider_pos,
            "signal_pos": map2d.signal(hider_pos)
        }
        map2d.hider.append(hider)
        map2d.hider_pos.add(hider_pos)
        map2d.hider_signal.add(hider["signal_pos"])
    seeker = Seeker(map2d, seeker_pos)
    seeker.updateMap()
    result = seeker
    result = search(result)
    path = sk.findSolution(seeker, result)
    runMapGUI(map2d.map, path)
    print(len(path) * -1 + 20 * len(hider_pos_list))

    
    