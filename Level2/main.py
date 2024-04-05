import pygame
from map import Map
from seeker import Seeker
import seeker as sk
import random
import copy
import time

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
            pygame.time.wait(100)
            step_index += 1

def encounterHider(seeker, beginAStar, hider_pos, list_potential_hider_signal, current_signal):
    result = seeker
    result = result.AStar(hider_pos)
    if result.map.map == beginAStar.map.map:
        return result, current_signal
    path = []
    while result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    temp = None
    original_signal = current_signal.copy()
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            for signal in original_signal:
                if signal == path[i].seeker_pos:
                    pass
                elif signal in path[i].observed:
                    path[i].map.map[signal[0]][signal[1]] = 4
                else:
                    path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                current_signal = set()
                for hider in list_potential_hider_signal:
                    if hider["hider_pos"] in path[i].map.hider_pos:
                        signal = random.choice(hider["potential_signal"])
                        while signal == path[i].seeker_pos:
                            signal = random.choice(hider["potential_signal"])
                        current_signal.add(signal)
            for signal in current_signal:
                path[i].map.map[signal[0]][signal[1]] = 5
            path[i].map.map[path[i].seeker_pos[0]][path[i].seeker_pos[1]] = 3
    result = path[-1]
    for hider in list_potential_hider_signal:
        result.map.hider_pos.remove(hider_pos)
        break
    foundSignal = current_signal.intersection(result.observed)
    if foundSignal != set():
        signal_pos = None
        min_distance = 1e9
        for signal in foundSignal:
            distance = result.calculateManhattanDistance(signal)
            if distance < min_distance and distance <= 2 * result.map.hider_radius - random.randint(0, result.map.hider_radius) and signal not in result.parent.observed:
                min_distance = distance
                signal_pos = signal
        if signal_pos != None:
            beginAStar = Seeker(result.map, result.seeker_pos)
            res = encounterSignal(result, beginAStar, signal_pos, list_potential_hider_signal, current_signal)
            result = res[0]
            current_signal = res[1]
            return result, current_signal
    return result, current_signal

def encounterSignal(seeker, beginAStar, signal_pos, list_potential_hider_signal, current_signal):
    result = seeker
    result = result.AStar(signal_pos)
    if result.map.map == beginAStar.map.map:
        return result, current_signal
    path = []
    while result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    temp = None
    original_signal = current_signal.copy()
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            for signal in original_signal:
                if signal == path[i].seeker_pos:
                    pass
                elif signal in path[i].observed:
                    path[i].map.map[signal[0]][signal[1]] = 4
                else:
                    path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                current_signal = set()
                for hider in list_potential_hider_signal:
                    if hider["hider_pos"] in path[i].map.hider_pos:
                        signal = random.choice(hider["potential_signal"])
                        while signal == path[i].seeker_pos:
                            signal = random.choice(hider["potential_signal"])
                        current_signal.add(signal)
            for signal in current_signal:
                path[i].map.map[signal[0]][signal[1]] = 5
            path[i].map.map[path[i].seeker_pos[0]][path[i].seeker_pos[1]] = 3
        if path[i].map.hider_pos.intersection(path[i].observed) != set():
            temp = path[i]
            break
        if i == len(path) - 1:
            temp = path[i]
    result = temp
    foundHider = result.map.hider_pos.intersection(result.observed)
    if foundHider != set():
        check = True
        hider_pos = None
        min_distance = 1e9
        for hider in foundHider:
            distance = result.calculateManhattanDistance(hider)
            if distance < min_distance:
                min_distance = distance
                hider_pos = hider
        beginAStar = Seeker(result.map, result.seeker_pos)
        res = encounterHider(result, beginAStar, hider_pos, list_potential_hider_signal, current_signal)
        result = res[0]
        current_signal = res[1]
        return result, current_signal
    foundSignal = current_signal.intersection(result.observed)
    if foundSignal != set():
        signal_pos = None
        min_distance = 1e9
        for signal in foundSignal:
            distance = result.calculateManhattanDistance(signal)
            if distance < min_distance and distance <= 2 * result.map.hider_radius - random.randint(0, result.map.hider_radius) and signal not in result.parent.observed:
                min_distance = distance
                signal_pos = signal
        if signal_pos != None:
            beginAStar = Seeker(result.map, result.seeker_pos)
            res = encounterSignal(result, beginAStar, signal_pos, list_potential_hider_signal, current_signal)
            result = res[0]
            current_signal = res[1]
            return result, current_signal
    return result, current_signal
    
