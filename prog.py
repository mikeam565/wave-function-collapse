import pygame
import tile
from tile import Tile, adjacency
import random
from collections import Counter
import time

# start pygame
pygame.init()

# CONSTANTS
LENGTH = 1000
HEIGHT = 1000
TILE_WIDTH = 5
COLS = LENGTH // TILE_WIDTH
ROWS = LENGTH // TILE_WIDTH
# STARTING_X = 0
# STARTING_Y = 0
STARTING_X = COLS//2
STARTING_Y = ROWS//2
STARTING_TERRAIN = tile.TREES
BRUSH_WIDTH = 10

# Some vars
screen = pygame.display.set_mode((LENGTH,HEIGHT))
clock = pygame.time.Clock()
running = True
pause = False
mouse_down = False
dt = 0
terrain_grid = [[0]*COLS for _ in range(ROWS)]
n = len(terrain_grid)
m = len(terrain_grid[0])

# Populate 2D grid with Tile objects
for i in range(n):
    for j in range(m):
        x = i*TILE_WIDTH
        y = j*TILE_WIDTH
        newTile = Tile("NONE", x, y, TILE_WIDTH)
        terrain_grid[i][j] = newTile

# Function that returns all the adjacent elements
def getAdjacent(i, j):
    global terrain_grid
    v = []
    for dx in range (-1 if (i > 0) else 0 , 2 if (i < n-1) else 1):
        for dy in range( -1 if (j > 0) else 0,2 if (j < m-1) else 1):
            if (dx != 0 or dy != 0):
                v.append(terrain_grid[i + dx][j + dy])
    return v


# Generate terrain from possible values
def generate(i,j):
    global terrain_grid
    if terrain_grid[i][j].terrain_type != "NONE" or i>ROWS or j>COLS or i<0 or j<0:
        return
    adj = getAdjacent(i,j)
    allNone = True
    for a in adj:
        if a.terrain_type != "NONE":
            allNone = False
    if allNone:
        return
    adj.append(terrain_grid[i][j])
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
    for tle in adj:
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
    
    for prob in probabilities:
        probabilities[prob] = probabilities[prob] / len(adj)

    terrain_grid[i][j].terrain_type = random.choices(list(probabilities.keys()), probabilities.values(), k=1)[0]

# Render terrain
def render(i, j):
    global terrain_grid
    if terrain_grid[i][j].terrain_type == "NONE" or i>ROWS or j>COLS or i<0 or j<0:
        return
    curr = terrain_grid[i][j]
    color = tile.colors[curr.terrain_type]
    pygame.draw.rect(screen, color, curr.rect)

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
            for tle in v:
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
            for tle in v:
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
            for tle in v:
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
            for tle in v:
                if tle.terrain_type != "NONE":
                    countPopulated += 1
            if countPopulated > maxPopulated[-1]:
                max_dx.append(this_dx)
                max_dy.append(this_dy)
                maxPopulated.append(countPopulated)
    # # Introduce small chance the second best is option is picked
    # choice = random.randint(1,10)
    # if choice <= 2 and len(max_dx)>1:
    #     return (i+max_dx[-2],j+max_dy[-2])
    # else:
    #     return (i+max_dx[-1],j+max_dy[-1])
    return (i+max_dx[-1],j+max_dy[-1])

        


# Generate and render first tile
terrain_grid[STARTING_X][STARTING_Y].terrain_type = STARTING_TERRAIN
render(STARTING_X, STARTING_Y)

# ### Pre-render all, going sequentially (only works with starting at 0,0)
# render(0,0)
# for i in range(n):
#     for j in range(m):
#         if not (i==0 and j==0):
#             generate(i,j)
#             render(i,j)

# ### Attempt at writing explorative i,j designator
# i = STARTING_X
# j = STARTING_Y
# flipped = ROWS*COLS - 1 # minus 1 since we already populated one
# k = 1
# while running:
#     events = pygame.event.get()
#     checkinput(events)
#     if pause:
#         continue
#     elif k<(ROWS*COLS-1):
#         print(f"------------iteration {k}--------")
#         generate(i,j)
#         render(i,j)
#         pygame.display.update()
#         (i,j) = findNextCoordinates1(terrain_grid,i,j)
#         print(f"New coordinates {i=},{j=}")
#         k+=1
#     else:
#         continue
#     dt = clock.tick(144) / 1000

i = -1
j = -1
while running:
    events = pygame.event.get()
    checkinput(events)
    if pause:
        continue
    else:
        if mouse_down:
            x, y = pygame.mouse.get_pos()
            i = x // TILE_WIDTH
            j = y // TILE_WIDTH
            for a in range(i-BRUSH_WIDTH,i+BRUSH_WIDTH):
                for b in range(j-BRUSH_WIDTH,j+BRUSH_WIDTH):
                    try:
                        generate(a,b)
                        render(a,b)
                    except Exception as e:
                        print(f"Error trying to generate at {a=}, {b=}")
                        print(e)
                        print("Filling errant spot with border tile...")
                        try:
                            terrain_grid[a][b].terrain_type = tile.CLIFF
                            render(a,b)
                        except Exception as e:
                            print(f"Irresolvable error at {a=},{b=}")
                            print(e)
            pygame.display.update()
    dt = clock.tick(60) / 1000

            


# ### update screen after rendering it all
# while running:
#     events = pygame.event.get()
#     checkinput(events)
#     if pause:
#         continue
#     else:
#         pygame.display.update()
#         continue
#     dt = clock.tick(60) / 1000

### See it happening in game loop (btw this currently double generates the first tile at 0,0)
# i = STARTING_X
# j = STARTING_Y
# k = 1
# render(0,0)
# while running:
#     i = k // COLS
#     j = k % COLS
#     events = pygame.event.get()
#     checkinput(events)
#     if pause:
#         continue
#     elif i<COLS:
#         print(f"---------------iteration {k}------------------")
#         generate(i,j)
#         render(i,j)
#         pygame.display.update()
#         k += 1
#     else:
#         continue
#     dt = clock.tick(144) / 1000