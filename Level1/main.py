import pygame
from .map import Map
from .seeker import Seeker, findSolution as sk
import random

class MapGUI:
    def __init__(self, map_data, tile_size=15):
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
        score_display_height = 40  # Height of the score display area
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height + score_display_height))
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
        pygame.draw.line(self.screen, (0, 0, 0), (0, self.window_height), (self.window_width, self.window_height))
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
    found_hider = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if step_index < len(path):
            map_gui.map_data = path[step_index].map.map
            # if seeker's position overlaps with hider's position, increment found_hider
            if path[step_index].seeker_pos == path[step_index].map.hider_pos:
                found_hider += 1
            map_gui.draw_map()
            score_font = pygame.font.Font(pygame.font.match_font('Arial'), 25)
            score = step_index * -1 + found_hider * 20
            score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))  # Specify text color as (0, 0, 0) for black
            score_rect = score_text.get_rect()
            score_rect.bottom = map_gui.window_height + 35  # Set the bottom of the text rectangle
            map_gui.screen.blit(score_text, score_rect)  # Blit score text onto the screen
            pygame.display.flip()  # Update the display after blitting
            pygame.time.wait(100)
            step_index += 1

def encounterHider(seeker, beginAStar, potentialSignalArea):
    result = seeker
    result = result.AStar(result.map.hider_pos)
    if result.map.map == beginAStar.map.map:
        return result
    path = []
    temp = result
    while result.parent != None and result != beginAStar:
        path.append(result)
        result = result.parent
    path.reverse()
    signal_pos = path[0].map.hider_signal_pos
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            signal = path[i].map.hider_signal_pos
            if signal == path[i].seeker_pos:
                pass
            elif signal in path[i].observed:
                path[i].map.map[signal[0]][signal[1]] = 4
            else:
                path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                signal_pos = random.choice(potentialSignalArea)
                while signal_pos == path[i].seeker_pos:
                    signal_pos = random.choice(potentialSignalArea)
            if path[i].seeker_pos != signal_pos:
                path[i].map.map[signal_pos[0]][signal_pos[1]] = 5
            path[i].map.hider_signal_pos = signal_pos
    result = path[-1]
    if result.map.hider_signal_pos in result.observed:
        result.map.map[result.map.hider_signal_pos[0]][result.map.hider_signal_pos[1]] = 4
    else:
        result.map.map[result.map.hider_signal_pos[0]][result.map.hider_signal_pos[1]] = 0
    return result

def encounterSignal(seeker, beginAStar, potentialSignalArea):
    result = seeker
    result = result.AStar(result.map.hider_signal_pos)
    if result.map.map == beginAStar.map.map:
        return result
    path = []
    temp = None
    hider_pos = None
    while result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    signal_pos = path[0].map.hider_signal_pos
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            signal = path[i].map.hider_signal_pos
            if signal == path[i].seeker_pos:
                pass
            elif signal in path[i].observed:
                path[i].map.map[signal[0]][signal[1]] = 4
            else:
                path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                signal_pos = random.choice(potentialSignalArea)
                while signal_pos == path[i].seeker_pos:
                    signal_pos = random.choice(potentialSignalArea)
            if path[i].seeker_pos != signal_pos:
                path[i].map.map[signal_pos[0]][signal_pos[1]] = 5
            path[i].map.hider_signal_pos = signal_pos
            temp = path[i]
            break
        elif path[i].map.hider_pos in path[i].observed:
            temp = path[i]
            break
        elif i == len(path) - 1:
            temp = path[i]
    result = temp
    if result.map.hider_pos in result.observed:
        beginAStar = Seeker(result.map, result.seeker_pos)
        result = encounterHider(result, beginAStar, potentialSignalArea)
    elif result.map.hider_signal_pos in result.observed:
        beginAStar = Seeker(result.map, result.seeker_pos)
        result = encounterSignal(result, beginAStar, potentialSignalArea)
    return result

