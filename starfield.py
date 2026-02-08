import random
from star import Star

class StarField:
    #containers = None  # will be set in main

    def __init__(self, width, height, count=100):
        self.stars =[]

        for _ in range(count):
            x = random.randint(0, width)
            y = random.randint(0, height)
            speed = random.uniform(0.2, 1.0)
            star = Star(x, y, speed, width, height)
            #star.add(*self.containers)
            self.stars.append(star)

    def update(self, dt):
        for star in self.stars:
            star.update(dt)


    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)

    def twinkle(self, time):
        for star in self.stars:
            star.twinkle(time)
