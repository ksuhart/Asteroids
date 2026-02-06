import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, lifetime, color):
        super().__init__(self.containers)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(speed, 0).rotate(angle)
        self.lifetime = lifetime
        self.timer = 0
        self.color = color

        # tiny particle
        self.image = pygame.Surface((3, 3), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (1, 1), 1)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.kill()
            return

        # Move
        self.position += self.velocity * dt * 60
        self.rect.center = self.position

        # Fade out
        fade = (self.timer/self.lifetime) ** 2.5  #slower fade
        alpha = max(0, 255 * (1 - fade))
        self.image.set_alpha(alpha)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

