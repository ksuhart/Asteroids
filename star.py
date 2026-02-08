import pygame
import random
import math
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

        # twinkle parameters
        self.twinkle_speed = random.uniform(1.0, 3.0)
        self.twinkle_offset = random.uniform(0, 10)


    def update(self, dt):
        self.y += self.speed * dt * 60  # consistent speed
        if self.y > 800:  # off screen
            self.y = 0
            self.x = random.randint(0, self.width)

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def twinkle(self, time):
        # brightness oscillates between 0-255

        brightness = int((math.sin(time * self.twinkle_speed + self.twinkle_offset) + 1) * 127.5)
        self.image.fill((brightness, brightness, brightness))



