import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Remove this asteroid no matter what
        self.kill()

        # If it's already the smallest size, we're done
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Log the split event
        log_event("asteroid_split")

        # Random angle between 20 and 50 degrees
        angle = random.uniform(20, 50)

        # Create two new velocity vectors
        vel1 = self.velocity.rotate(angle)
        vel2 = self.velocity.rotate(-angle)

        # New radius for the smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Spawn two new asteroids at the same position
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Make them move slightly faster
        a1.velocity = vel1 * 1.2
        a2.velocity = vel2 * 1.2

