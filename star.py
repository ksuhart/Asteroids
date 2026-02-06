import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height

        # tiny white pixel
        self.image = pygame.Surface((2, 2))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.y += self.speed * dt * 60  # consistent speed
        if self.y > 800:  # off screen
            self.y = 0
            self.x = random.randint(0, 800)

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

