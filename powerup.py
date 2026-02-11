import pygame
import random
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PowerUp(CircleShape):
    containers = ()
    
    TYPES = {
        'double': {'color': (0, 150, 255), 'symbol': '==', 'duration': 10},
        'triple': {'color': (255, 150, 0), 'symbol': '≡', 'duration': 12},
        'spread': {'color': (255, 50, 255), 'symbol': '***', 'duration': 15},
    }
    
    def __init__(self, x, y, powerup_type=None):
        super().__init__(x, y, 20)
        
        if powerup_type is None:
            powerup_type = random.choice(list(self.TYPES.keys()))
        
        self.type = powerup_type
        self.config = self.TYPES[powerup_type]
        self.color = self.config['color']
        self.symbol = self.config['symbol']
        self.duration = self.config['duration']
        
        # Floating animation
        self.float_offset = 0
        self.pulse = 0
        
        # Drift slowly
        angle = random.random() * 3.14159 * 2
        speed = 20
        self.velocity = pygame.Vector2(
            speed * pygame.math.Vector2(1, 0).rotate(angle).x,
            speed * pygame.math.Vector2(1, 0).rotate(angle).y
        )
        
        # Lifetime (despawn after 15 seconds)
        self.lifetime = 15.0
    
    def update(self, dt):
        # Move
        self.position += self.velocity * dt
        
        # Wrap around screen
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        
        # Animation
        self.float_offset += dt * 3
        self.pulse += dt * 5
        
        # Lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
    
    def draw(self, screen):
        # Pulsing effect
        pulse_size = 1 + 0.2 * pygame.math.Vector2(1, 0).rotate(self.pulse * 50).x
        radius = int(self.radius * pulse_size)
        
        # Floating offset
        float_y = int(5 * pygame.math.Vector2(1, 0).rotate(self.float_offset * 50).y)
        draw_pos = (int(self.position.x), int(self.position.y + float_y))
        
        # Outer glow
        glow_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(screen, glow_color, draw_pos, radius + 3, 2)
        
        # Main circle
        pygame.draw.circle(screen, self.color, draw_pos, radius, 3)
        
        # Symbol
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.symbol, True, self.color)
        text_rect = text.get_rect(center=draw_pos)
        screen.blit(text, text_rect)
        
        # Flashing indicator if about to expire
        if self.lifetime < 3:
            if int(self.lifetime * 4) % 2 == 0:
                pygame.draw.circle(screen, (255, 255, 255), draw_pos, radius + 5, 1)
