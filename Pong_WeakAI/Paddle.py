import pygame
import random
from constant import *

class Paddle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen

        self.rect = pygame.Rect(x, y, width, height)
        self.dy = random.choice([-1, 1]) * PADDLE_SPEED 

    def update(self, dt):
        if self.rect.y <= 0 and self.dy < 0:
            self.dy = PADDLE_SPEED  
        
        elif self.rect.y + self.rect.height >= HEIGHT and self.dy > 0:
            self.dy = -PADDLE_SPEED 
        
        self.rect.y += self.dy * dt
        
    def render(self):
        pygame.draw.rect(self.screen, (255, 193, 203), self.rect)