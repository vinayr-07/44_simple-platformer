import pygame

class Player:
    def __init__(self, x, y, width=24, height=32):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.speed = 4
        self.jump_strength = -12
        self.on_ground = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
