import pygame

class Trail():

    def __init__(self, screen, position, radius):
        self.screen = screen
        self.position = position
        self.radius = radius
        
    def draw(self):
        pygame.draw.circle(self.screen, "black", self.position, self.radius)