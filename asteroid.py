import pygame
import math
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Generate lumpy shape once
        self.points = self.generate_shape()

        #Generate craters once
        self.craters = []
        num_craters = random.randint(2, 5)

        for _ in range(num_craters):
            angle = random.uniform(0, math.tau)
            dist = random.uniform(0, self.radius * 0.6)

            # crater center in local asteriod space
            cx = math.cos(angle) * dist
            cy = math.sin(angle) * dist
            r = random.randint(3, 7)

            self.craters.append((cx, cy, r))


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

        # Base asteroid color (brown)
        base_color = (139, 69, 19)      # SaddleBrown
        outline_color = (100, 50, 10)   # Darker brown
        highlight_color = (205, 133, 63)

        # Draw filled polygon
        pygame.draw.polygon(screen, base_color, rotated)

    # RADIAL SHADING (3D effect)
    # -----------------------
        for i in range(self.radius, 0, -1):
            t = i / self.radius
            shade = int(139 - t * 60)
            shade = max(40, min(200, shade))
            pygame.draw.circle(
                screen,
                (shade, shade // 2, shade // 3),
                (int(self.position.x), int(self.position.y)),
                i
            )






        # Draw outline
        pygame.draw.polygon(screen, outline_color, rotated, width=2)

        # Simple shading: highlight on the "sunlit" side
        highlight = [(x - 3, y - 3) for (x, y) in rotated]
        #for x, y in rotated:
            # shift points slightly toward top-left for highlight
            #highlight.append((x - 3, y - 3))

        #highlight_color = (205, 133, 63)  # Peru (lighter brown)
        pygame.draw.polygon(screen, highlight_color, highlight, width=1)


    # -----------------------
    # CRATERS (rotated)
    # -----------------------
        for cx, cy, r in self.craters:
        # rotate crater center
            rx = cx * math.cos(self.rotation) - cy * math.sin(self.rotation)
            ry = cx * math.sin(self.rotation) + cy * math.cos(self.rotation)

            crater_x = int(self.position.x + rx)
            crater_y = int(self.position.y + ry)

        # dark crater fill
            pygame.draw.circle(screen, (60, 40, 30), (crater_x, crater_y), r)

        # crater rim
            pygame.draw.circle(screen, (30, 20, 15), (crater_x, crater_y), r, 1)

        # inner shadow for depth
            pygame.draw.circle(screen, (20, 10, 5), (crater_x + 1, crater_y + 1), r - 1)

    # -----------------------
    # TEXTURE (random speckles)
    # -----------------------
        for _ in range(10):
            tx = random.randint(-self.radius, self.radius)
            ty = random.randint(-self.radius, self.radius)

            if tx * tx + ty * ty <= self.radius * self.radius:
                screen.set_at(
                    (int(self.position.x + tx), int(self.position.y + ty)),
                    (90, 70, 50)
                )






    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        # Wrap around screen
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH

        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT




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

