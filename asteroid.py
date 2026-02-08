import pygame
import math
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Generate lumpy shape once (in local space)
        self.points = self.generate_shape()

        # Generate craters once (in local space)
        self.craters = []
        num_craters = random.randint(2, 5)
        for _ in range(num_craters):
            angle = random.uniform(0, math.tau)
            dist = random.uniform(0, self.radius * 0.6)
            cx = math.cos(angle) * dist
            cy = math.sin(angle) * dist
            r = random.randint(3, 7)
            self.craters.append((cx, cy, r))

        # Rotation
        self.rotation = 0
        self.rotation_speed = random.uniform(-1.0, 1.0)

        # Pre-render asteroid appearance to a surface
        self.base_image = self.build_base_image()

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

    def build_base_image(self):
        size = self.radius * 2
        center = self.radius

        # Surface with alpha
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Colors
        base_color = (139, 69, 19)      # SaddleBrown
        outline_color = (100, 50, 10)   # Darker brown
        highlight_color = (205, 133, 63)

        # Local polygon points shifted to center
        local_points = []
        for x, y in self.points:
            local_points.append((center + x, center + y))

        # Base polygon fill
        pygame.draw.polygon(surf, base_color, local_points)

        # -----------------------
        # DIRECTIONAL SHADING (polygon-aware, precomputed)
        # -----------------------
        light_dir = pygame.Vector2(-1, -1).normalize()

        # Mask from polygon
        mask = pygame.mask.from_surface(surf)
        shading_surf = pygame.Surface((size, size), pygame.SRCALPHA)

        for py in range(size):
            for px in range(size):
                if mask.get_at((px, py)):
                    vx = px - center
                    vy = py - center
                    v = pygame.Vector2(vx, vy)
                    if v.length() > 0:
                        v = v.normalize()
                        dot = max(0, v.dot(light_dir))  # 0–1
                        shade = int(80 + dot * 80)      # 80–160
                        shading_surf.set_at((px, py), (shade, shade, shade, 255))

        # Multiply shading onto base color
        surf.blit(shading_surf, (0, 0), special_flags=pygame.BLEND_MULT)

        # Outline
        pygame.draw.polygon(surf, outline_color, local_points, width=2)

        # Highlight (shifted toward top-left)
        highlight_points = [(x - 3, y - 3) for (x, y) in local_points]
        pygame.draw.polygon(surf, highlight_color, highlight_points, width=1)

        # Craters (drawn in local space)
        for cx, cy, r in self.craters:
            crater_x = int(center + cx)
            crater_y = int(center + cy)

            pygame.draw.circle(surf, (60, 40, 30), (crater_x, crater_y), r)
            pygame.draw.circle(surf, (30, 20, 15), (crater_x, crater_y), r, 1)
            pygame.draw.circle(surf, (20, 10, 5), (crater_x + 1, crater_y + 1), r - 1)

        # Texture speckles
        for _ in range(10 * max(1, self.radius // 10)):
            tx = random.randint(-self.radius, self.radius)
            ty = random.randint(-self.radius, self.radius)
            if tx * tx + ty * ty <= self.radius * self.radius:
                sx = int(center + tx)
                sy = int(center + ty)
                if 0 <= sx < size and 0 <= sy < size:
                    surf.set_at((sx, sy), (90, 70, 50, 255))

        return surf

    def draw(self, screen):
        # Rotate pre-rendered image
        rotated_image = pygame.transform.rotate(self.base_image, math.degrees(self.rotation))
        rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_image, rect)

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







