import pygame
from circleshape import CircleShape

class Powerup(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 12)  # small pickup radius
        self.color = (0, 200, 255)  # cyan glow

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius, 2)
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius - 4, 1)

