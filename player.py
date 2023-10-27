import pygame

class Player():

    def __init__(self, screen, color, position, radius):
        self.screen = screen
        self.color = color
        self.position = position
        self.radius = radius
        self.circle = self.draw_player()

    def draw_player(self):
        return pygame.draw.circle(self.screen, self.color, self.position, self.radius)

    def move_player(self):
        self.circle.move(self.position.x,self.position.y)
    
    def update_pos(self, position):
        old_pos = self.position
        self.position = position
        self.move_player()
        return old_pos