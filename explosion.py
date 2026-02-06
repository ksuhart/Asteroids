import pygame
import math

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.radius = 10
        self.max_radius = 80
        self.lifetime = 0.6  # seconds
        self.timer = 0
        

    def update(self, dt):
        self.timer += dt
        # Expand radius
        self.radius = 5 + (self.max_radius - 5) * (self.timer / self.lifetime)

        if self.timer >= self.lifetime:
            self.kill()
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.position.x), int(self.position.y)),
            int(self.radius),
            3
        )

        # Create a temporary surface for alpha drawing
        #surf = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)
        #pygame.draw.circle(surf, color, (self.max_radius, self.max_radius), int(self.radius), 2)
        #screen.blit(surf, (self.position.x - self.max_radius, self.position.y - self.max_radius))

