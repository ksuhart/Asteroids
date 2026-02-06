import random
from star import Star

class StarField:
    containers = None  # will be set in main

    def __init__(self, width, height, count=100):
        for _ in range(count):
            x = random.randint(0, width)
            y = random.randint(0, height)
            speed = random.uniform(0.2, 1.0)
            Star(x, y, speed, width, height).add(*self.containers)

