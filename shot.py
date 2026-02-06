import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT



class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        if (
            self.position.x < 0 or self.position.x > SCREEN_WIDTH or
            self.position.y < 0 or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()



        # wrap
        #if self.position.x < 0:
        #    self.position.x += SCREEN_WIDTH
        #elif self.position.x > SCREEN_WIDTH:
        #    self.position.x -= SCREEN_WIDTH

        #if self.position.y < 0:
        #    self.position.y += SCREEN_HEIGHT
        #elif self.position.y > SCREEN_HEIGHT:
        #    self.position.y -= SCREEN_HEIGHT

