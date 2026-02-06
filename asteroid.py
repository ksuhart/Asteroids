import pygame
import math
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Generate lumpy shape once
        self.points = self.generate_shape()

        # Rotation
        self.rotation = 0
        self.rotation_speed = random.uniform(-1.0, 1.0)

    def generate_shape(self):
        points = []
        num_points = 12

        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi

            offset = random.uniform(-self.radius * 0.3, self.radius * 0.3)
            r = self.radius + offset

            x = math.cos(angle) * r
            y = math.sin(angle) * r
            points.append((x, y))

        return points

    def draw(self, screen):
        rotated = []
        for x, y in self.points:
            rx = x * math.cos(self.rotation) - y * math.sin(self.rotation)
            ry = x * math.sin(self.rotation) + y * math.cos(self.rotation)
            rotated.append((self.position.x + rx, self.position.y + ry))

        pygame.draw.polygon(screen, "white", rotated, width=2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt

    def split(self):
        # Remove this asteroid
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(angle)
        vel2 = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)

        a1.velocity = vel1 * 1.2
        a2.velocity = vel2 * 1.2

