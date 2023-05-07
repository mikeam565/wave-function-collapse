import pygame
import tile
from tile import Tile, adjacency
import random
from collections import Counter
import time

pygame.init()
LENGTH = 1000
HEIGHT = 1000
TILE_WIDTH = 10
COLS = LENGTH // TILE_WIDTH
ROWS = LENGTH // TILE_WIDTH

screen = pygame.display.set_mode((LENGTH,HEIGHT))
clock = pygame.time.Clock()
running = True
pause = False
dt = 0
terrain_grid = [[0]*COLS for _ in range(ROWS)]
n = len(terrain_grid)
m = len(terrain_grid[0])

for i in range(n):
    for j in range(m):
        x = i*TILE_WIDTH
        y = j*TILE_WIDTH
        newTile = Tile("NONE", x, y, TILE_WIDTH)
        terrain_grid[i][j] = newTile

curr_terrain = tile.GRASSLAND
terrain_grid[0][0].terrain_type = curr_terrain

# Function that returns all the adjacent elements
def getAdjacent(i, j):
    global terrain_grid
    v = []
    for dx in range (-1 if (i > 0) else 0 , 2 if (i < n-1) else 1):
        for dy in range( -1 if (j > 0) else 0,2 if (j < m-1) else 1):
            if (dx is not 0 or dy is not 0):
                v.append(terrain_grid[i + dx][j + dy])
    return v


# Generate terrain from possible values
def generate(i,j):
    global curr_terrain
    global terrain_grid
    adj = getAdjacent(i,j)
    adj.append(terrain_grid[i][j])
    target = len(adj) # I want len(adj) occurrences of a terrain for it to be considered viable
    allAdj = []
    probabilities = {
        tile.GRASSLAND: 0,
        tile.SAND: 0,
        tile.TREES: 0,
        tile.DENSE_TREES: 0,
        tile.WATER: 0
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
    print(probabilities)
    
    for prob in probabilities:
        probabilities[prob] = probabilities[prob] / len(adj)

    print(probabilities)
    # terrain_grid[i][j].terrain_type = random.choice(keepVals)
    terrain_grid[i][j].terrain_type = random.choices(list(probabilities.keys()), probabilities.values(), k=1)[0]

# Render terrain
def render(i, j):
    global terrain_grid
    curr = terrain_grid[i][j]
    color = tile.colors[curr.terrain_type]
    pygame.draw.rect(screen, color, curr.rect)

def checkquit(e):
    global running, pause
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

i = 0
j = 0
k = 1
render(0,0)
while running:
    i = k // COLS
    j = k % COLS
    events = pygame.event.get()
    checkquit(events)
    if pause:
        continue
    elif i<COLS:
        print(f"---------------iteration {k}------------------")
        generate(i,j)
        render(i,j)
        pygame.display.update()
        k += 1
    else:
        continue
    dt = clock.tick(144) / 1000