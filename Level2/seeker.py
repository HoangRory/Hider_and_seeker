from .map import Map
import heapq
import time
import random
import copy
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP_RIGHT = (1, 1)
UP_LEFT = (-1, 1)
DOWN_RIGHT = (1, -1)
DOWN_LEFT = (-1, -1)

class Seeker:
    def __init__(self, map2d, seeker_pos, vision_range = 3, visionCount = 0, path_cost = 0, heuristic_cost = 0, parent = None, unobserved = None):
        self.map = Map(map2d.row, map2d.col, map2d.step, map2d.timeSignal)
        self.map.map = copy.deepcopy(map2d.map)
        self.map.obstacles = map2d.obstacles
        self.map.hider_pos = map2d.hider_pos
        self.seeker_pos = seeker_pos
        self.vision_range = vision_range
        self.visionCount = visionCount
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.parent = parent
        self.observed = set()
        self.unobserved = unobserved
        if unobserved == None:
            self.unobserved = set()
            for i in range(self.map.row):
                for j in range(self.map.col):
                    if self.map.map[i][j] == 0:
                        self.unobserved.add((i, j))
    
    def blockVisionVertical(self, obstacle_pos):
        if self.seeker_pos[1] == obstacle_pos[1]:
            if abs(self.seeker_pos[0] - obstacle_pos[0]) != 1:
                if self.seeker_pos[0] > obstacle_pos[0]:
                    for i in range(self.seeker_pos[0] - self.vision_range, obstacle_pos[0]):
                        if i >= 0 and i < self.map.row:
                            if self.parent == None or (i, self.seeker_pos[1]) not in self.parent.observed:
                                if self.map.map[i][self.seeker_pos[1]] != 1 and self.map.map[i][self.seeker_pos[1]] != -1: 
                                    if self.map.map[i][self.seeker_pos[1]] != 2 and self.map.map[i][self.seeker_pos[1]] != 5:
                                        self.map.map[i][self.seeker_pos[1]] = 0
                                    self.observed.discard((i, self.seeker_pos[1]))
                                    self.unobserved.add((i, self.seeker_pos[1]))
                elif self.seeker_pos[0] < obstacle_pos[0]:
                    for i in range(obstacle_pos[0] + 1, self.seeker_pos[0] + self.vision_range + 1):
                        if i >= 0 and i < self.map.row:
                            if self.parent == None or (i, self.seeker_pos[1]) not in self.parent.observed:
                                if self.map.map[i][self.seeker_pos[1]] != 1 and self.map.map[i][self.seeker_pos[1]] != -1:
                                    if self.map.map[i][self.seeker_pos[1]] != 2 and self.map.map[i][self.seeker_pos[1]] != 5:
                                        self.map.map[i][self.seeker_pos[1]] = 0
                                    self.observed.discard((i, self.seeker_pos[1]))
                                    self.unobserved.add((i, self.seeker_pos[1]))
            else:
                if self.seeker_pos[0] > obstacle_pos[0]:
                    for i in range(self.seeker_pos[0] - self.vision_range, obstacle_pos[0]):
                        if i >= 0 and i < self.map.row:
                            for j in range(self.seeker_pos[1] - (obstacle_pos[0] - i), self.seeker_pos[1] + (obstacle_pos[0] - i) + 1):
                                if j >= 0 and j < self.map.col:
                                    if self.parent == None or (i, j) not in self.parent.observed:
                                        if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                            if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                                self.map.map[i][j] = 0
                                            self.observed.discard((i, j))
                                            self.unobserved.add((i, j))
                else:
                    for i in range(obstacle_pos[0] + 1, self.seeker_pos[0] + self.vision_range + 1):
                        if i >= 0 and i < self.map.row:
                            for j in range(self.seeker_pos[1] - (i - obstacle_pos[0]), self.seeker_pos[1] + (i - obstacle_pos[0]) + 1):
                                if j >= 0 and j < self.map.col:
                                    if self.parent == None or (i, j) not in self.parent.observed:
                                        if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                            if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                                self.map.map[i][j] = 0
                                            self.observed.discard((i, j))
                                            self.unobserved.add((i, j))
    
    def blockVisionHorizontal(self, obstacle_pos):
        if self.seeker_pos[0] == obstacle_pos[0]:
            if abs(self.seeker_pos[1] - obstacle_pos[1]) != 1:
                if self.seeker_pos[1] > obstacle_pos[1]:
                    for j in range(self.seeker_pos[1] - self.vision_range, obstacle_pos[1]):
                        if j >= 0 and j < self.map.col:
                            if self.parent == None or (self.seeker_pos[0], j) not in self.parent.observed:
                                if self.map.map[self.seeker_pos[0]][j] != 1 and self.map.map[self.seeker_pos[0]][j] != -1:
                                    if self.map.map[self.seeker_pos[0]][j] != 2 and self.map.map[self.seeker_pos[0]][j] != 5:
                                        self.map.map[self.seeker_pos[0]][j] = 0
                                    self.observed.discard((self.seeker_pos[0], j))
                                    self.unobserved.add((self.seeker_pos[0], j))
                elif self.seeker_pos[1] < obstacle_pos[1]:
                    for j in range(obstacle_pos[1] + 1, self.seeker_pos[1] + self.vision_range + 1):
                        if j >= 0 and j < self.map.col:
                            if self.parent == None or (self.seeker_pos[0], j) not in self.parent.observed:
                                if self.map.map[self.seeker_pos[0]][j] != 1 and self.map.map[self.seeker_pos[0]][j] != -1:
                                    if self.map.map[self.seeker_pos[0]][j] != 2 and self.map.map[self.seeker_pos[0]][j] != 5:
                                        self.map.map[self.seeker_pos[0]][j] = 0
                                    self.observed.discard((self.seeker_pos[0], j))
                                    self.unobserved.add((self.seeker_pos[0], j))
            else:
                if self.seeker_pos[1] > obstacle_pos[1]:
                    for j in range(self.seeker_pos[1] - self.vision_range, obstacle_pos[1]):
                        if j >= 0 and j < self.map.col:
                            for i in range(self.seeker_pos[0] - (obstacle_pos[1] - j), self.seeker_pos[0] + (obstacle_pos[1] - j) + 1):
                                if i >= 0 and i < self.map.row:
                                    if self.parent == None or (i, j) not in self.parent.observed:
                                        if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                            if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                                self.map.map[i][j] = 0
                                            self.observed.discard((i, j))
                                            self.unobserved.add((i, j))
                else:
                    for j in range(obstacle_pos[1] + 1, self.seeker_pos[1] + self.vision_range + 1):
                        if j >= 0 and j < self.map.col:
                            for i in range(self.seeker_pos[0] - (j - obstacle_pos[1]), self.seeker_pos[0] + (j - obstacle_pos[1]) + 1):
                                if i >= 0 and i < self.map.row:
                                    if self.parent == None or (i, j) not in self.parent.observed:
                                        if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                            if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                                self.map.map[i][j] = 0
                                            self.observed.discard((i, j))
                                            self.unobserved.add((i, j))
    
    def blockDiagonal(self, obstacle_pos):
        if abs(self.seeker_pos[0] - obstacle_pos[0]) == abs(self.seeker_pos[1] - obstacle_pos[1]):
            if self.seeker_pos[0] > obstacle_pos[0] and self.seeker_pos[1] < obstacle_pos[1]:
                for i in range(obstacle_pos[0] - 1, self.seeker_pos[0]  - self.vision_range - 1, -1):
                    for j in range(obstacle_pos[1] + 1, self.seeker_pos[1] + self.vision_range + 1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
            elif self.seeker_pos[0] > obstacle_pos[0] and self.seeker_pos[1] > obstacle_pos[1]:
                for i in range(obstacle_pos[0] - 1, self.seeker_pos[0] - self.vision_range - 1, -1):
                    for j in range(obstacle_pos[1] - 1, self.seeker_pos[1] - self.vision_range - 1, -1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
            elif self.seeker_pos[0] < obstacle_pos[0] and self.seeker_pos[1] < obstacle_pos[1]:
                for i in range(obstacle_pos[0] + 1, self.seeker_pos[0] + self.vision_range + 1):
                    for j in range(obstacle_pos[1] + 1, self.seeker_pos[1] + self.vision_range + 1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
            elif self.seeker_pos[0] < obstacle_pos[0] and self.seeker_pos[1] > obstacle_pos[1]:
                for i in range(obstacle_pos[0] + 1, self.seeker_pos[0] + self.vision_range + 1):
                    for j in range(obstacle_pos[1] - 1, self.seeker_pos[1] - self.vision_range - 1, -1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
        
        elif abs(self.seeker_pos[0] - obstacle_pos[0]) > abs(self.seeker_pos[1] - obstacle_pos[1]):
            if self.seeker_pos[0] > obstacle_pos[0] and self.seeker_pos[1] < obstacle_pos[1]:
                for j in range(obstacle_pos[0] - 1, self.seeker_pos[0] - self.vision_range - 1, -1):
                    for i in range(obstacle_pos[1], self.seeker_pos[1] + self.vision_range):
                        if i >= 0 and i < self.map.col and j >= 0 and j < self.map.row:
                            if self.parent == None or (j, i) not in self.parent.observed:
                                if self.map.map[j][i] != 1 and self.map.map[j][i] != -1:
                                    if self.map.map[j][i] != 2 and self.map.map[j][i] != 5:
                                        self.map.map[j][i] = 0
                                    self.observed.discard((j, i))
                                    self.unobserved.add((j, i))
            elif self.seeker_pos[0] > obstacle_pos[0] and self.seeker_pos[1] > obstacle_pos[1]:
                for j in range(obstacle_pos[0] - 1, self.seeker_pos[0] - self.vision_range - 1, -1):
                    for i in range(obstacle_pos[1], self.seeker_pos[1] - self.vision_range, -1):
                        if i >= 0 and i < self.map.col and j >= 0 and j < self.map.row:
                            if self.parent == None or (j, i) not in self.parent.observed:
                                if self.map.map[j][i] != 1 and self.map.map[j][i] != -1:
                                    if self.map.map[j][i] != 2 and self.map.map[j][i] != 5:
                                        self.map.map[j][i] = 0
                                    self.observed.discard((j, i))
                                    self.unobserved.add((j, i))
            elif self.seeker_pos[0] < obstacle_pos[0] and self.seeker_pos[1] < obstacle_pos[1]:
                for j in range(obstacle_pos[0] + 1, self.seeker_pos[0] + self.vision_range + 1):
                    for i in range(obstacle_pos[1], self.seeker_pos[1] + self.vision_range):
                        if i >= 0 and i < self.map.col and j >= 0 and j < self.map.row:
                            if self.parent == None or (j, i) not in self.parent.observed:
                                if self.map.map[j][i] != 1 and self.map.map[j][i] != -1:
                                    if self.map.map[j][i] != 2 and self.map.map[j][i] != 5:
                                        self.map.map[j][i] = 0
                                    self.observed.discard((j, i))
                                    self.unobserved.add((j, i))
            elif self.seeker_pos[0] < obstacle_pos[0] and self.seeker_pos[1] > obstacle_pos[1]:
                for j in range(obstacle_pos[0] + 1, self.seeker_pos[0] + self.vision_range + 1):
                    for i in range(obstacle_pos[1], self.seeker_pos[1] - self.vision_range, -1):
                        if i >= 0 and i < self.map.col and j >= 0 and j < self.map.row:
                            if self.parent == None or (j, i) not in self.parent.observed:
                                if self.map.map[j][i] != 1 and self.map.map[j][i] != -1:
                                    if self.map.map[j][i] != 2 and self.map.map[j][i] != 5:
                                        self.map.map[j][i] = 0
                                    self.observed.discard((j, i))
                                    self.unobserved.add((j, i))
        
        elif abs(self.seeker_pos[0] - obstacle_pos[0]) < abs(self.seeker_pos[1] - obstacle_pos[1]):
            if self.seeker_pos[0] > obstacle_pos[0] and self.seeker_pos[1] < obstacle_pos[1]:
                for i in range(obstacle_pos[0], self.seeker_pos[0] - self.vision_range, -1):
                    for j in range(obstacle_pos[1] + 1, self.seeker_pos[1] + self.vision_range + 1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
            elif self.seeker_pos[0] > obstacle_pos[0] and self.seeker_pos[1] > obstacle_pos[1]:
                for i in range(obstacle_pos[0], self.seeker_pos[0] - self.vision_range, -1):
                    for j in range(obstacle_pos[1] - 1, self.seeker_pos[1] - self.vision_range - 1, -1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
            elif self.seeker_pos[0] < obstacle_pos[0] and self.seeker_pos[1] < obstacle_pos[1]:
                for i in range(obstacle_pos[0], self.seeker_pos[0] + self.vision_range):
                    for j in range(obstacle_pos[1] + 1, self.seeker_pos[1] + self.vision_range + 1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
            elif self.seeker_pos[0] < obstacle_pos[0] and self.seeker_pos[1] > obstacle_pos[1]:
                for i in range(obstacle_pos[0], self.seeker_pos[0] + self.vision_range):
                    for j in range(obstacle_pos[1] - 1, self.seeker_pos[1] - self.vision_range - 1, -1):
                        if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                            if self.parent == None or (i, j) not in self.parent.observed:
                                if self.map.map[i][j] != 1 and self.map.map[i][j] != -1:
                                    if self.map.map[i][j] != 2 and self.map.map[i][j] != 5:
                                        self.map.map[i][j] = 0
                                    self.observed.discard((i, j))
                                    self.unobserved.add((i, j))
    
    def blockVision(self, obstacle_pos):
        self.blockVisionVertical(obstacle_pos)
        self.blockVisionHorizontal(obstacle_pos)
        self.blockDiagonal(obstacle_pos)
    
    def updateMap(self):
        for i in range(self.seeker_pos[0] - self.vision_range, self.seeker_pos[0] + self.vision_range + 1):
            for j in range(self.seeker_pos[1] - self.vision_range, self.seeker_pos[1] + self.vision_range + 1):
                if i >= 0 and i < self.map.row and j >= 0 and j < self.map.col:
                    if self.map.map[i][j] == 4:
                        self.observed.add((i, j))
                        self.unobserved.discard((i, j))
                    elif self.map.map[i][j] == 0:
                        self.map.map[i][j] = 4
                        self.observed.add((i, j))
                        self.unobserved.discard((i, j))
                    elif self.map.map[i][j] == 2 or self.map.map[i][j] == 5:
                        self.observed.add((i, j))
                        self.unobserved.discard((i, j))
                    elif self.map.map[i][j] == 3:
                        self.map.map[i][j] = 4
                        self.observed.add((i, j))
                        self.unobserved.discard((i, j))
        self.map.map[self.seeker_pos[0]][self.seeker_pos[1]] = 3
        self.observed.add(self.seeker_pos)
        self.unobserved.discard(self.seeker_pos)
        for i in range(self.seeker_pos[0] - self.vision_range, self.seeker_pos[0] + self.vision_range + 1):
            for j in range(self.seeker_pos[1] - self.vision_range, self.seeker_pos[1] + self.vision_range + 1):
                if (i , j) in self.map.obstacles:
                    self.blockVision((i, j))
        if self.parent != None:
            self.observed = self.observed.union(self.parent.observed)
        self.visionCount = len(self.observed)
    
    def checkValidMoves(self):
        valid_moves = []
        for move in [UP, DOWN, LEFT, RIGHT, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT]:
            new_pos = (self.seeker_pos[0] + move[0], self.seeker_pos[1] + move[1])
            if (new_pos[0] >= 0 and new_pos[0] < self.map.row and new_pos[1] >= 0 
            and new_pos[1] < self.map.col and self.map.map[new_pos[0]][new_pos[1]] != 1
            and self.map.map[new_pos[0]][new_pos[1]] != -1):
                valid_moves.append(move)
        return valid_moves
    
    def calculateManhattanDistance(self, pos):
        return abs(self.seeker_pos[0] - pos[0]) + abs(self.seeker_pos[1] - pos[1])
    
    def __lt__(self, other):
        return self.path_cost + self.heuristic_cost < other.path_cost + self.heuristic_cost
    
    def checkGoal(self, goal_pos):
        return self.seeker_pos == goal_pos
    
    def generateNewStates(self):
        new_states = []
        valid_moves = self.checkValidMoves()
        for move in valid_moves:
            new_pos = (self.seeker_pos[0] + move[0], self.seeker_pos[1] + move[1])
            new_state = Seeker(self.map, new_pos, self.vision_range, self.visionCount, unobserved = self.unobserved, parent = self)
            new_state.map.step += 1
            new_state.path_cost = self.path_cost + 1
            new_state.updateMap()
            new_states.append(new_state)
        return new_states
    
    def updateHeuristicForListStates(self, list_states, goal_pos):
        for state in list_states:
            state.heuristic_cost = state.calculateManhattanDistance(goal_pos)
    
    def checkExplored(self, explored):
        return tuple(tuple(row) for row in self.map.map) in explored
        
    def hillClimbing(self, list_potential_hider_signal, current_signal, check = False):
        current_state = self
        if current_state.map.hider_pos.intersection(current_state.observed):
            return current_state, current_signal
        # if check == False:
        #     if current_signal.intersection(current_state.observed):
        #         return current_state, current_signal
        while True:
            new_states = current_state.generateNewStates()
            try:
                new_states[0]
            except IndexError:
                break
            max_vision_count = max(new_states, key = lambda x: x.visionCount).visionCount
            if max_vision_count <= current_state.visionCount:
                break
            best_states = [state for state in new_states if state.visionCount == max_vision_count]
            current_state = random.choice(best_states)
            if current_state.map.step >= current_state.map.timeSignal:
                for signal in current_signal:
                    if signal == current_state.seeker_pos:
                        pass
                    elif signal in current_state.observed:
                        current_state.map.map[signal[0]][signal[1]] = 4
                    else:
                        current_state.map.map[signal[0]][signal[1]] = 0
                if current_state.map.step % current_state.map.timeSignal == 0:
                    current_signal = set()
                    for hider in list_potential_hider_signal:
                        if hider["hider_pos"] in current_state.map.hider_pos:
                            signal = random.choice(hider["potential_signal"])
                            while signal == current_state.seeker_pos:
                                signal = random.choice(hider["potential_signal"])
                            current_signal.add(signal)
                for signal in current_signal:
                    current_state.map.map[signal[0]][signal[1]] = 5
                current_state.map.map[current_state.seeker_pos[0]][current_state.seeker_pos[1]] = 3
            if current_state.map.hider_pos.intersection(current_state.observed) != set():
                break
            # if check == False:
            #     if current_signal.intersection(current_state.observed) != set():
            #         break
        return current_state, current_signal
    
    def AStar(self, goal_pos):
        frontier = []
        heapq.heappush(frontier, self)
        explored = set()
        length_frontier = 1
        while length_frontier > 0:
            current_state = heapq.heappop(frontier)
            length_frontier -= 1
            if current_state.checkExplored(explored):
                continue
            if current_state.checkGoal(goal_pos):
                return current_state
            explored.add(tuple(tuple(row) for row in current_state.map.map))
            new_states = current_state.generateNewStates()
            current_state.updateHeuristicForListStates(new_states, goal_pos)
            for new_state in new_states:
                if not new_state.checkExplored(explored):
                    heapq.heappush(frontier, new_state)
                    length_frontier += 1
        return self

    def BFS(self, list_unobserved):
        frontier = [self]
        explored = set()
        length_frontier = 1
        while length_frontier > 0:
            current_state = heapq.heappop(frontier)
            length_frontier -= 1
            if current_state.checkExplored(explored):
                continue
            if current_state.seeker_pos in list_unobserved:
                return current_state
            explored.add(tuple(tuple(row) for row in current_state.map.map))
            new_states = current_state.generateNewStates()
            for new_state in new_states:
                if not new_state.checkExplored(explored):
                    heapq.heappush(frontier, new_state)
                    length_frontier += 1
        return self

def findSolution(initial_state, result):
    path = []
    if result == None:
        return path
    while result.parent != None:
        path.append(result)
        result = result.parent
    path.append(initial_state)
    path.reverse()
    return path
    