def encounterLocalMaximum(seeker, beginAStar, list_potential_hider_signal, current_signal):
    result = seeker
    list_unobserved = result.unobserved.copy()
    result = result.BFS(list_unobserved)
    if result.map.map == beginAStar.map.map:
        return result, current_signal
    path = []
    while result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    temp = None
    original_signal = current_signal.copy()
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            for signal in original_signal:
                if signal == path[i].seeker_pos:
                    pass
                elif signal in path[i].observed:
                    path[i].map.map[signal[0]][signal[1]] = 4
                else:
                    path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                current_signal = set()
                for hider in list_potential_hider_signal:
                    if hider["hider_pos"] in path[i].map.hider_pos:
                        signal = random.choice(hider["potential_signal"])
                        while signal == path[i].seeker_pos:
                            signal = random.choice(hider["potential_signal"])
                        current_signal.add(signal)
            for signal in current_signal:
                path[i].map.map[signal[0]][signal[1]] = 5
            path[i].map.map[path[i].seeker_pos[0]][path[i].seeker_pos[1]] = 3
        if len(path[i].unobserved) < len(list_unobserved) or path[i].map.hider_pos.intersection(path[i].observed) != set():
            temp = path[i]
            break
        if i == len(path) - 1:
            temp = path[i]
    result = temp
    if result.seeker_pos in result.map.hider_pos:
        result.map.hider_pos.discard(result.seeker_pos)
        return result, current_signal
    foundHider = result.map.hider_pos.intersection(result.observed)
    if foundHider != set():
        check = True
        hider_pos = None
        min_distance = 1e9
        for hider in foundHider:
            distance = result.calculateManhattanDistance(hider)
            if distance < min_distance:
                min_distance = distance
                hider_pos = hider
        beginAStar = Seeker(result.map, result.seeker_pos)
        res = encounterHider(result, beginAStar, hider_pos, list_potential_hider_signal, current_signal)
        result = res[0]
        current_signal = res[1]
        return result, current_signal
    foundSignal = current_signal.intersection(result.observed)
    if foundSignal != set():
        signal_pos = None
        min_distance = 1e9
        for signal in foundSignal:
            distance = result.calculateManhattanDistance(signal)
            if distance < min_distance and distance <= 2 * result.map.hider_radius - random.randint(0, result.map.hider_radius) and signal not in result.parent.observed:
                min_distance = distance
                signal_pos = signal
        if signal_pos != None:
            beginAStar = Seeker(result.map, result.seeker_pos)
            res = encounterSignal(result, beginAStar, signal_pos, list_potential_hider_signal, current_signal)
            result = res[0]
            current_signal = res[1]
            return result, current_signal
    return result, current_signal

