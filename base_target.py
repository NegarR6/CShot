import pygame
import random

class Target: # Base class for all targets in the game 

    def __init__(self, x, y, points=5, image_path="pics/Target.jpg"):
        self.x = x
        self.y = y
        self.points = points
        self.active = True

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def hit(self):
        if self.active:
            self.active = False
            return self.points
        return 0

    def respawn(self):
        self.x = random.randint(50, 750)
        self.y = random.randint(50, 550)
        self.active = True