def encounterLocalMaximum(seeker, beginAStar, potentialSignalArea):
    result = seeker
    list_unobserved = result.unobserved.copy()
    result = result.BFS(list_unobserved)
    if result.map.map == beginAStar.map.map:
        return encounterLocalMaximum2(seeker, beginAStar, potentialSignalArea)
    temp = None
    path = []
    while  result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    signal_pos = path[0].map.hider_signal_pos
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            signal = path[i].map.hider_signal_pos
            if signal == path[i].seeker_pos:
                pass
            elif signal in path[i].observed:
                path[i].map.map[signal[0]][signal[1]] = 4
            else:
                path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                signal_pos = random.choice(potentialSignalArea)
                while signal_pos == path[i].seeker_pos:
                    signal_pos = random.choice(potentialSignalArea)
            if path[i].seeker_pos != signal_pos:
                path[i].map.map[signal_pos[0]][signal_pos[1]] = 5
            path[i].map.hider_signal_pos = signal_pos
            if len(path[i].unobserved) < len(list_unobserved) or path[i].map.hider_pos in path[i].observed:
                temp = path[i]
                break
        if len(path[i].unobserved) < len(list_unobserved) or path[i].map.hider_pos in path[i].observed:
            temp = path[i]
            break
        if i == len(path) - 1:
            temp = path[i]
    result = temp
    return result

def encounterLocalMaximum2(seeker, beginAStar, potentialSignalArea):
    result = seeker
    list_unobserved = result.unobserved.copy()
    goal_pos = None
    for val in list_unobserved:
        goal_pos = val
        break
    result = result.AStar(goal_pos)
    if result.map.map == beginAStar.map.map:
        return result
    temp = None
    path = []
    while  result.parent != None and result.map.map != beginAStar.map.map:
        path.append(result)
        result = result.parent
    path.reverse()
    signal_pos = path[0].map.hider_signal_pos
    for i in range(len(path)):
        if path[i].map.step >= path[i].map.timeSignal:
            signal = path[i].map.hider_signal_pos
            if signal == path[i].seeker_pos:
                pass
            elif signal in path[i].observed:
                path[i].map.map[signal[0]][signal[1]] = 4
            else:
                path[i].map.map[signal[0]][signal[1]] = 0
            if path[i].map.step % path[i].map.timeSignal == 0:
                signal_pos = random.choice(potentialSignalArea)
                while signal_pos == path[i].seeker_pos:
                    signal_pos = random.choice(potentialSignalArea)
            if path[i].seeker_pos != signal_pos:
                path[i].map.map[signal_pos[0]][signal_pos[1]] = 5
            path[i].map.hider_signal_pos = signal_pos
        if len(path[i].unobserved) < len(list_unobserved) or path[i].map.hider_pos in path[i].observed:
            temp = path[i]
            break
        if i == len(path) - 1:
            temp = path[i]
    result = temp
    return result

def search(seeker, potentialSignalArea):
    result = seeker
    check = False
    while True:
        result = result.hillClimbing(potentialSignalArea)
        beginAStar = Seeker(result.map, result.seeker_pos)
        if result.map.hider_pos in result.observed:
            result = encounterHider(result, beginAStar, potentialSignalArea)
            break
        elif result.map.hider_signal_pos in result.observed and result.calculateManhattanDistance(result.map.hider_signal_pos) <= 2 * result.map.hider_radius:
            result = encounterSignal(result, beginAStar, potentialSignalArea)
            if result.seeker_pos == result.map.hider_pos:
                break
        else:
            result = encounterLocalMaximum(result, beginAStar, potentialSignalArea)
            if result.seeker_pos == result.map.hider_pos:
                break
    return result

def main(fileName = "map1.txt"):
    map2d = Map()
    map2d.read_map(fileName)
    seeker_pos = map2d.get_seeker_pos()
    hider_pos = map2d.get_hider_pos()
    map2d.get_walls_and_obstacles()
    map2d.hider_pos = hider_pos
    map2d.hider_signal_pos = map2d.signal(hider_pos)
    potentialSignalArea = map2d.potentialSignalArea(hider_pos)
    seeker = Seeker(map2d = map2d, seeker_pos = seeker_pos)
    seeker.updateMap()
    result = seeker
    result = search(result, potentialSignalArea)
    path = sk(seeker, result)
    runMapGUI(map2d.map, path)
    print(path[-1].map.step * -1 + 20)