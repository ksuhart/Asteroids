import pygame
from constants import (PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT,)
import math
from circleshape import CircleShape
from shot import Shot




class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.invincible_timer = 0
        self.weapon_type = 'single'  #adding single, double, triple and spread weapons

    def ship_shape(self):
        # Define ship points in local space (pointing up)
        points = [
            pygame.Vector2(0, -self.radius),  #nose
            pygame.Vector2(self.radius * 0.6, self.radius * 0.5), # right wing
            pygame.Vector2(0, self.radius * 0.2), # tail notch
            pygame.Vector2(-self.radius * 0.6, self.radius * 0.5), #left wing
        ]

        # Rotate and translate points
        rotated = [p.rotate(self.rotation) + self.position for p in points]
        return rotated


    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):

        # NEW: Change ship color based on weapon type
        color = "white"
        if self.weapon_type == 'double':
            color = (0, 150, 255)  # Blue
        elif self.weapon_type == 'triple':
            color = (255, 150, 0)  # Orange
        elif self.weapon_type == 'spread':
            color = (255, 50, 255)  # Magenta
        
        # Flash when invincible
        if self.invincible_timer > 0:
            if int(self.invincible_timer * 10) % 2 == 0:
                return  # Don't draw (flashing effect)

        pygame.draw.polygon(screen, "white", self.ship_shape(), LINE_WIDTH)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def update(self, dt):
        self.position += self.velocity * dt

        # wrap
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH

        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)  #rotate left
        if keys[pygame.K_d]:
            self.rotate(dt)   #rotate right
        if keys[pygame.K_w]:
            self.move(dt)     #move forward
        if keys[pygame.K_s]:
            self.move(-dt)    #move backward
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if self.invincible_timer > 0:
            self.invincible_timer -= dt



    
    def shoot(self):
        if self.shoot_timer > 0:
            return

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Ship nose points UP now
        forward = pygame.Vector2(0, -1).rotate(self.rotation)

        # Spawn position at nose of ship
        spawn_x = self.position.x + forward.x * self.radius
        spawn_y = self.position.y + forward.y * self.radius

        # NEW: Different shooting patterns based on weapon type
        if self.weapon_type == 'single':
            # Standard single shot
            shot = Shot(spawn_x, spawn_y)
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            
        elif self.weapon_type == 'double':
            # Two shots side by side
            right = pygame.Vector2(0, -1).rotate(self.rotation + 90)
            offset = self.radius * 0.4
            
            # Left shot
            shot1 = Shot(
                spawn_x + right.x * offset,
                spawn_y + right.y * offset
            )
            direction = pygame.Vector2(0, -1).rotate(self.rotation)
            shot1.velocity = direction * PLAYER_SHOOT_SPEED
            
            # Right shot
            shot2 = Shot(
                spawn_x - right.x * offset,
                spawn_y - right.y * offset
            )
            shot2.velocity = direction * PLAYER_SHOOT_SPEED
            
        elif self.weapon_type == 'triple':
            # Three shots in a spread pattern (center + 15° left + 15° right)
            
            # Center shot
            shot_center = Shot(spawn_x, spawn_y)
            direction_center = pygame.Vector2(0, -1).rotate(self.rotation)
            shot_center.velocity = direction_center * PLAYER_SHOOT_SPEED
            
            # Left shot (15 degrees)
            shot_left = Shot(spawn_x, spawn_y)
            direction_left = pygame.Vector2(0, -1).rotate(self.rotation - 15)
            shot_left.velocity = direction_left * PLAYER_SHOOT_SPEED
            
            # Right shot (15 degrees)
            shot_right = Shot(spawn_x, spawn_y)
            direction_right = pygame.Vector2(0, -1).rotate(self.rotation + 15)
            shot_right.velocity = direction_right * PLAYER_SHOOT_SPEED
            
        elif self.weapon_type == 'spread':
            # Five shots in a wide spread (30° between each)
            angles = [-30, -15, 0, 15, 30]
            
            for angle_offset in angles:
                shot = Shot(spawn_x, spawn_y)
                direction = pygame.Vector2(0, -1).rotate(self.rotation + angle_offset)
                shot.velocity = direction * PLAYER_SHOOT_SPEED




    def make_invincible(self, seconds):
        self.invincible_timer = seconds


  # ========== TRIANGULAR COLLISION DETECTION ==========
    
    def collides_with(self, other):
        # Get triangle vertices
        triangle = self.triangle()
        
        # Method 1: Check if circle center is inside triangle
        if self._point_in_triangle(other.position, triangle):
            return True
        
        # Method 2: Check distance from circle center to each edge
        for i in range(3):
            p1 = triangle[i]
            p2 = triangle[(i + 1) % 3]
            
            # Distance from circle center to line segment
            dist = self._point_to_segment_distance(other.position, p1, p2)
            if dist < other.radius:
                return True
        
        return False

    def _point_to_segment_distance(self, point, seg_a, seg_b):
        # Calculate distance from point to line segment
        line_vec = seg_b - seg_a
        point_vec = point - seg_a
        line_len = line_vec.length()
        
        if line_len == 0:
            return point_vec.length()
        
        # Project point onto line
        t = max(0, min(1, point_vec.dot(line_vec) / (line_len * line_len)))
        projection = seg_a + line_vec * t
        
        return (point - projection).length()

    def _point_in_triangle(self, point, triangle):
        a, b, c = triangle
        
        v0 = c - a
        v1 = b - a
        v2 = point - a
        
        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)
        
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        return (u >= 0) and (v >= 0) and (u + v < 1)

