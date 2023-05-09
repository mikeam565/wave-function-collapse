import pygame

GRASSLAND = "grassland"
SAND = "sand"
TREES = "trees"
DENSE_TREES = "dense_trees"
WATER = "water"
DEEP_WATER = "deep_water"
CLIFF = "cliff"

## Terrain colors
colors = {
    GRASSLAND: "green2",
    SAND: "tan",
    TREES: "green4",
    DENSE_TREES: "darkgreen",
    WATER: "blue",
    DEEP_WATER: "darkblue",
    CLIFF: "brown"
}

# ### Other colors for fun
# colors = {
#     GRASSLAND: "yellow",
#     SAND: "green",
#     TREES: "orange",
#     DENSE_TREES: "red",
#     WATER: "blue",
#     DEEP_WATER: "indigo"
# }


adjacency = {
    GRASSLAND: {
        GRASSLAND: 0.8,
        TREES: 0.1,
        SAND: 0.1
    },
    SAND: {
        SAND: 0.5,
        GRASSLAND: 0.25,
        WATER: 0.25
    },
    TREES: {
        TREES: 0.5,
        GRASSLAND: 0.25,
        DENSE_TREES: 0.25
    },
    DENSE_TREES: {
        DENSE_TREES: 0.8,
        TREES: 0.2,
    },
    WATER: {
        WATER: 0.8,
        DEEP_WATER: 0.12,
        SAND: 0.08
    },
    DEEP_WATER: {
        DEEP_WATER: 0.9,
        WATER: 0.1
    },
    CLIFF: {
        GRASSLAND:1,
        SAND:1,
        TREES:1,
        DENSE_TREES:1,
        WATER:1,
        DEEP_WATER:1
    },
    "NONE": {
        GRASSLAND: 0,
        SAND: 0,
        TREES: 0,
        DENSE_TREES: 0,
        WATER: 0,
        DEEP_WATER: 0
    }
}

class Tile:

    def __init__(self, terrain_type, x, y, width):
        # print(f"Tile created at ({x},{y}) with terrain {terrain_type} and width {width}")
        self.terrain_type = terrain_type
        self.x = x
        self.y = y
        self.width = width
        self.rect = pygame.Rect(x, y, width, width)

    def __repr__(self):
        return f"Tile at {self.x=}, {self.y} with {self.terrain_type=}"

    def setX(self, x):
        self.x = x
        self.rect.left = x
    
    def setY(self, y):
        self.y = y
        self.rect.top = y