def encounterLocalMaximum2(seeker, beginAStar, list_potential_hider_signal, current_signal):
    result = seeker
    list_unobserved = result.unobserved.copy()
    goal_pos = None
    for val in list_unobserved:
        goal_pos = val
        break
    result = result.AStar(goal_pos)
    if result.map.map == beginAStar.map.map:
        return result, current_signal
    path = []
    while result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    temp = None
    original_signal = current_signal.copy()
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            for signal in original_signal:
                if signal == path[i].seeker_pos:
                    pass
                elif signal in path[i].observed:
                    path[i].map.map[signal[0]][signal[1]] = 4
                else:
                    path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                current_signal = set()
                for hider in list_potential_hider_signal:
                    if hider["hider_pos"] in path[i].map.hider_pos:
                        signal = random.choice(hider["potential_signal"])
                        while signal == path[i].seeker_pos:
                            signal = random.choice(hider["potential_signal"])
                        current_signal.add(signal)
            for signal in current_signal:
                path[i].map.map[signal[0]][signal[1]] = 5
            path[i].map.map[path[i].seeker_pos[0]][path[i].seeker_pos[1]] = 3
        if len(path[i].unobserved) < len(list_unobserved) or path[i].map.hider_pos.intersection(path[i].observed) != set():
            temp = path[i]
            break
        if i == len(path) - 1:
            temp = path[i]
    result = temp
    if result.seeker_pos in result.map.hider_pos:
        result.map.hider_pos.discard(result.seeker_pos)
        return result, current_signal

def search(seeker, list_potential_hider_signal, current_signal, time_limit = 10):
    result = seeker
    check = False
    start = time.time()
    while result.map.hider_pos != set():
        res = result.hillClimbing(list_potential_hider_signal, current_signal, check)
        result = res[0]
        current_signal = res[1]
        print(result.seeker_pos, end = "hill\n")
        beginAStar = Seeker(result.map, result.seeker_pos)
        foundHider = result.map.hider_pos.intersection(result.observed)
        if foundHider != set():
            check = True
            hider_pos = None
            min_distance = 1e9
            for hider in foundHider:
                distance = result.calculateManhattanDistance(hider)
                if distance < min_distance:
                    min_distance = distance
                    hider_pos = hider
            beginAStar = Seeker(result.map, result.seeker_pos)
            res = encounterHider(result, beginAStar, hider_pos, list_potential_hider_signal, current_signal)
            result = res[0]
            current_signal = res[1]
            print(result.seeker_pos, end = "hider\n")
            continue
        foundSignal = current_signal.intersection(result.observed)
        if foundSignal != set():
            signal_pos = None
            min_distance = 1e9
            for signal in foundSignal:
                distance = result.calculateManhattanDistance(signal)
                if distance < min_distance and distance < 2 * result.map.hider_radius - random.randint(0, result.map.hider_radius) and signal not in result.parent.observed:
                    min_distance = distance
                    signal_pos = signal
            if signal_pos != None:
                beginAStar = Seeker(result.map, result.seeker_pos)
                res = encounterSignal(result, beginAStar, signal_pos, list_potential_hider_signal, current_signal)
                result = res[0]
                current_signal = res[1]
                print(result.seeker_pos, end = "signal\n")
                continue
        res = encounterLocalMaximum(result, beginAStar, list_potential_hider_signal, current_signal)
        result = res[0]
        current_signal = res[1]
        print(result.seeker_pos, end = "local\n")
    return result

if __name__ == "__main__":
    map2d = Map()
    map2d.read_map("map2.txt")
    seeker_pos = map2d.get_seeker_pos()
    map2d.get_walls_and_obstacles()
    hider_pos_list = map2d.get_hider_pos()
    list_potential_hider_signal = []
    current_signal = set()
    for hider_pos in hider_pos_list:
        hider = {
            "hider_pos": hider_pos,
            "potential_signal": map2d.potentialSignalArea(hider_pos)
        }
        list_potential_hider_signal.append(hider)
        map2d.hider_pos.add(hider_pos)
        current_signal.add(random.choice(hider["potential_signal"]))
    seeker = Seeker(map2d, seeker_pos)
    seeker.updateMap()
    result = seeker
    result = search(result, list_potential_hider_signal, current_signal)
    path = sk.findSolution(seeker, result)
    runMapGUI(map2d.map, path)
    print(path[-1].map.step * -1 + len(hider_pos_list))
    