import pygame
from constants import (PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT,)

from circleshape import CircleShape
from shot import Shot




class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.invincible_timer = 0

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

        # Spawn shot at the nose of the ship

        #shot = Shot(self.position.x, self.position.y)
        shot = Shot(
            self.position.x + forward.x * self.radius,
            self.position.y + forward.y * self.radius
        )

        direction = pygame.Vector2(0, -1).rotate(self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED




    def make_invincible(self, seconds):
        self.invincible_timer = seconds
