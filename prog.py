import collections
from queue import PriorityQueue
import pygame
import tile
from tile import Tile, adjacency
import random
from collections import Counter
import time
import math
import player as pl
from trail import Trail


#################################################################################################
### Initialization ##############################################################################
#################################################################################################

# start pygame
pygame.init()

# CONSTANTS
LENGTH = 1000
HEIGHT = 1000
TILE_WIDTH = 10
COLS = LENGTH // TILE_WIDTH
ROWS = LENGTH // TILE_WIDTH
# STARTING_X = 0
# STARTING_Y = 0
STARTING_X = COLS//2
STARTING_Y = ROWS//2
STARTING_TERRAIN = tile.GRASSLAND
BRUSH_WIDTH = 10
countFilled = 1
PLAYER_CENTERING = TILE_WIDTH // 2
diagonalMovement = {
    (1,1):True,
    (1,-1):True,
    (-1,1):True,
    (-1,-1):True
}

# Some vars
screen = pygame.display.set_mode((LENGTH,HEIGHT))
clock = pygame.time.Clock()
running = True
pause = False
mouse_down = False
dt = 0
terrain_grid = [[0]*COLS for _ in range(ROWS)]
adjacent_tiles = [[0]*COLS for _ in range(ROWS)]
n = len(terrain_grid)
m = len(terrain_grid[0])
player_pos = pygame.Vector2(screen.get_width() // 2 + PLAYER_CENTERING, screen.get_height() // 2 + PLAYER_CENTERING)

# Populate 2D grid with Tile objects
for i in range(n):
    for j in range(m):
        x = i*TILE_WIDTH
        y = j*TILE_WIDTH
        newTile = Tile("NONE", i, j, x, y, TILE_WIDTH)
        terrain_grid[i][j] = newTile

#################################################################################################
### Terrain Generation ##########################################################################
#################################################################################################

# Function that returns all the adjacent elements
def getAdjacent(i,j):
    global terrain_grid
    global adjacent_tiles
    global n, m
    global diagonalMovement
    if isinstance(adjacent_tiles[i][j], list):
        return adjacent_tiles[i][j]
    v = []
    for (di,dj) in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
        if (i+di)>=0 and (i+di)<len(terrain_grid) and (j+dj)>=0 and (j+dj)<len(terrain_grid[i+di]):
            v.append((terrain_grid[i + di][j + dj],(di,dj) in diagonalMovement))
    adjacent_tiles[i][j] = v
    return v

# Generate terrain from possible values
def generate(i,j):
    global terrain_grid, countFilled
    if terrain_grid[i][j].terrain_type != "NONE" or i>ROWS or j>COLS or i<0 or j<0:
        return
    adj = getAdjacent(i,j)
    allNone = True
    for (a,_) in adj:
        if a.terrain_type != "NONE":
            allNone = False
    if allNone:
        return
    adj.append((terrain_grid[i][j],False))
    target = len(adj) # I want len(adj) occurrences of a terrain for it to be considered viable
    allAdj = []
    probabilities = {
        tile.GRASSLAND: 0,
        tile.SAND: 0,
        tile.TREES: 0,
        tile.DENSE_TREES: 0,
        tile.WATER: 0,
        tile.DEEP_WATER: 0
    }
    for (tle,_) in adj:
        for typ in adjacency[tle.terrain_type]:
            probabilities[typ] += adjacency[tle.terrain_type][typ]
        allAdj += list(adjacency[tle.terrain_type].keys())
    counts = Counter(allAdj)
    keepVals = []
    for cnt in counts:
        if counts[cnt] >= target:
            keepVals.append(cnt)
    
    for val in [v for v in probabilities if v not in keepVals]:
        del probabilities[val]
    
    if probabilities:
        for prob in probabilities:
            probabilities[prob] = probabilities[prob] / len(adj)
        terrain_grid[i][j].terrain_type = random.choices(list(probabilities.keys()), probabilities.values(), k=1)[0]
    else: # If impossible arrangement occurs, assume cliff
        terrain_grid[i][j].terrain_type = tile.CLIFF
    countFilled += 1

#################################################################################################
### Rendering ###################################################################################
#################################################################################################

# Render tile based off it's current terrain_type
def render(i, j):
    global terrain_grid
    if terrain_grid[i][j].terrain_type == "NONE" or i>ROWS or j>COLS or i<0 or j<0:
        return
    curr = terrain_grid[i][j]
    color = tile.colors[curr.terrain_type]
    pygame.draw.rect(screen, color, curr.rect)

### Pre-render all in quadrants
def render_screen():
    render(STARTING_X,STARTING_Y)
    for i in range(STARTING_X, n):
        for j in range(STARTING_Y, m):
            generate(i,j)
            render(i,j)
    for i in range(STARTING_X, -1, -1):
        for j in range(STARTING_Y, -1, -1):
            generate(i,j)
            render(i,j)
    for i in range(STARTING_X, -1, -1):
        for j in range(STARTING_Y, m):
            generate(i,j)
            render(i,j)
    for i in range(STARTING_X, n):
        for j in range(STARTING_Y, -1, -1):
            generate(i,j)
            render(i,j)

#################################################################################################
### Input Checking ##############################################################################
#################################################################################################
def checkinput(e):
    global running, pause, mouse_down
    for ev in e:
        if ev.type == pygame.QUIT:
            exit(0)
            running = True
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if pause:
                pause = False
            else:
                quit(0)
                running = True
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
            pause = not pause
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

#################################################################################################
### Tile Selection ##############################################################################
#################################################################################################

def findNextCoordinates1(terrain_grid, i,j):
    temp_i = i
    temp_j = j
    max_dx = [0]
    max_dy = [0]
    maxPopulated = [0]
    # Check right
    this_dx = 1
    this_dy = 0
    temp_i = i + this_dx
    temp_j = j + this_dy
    if temp_i < COLS:
        if terrain_grid[temp_i][temp_j].terrain_type == "NONE":
            v = getAdjacent(temp_i, temp_j)
            countPopulated = 0
            for (tle,_) in v:
                if tle.terrain_type != "NONE":
                    countPopulated += 1
            if countPopulated > maxPopulated[-1]:
                max_dx.append(this_dx)
                max_dy.append(this_dy)
                maxPopulated.append(countPopulated)
    # Check down
    this_dx = 0
    this_dy = 1
    temp_i = i + this_dx
    temp_j = j + this_dy
    if temp_j < ROWS:
        if terrain_grid[temp_i][temp_j].terrain_type == "NONE":
            v = getAdjacent(temp_i, temp_j)
            countPopulated = 0
            for (tle,_) in v:
                if tle.terrain_type != "NONE":
                    countPopulated += 1
            if countPopulated > maxPopulated[-1]:
                max_dx.append(this_dx)
                max_dy.append(this_dy)
                maxPopulated.append(countPopulated)
    # Check left
    this_dx = -1
    this_dy = 0
    temp_i = i + this_dx
    temp_j = j + this_dy
    if temp_i >= 0:
        if terrain_grid[temp_i][temp_j].terrain_type == "NONE":
            v = getAdjacent(temp_i, temp_j)
            countPopulated = 0
            for (tle,_) in v:
                if tle.terrain_type != "NONE":
                    countPopulated += 1
            if countPopulated > maxPopulated[-1]:
                max_dx.append(this_dx)
                max_dy.append(this_dy)
                maxPopulated.append(countPopulated)
    # Check up
    this_dx = 0
    this_dy = -1
    temp_i = i + this_dx
    temp_j = j + this_dy
    if temp_j >= 0:
        if terrain_grid[temp_i][temp_j].terrain_type == "NONE":
            v = getAdjacent(temp_i, temp_j)
            countPopulated = 0
            for (tle,_) in v:
                if tle.terrain_type != "NONE":
                    countPopulated += 1
            if countPopulated > maxPopulated[-1]:
                max_dx.append(this_dx)
                max_dy.append(this_dy)
                maxPopulated.append(countPopulated)
    # Introduce small chance the second best is option is picked (TODO: Fix getting stuck)
    choice = random.randint(1,10)
    if choice <= 4 and len(max_dx)>1:
        return (i+max_dx[-2],j+max_dy[-2])
    else:
        return (i+max_dx[-1],j+max_dy[-1])
    # return (i+max_dx[-1],j+max_dy[-1]) 

# ### Attempt at writing explorative i,j designator
def explorative_generation():
    i = STARTING_X
    j = STARTING_Y
    flipped = ROWS*COLS - 1 # minus 1 since we already populated one
    k = 1
    while running:
        events = pygame.event.get()
        checkinput(events)
        if pause:
            continue
        elif k<(ROWS*COLS-1):
            generate(i,j)
            render(i,j)
            pygame.display.update()
            (i,j) = findNextCoordinates1(terrain_grid,i,j)
            k+=1
        else:
            continue
        dt = clock.tick(144) / 1000

def user_draw():
    global countFilled, terrain_grid, player_pos
    i = -1
    j = -1
    path = None
    curr = None
    trails = []
    while running:
        events = pygame.event.get()
        checkinput(events)
        if pause:
            continue
        else:
            if countFilled < (COLS*ROWS)-6: # 
                if mouse_down:
                    x, y = pygame.mouse.get_pos()
                    i = x // TILE_WIDTH
                    j = y // TILE_WIDTH
                    for a in range(i-BRUSH_WIDTH,i+BRUSH_WIDTH):
                        for b in range(j-BRUSH_WIDTH+abs(i-a),j+BRUSH_WIDTH-abs(i-a)):
                            if a<len(terrain_grid) and b<len(terrain_grid[0]):
                                generate(a,b)
                                render(a,b)
            else:
                # put a lil guy down
                screen.fill("black")
                render_screen()
                for trail in trails:
                    trail.draw()
                player = pl.Player(screen, "red", player_pos, TILE_WIDTH//2)
                if not path and pygame.mouse.get_pressed()[2]:
                    # Get dx and dy to location
                    x2,y2 = pygame.mouse.get_pos()
                    i1 = player_pos.x // TILE_WIDTH
                    j1 = player_pos.y // TILE_WIDTH
                    i2 = x2 // TILE_WIDTH
                    j2 = y2 // TILE_WIDTH
                    if not path:
                        print(f"Finding path from ({i1},{j1}) to ({i2},{j2})...")
                        path = findPath(int(i2),int(j2),int(i1),int(j1))
                        print("Path found!")
                        curr = terrain_grid[int(i1)][int(j1)]
                if path and curr in path:
                    curr = path[curr]
                    if curr:
                        player_pos.x = curr.x + PLAYER_CENTERING
                        player_pos.y = curr.y + PLAYER_CENTERING
                        (old_x,old_y) = player.update_pos(player_pos)
                        trail_pos = (int(old_x), int(old_y))
                        trails.append(Trail(screen, trail_pos, TILE_WIDTH//2))                
                    else:
                        path = None
        pygame.display.update()
        clock.tick(30)

### update screen with pause
def update_screen_with_pause():
    while running:
        events = pygame.event.get()
        checkinput(events)
        if pause:
            continue
        else:
            pygame.display.update()
        dt = clock.tick(60) / 1000

### See it happening in game loop (btw this currently double generates the first tile at 0,0)
def live_draw():
    i = STARTING_X
    j = STARTING_Y
    k = 1
    render(STARTING_X,STARTING_Y)
    while running:
        i = k // COLS
        j = k % COLS
        events = pygame.event.get()
        checkinput(events)
        if pause:
            continue
        elif i<COLS:
            generate(i,j)
            render(i,j)
            pygame.display.update()
            k += 1
        else:
            continue
        dt = clock.tick(144) / 1000

#################################################################################################
### Path-finding functions ######################################################################
#################################################################################################

def path_heuristic(t1, t2):
    return abs(t1.x - t2.x) + abs(t1.y - t2.y)
    # return 0

# ref: https://www.redblobgames.com/pathfinding/a-star/introduction.html
def findPath(i1,j1,i2,j2):
    global terrain_grid
    global player_pos
    start_node = terrain_grid[i1][j1]
    end_node = terrain_grid[i2][j2]
    frontier = PriorityQueue()
    frontier.put(start_node, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_node] = None
    cost_so_far[start_node] = 0
    while not frontier.empty():
        current = frontier.get()
        if current == end_node:
            break
        for (nxt,isDiagMov) in getAdjacent(current.i, current.j):
            diag_cost = (1+math.sqrt(2)) if isDiagMov else 1
            new_cost = cost_so_far[current] + (tile.MOVEMENT_COSTS[current.terrain_type] * diag_cost)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + path_heuristic(end_node, nxt)
                frontier.put(nxt, priority)
                came_from[nxt] = current
    return came_from




# Generate and render starting tile
terrain_grid[STARTING_X][STARTING_Y].terrain_type = STARTING_TERRAIN
render(STARTING_X, STARTING_Y)
#################################################################################################
### Select style of drawing here ################################################################
#################################################################################################

## Render in quadrants from STARTING_X, _Y
render_screen()
# update_screen_with_pause()

### Draw in order live
# live_draw() # Only works with STARTING_X and _Y of 0,0 currently

### attempts an exploration of adjacent tiles. Currently gets stuck.
# explorative_generation()

### User draws from origin node, then after enough boxes drawn, lets us pathfind through terrain
user_draw()