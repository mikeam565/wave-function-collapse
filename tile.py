import pygame

GRASSLAND = "grassland"
SAND = "sand"
TREES = "trees"
DENSE_TREES = "dense_trees"
WATER = "water"

colors = {
    GRASSLAND: "green",
    SAND: "tan",
    TREES: "dark green",
    DENSE_TREES: "brown",
    WATER: "blue"
}

adjacency = {
    GRASSLAND: {
        GRASSLAND: 0.5,
        TREES: 0.25,
        SAND: 0.25
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
        DENSE_TREES: 0.5,
        TREES: 0.5,
    },
    WATER: {
        WATER: 0.9,
        SAND: 0.1
    },
    "NONE": {
        GRASSLAND: 0,
        SAND: 0,
        TREES: 0,
        DENSE_TREES: 0,
        WATER: 0
    }
}

class Tile:

    def __init__(self, terrain_type, x, y, width):
        print(f"Tile created at ({x},{y}) with terrain {terrain_type} and width {width}")
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