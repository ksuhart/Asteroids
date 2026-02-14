import pygame
import random
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MIN_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MIN_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MIN_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MIN_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_rate = 2.0  # seconds between spawns

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
#        print(f"[FIELD SPAWN] Asteroid radius={radius} at ({position.x:.0f}, {position.y:.0f})")

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            # Pick a random edge
            edge = random.choice(self.edges)
            
            # Get spawn position OFF screen
            spawn_position = edge[1](random.random())
            
            # Calculate velocity TOWARD the play area (opposite of edge direction)
            # This makes asteroids float INTO the screen
            speed = random.randint(40, 100)
            
            # Direction toward center with some randomness
            to_center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) - spawn_position
            to_center = to_center.normalize()
            
            # Add some angle variation (±45 degrees)
            angle_variation = random.uniform(-45, 45)
            velocity = to_center.rotate(angle_variation) * speed
            
            # Random asteroid size
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, spawn_position, velocity)


# Constants (adjust these in your constants.py file if needed)
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
