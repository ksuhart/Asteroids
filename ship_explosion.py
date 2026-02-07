import random
import pygame
from shipparticle import ShipParticle

class ShipExplosion:
    containers = None  # set in main

    def __init__(self, x, y):
        # Blue sparks
        for _ in range(25):
            vel = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(200, 400)
            ShipParticle(
                x, y,
                velocity=vel,
                radius=2,
                color=(100, 180, 255),
                lifetime=0.3
            )

        # White-hot core sparks
        for _ in range(15):
            vel = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(150, 250)
            ShipParticle(
                x, y,
                velocity=vel,
                radius=3,
                color=(255, 255, 255),
                lifetime=0.4
            )

        # Orange debris
        for _ in range(12):
            vel = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(80, 180)
            ShipParticle(
                x, y,
                velocity=vel,
                radius=4,
                color=(255, 150, 50),
                lifetime=0.6
            )

