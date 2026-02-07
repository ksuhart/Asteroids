import random
import pygame
from particle import Particle




class ParticleExplosion:
    containers = None  # set in main

    def __init__(self, x, y, count=25):
        for _ in range(count):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 200)
            lifetime = random.uniform(0.8, 1.6)

            # warm asteroid‑y colors
            color = random.choice([
                (255, 200, 50),
                (255, 150, 50),
                (255, 100, 50),
                (255, 255, 255)
            ])

            Particle(x, y, angle, speed, lifetime, color)

        
