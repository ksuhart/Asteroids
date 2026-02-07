import pygame
import random

class ShipParticle(pygame.sprite.Sprite):
    containers = None  # set in main

    def __init__(self, x, y, velocity, radius, color, lifetime):
        super().__init__(self.containers)

        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.timer = 0

        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.kill()
            return

        self.position += self.velocity * dt
        self.rect.center = self.position

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
