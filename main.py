import pygame
import math
import colorsys
import random
import sys

# Initialize pygame FIRST to detect screen
pygame.init()
display_info = pygame.display.Info()

# Update constants BEFORE importing game classes
import constants
constants.SCREEN_WIDTH = display_info.current_w
constants.SCREEN_HEIGHT = display_info.current_h

# NOW import everything else (they'll use the updated constants)
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import PowerUp


def respawn_player(player):
    player.position.x = SCREEN_WIDTH / 2
    player.position.y = SCREEN_HEIGHT / 2
    player.velocity = pygame.Vector2(0, 0)
    player.rotation = 0


def main():
    game_state = "start"
    dying_timer = 0
    fade_alpha = 0
    
    # Screen dimensions already detected and constants updated at module level
    print("Starting Asteroids with pygame version: 2.6.1")
    print(f"Screen width: {SCREEN_WIDTH} (auto-detected)")
    print(f"Screen height: {SCREEN_HEIGHT} (auto-detected)")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    
    from ship_explosion import ShipExplosion
    ShipExplosion.containers = (particles, updatable, drawable)
    from shipparticle import ShipParticle
    ShipParticle.containers = (particles, updatable, drawable)
    from starfield import StarField
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, count=150)

    from particle import Particle
    from particle_explosion import ParticleExplosion

    Particle.containers = (particles, updatable, drawable)

    clock = pygame.time.Clock()
    dt = 0

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    lives = 3
    asteroid_field = AsteroidField()
    score = 0
    respawn_timer = 0
    
    # Weapon upgrade tracking
    current_weapon = 'single'
    weapon_timer = 0

    while True:
        # ---------------- START SCREEN ----------------
        
        if game_state == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = "playing"
    
            screen.fill("black")
            t = pygame.time.get_ticks() / 500
            starfield.twinkle(t)
            starfield.draw(screen)
    
            # Letters on floating asteroids - BIGGER!
            title_text = "ASTEROIDS"
            big_font = pygame.font.SysFont(None, 110)  # HUGE font (was 72)
            letter_spacing = 105  # Much wider spacing (was 70)
            total_width = len(title_text) * letter_spacing
            x_start = SCREEN_WIDTH // 2 - total_width // 2
    
            # Alternating cyan and magenta colors with pulsing
            pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 300)
            
            # Dramatic cyan and magenta
            cyan_brightness = int(200 + 55 * pulse)
            cyan = (0, cyan_brightness, cyan_brightness)
            
            magenta_brightness = int(200 + 55 * pulse)
            magenta = (magenta_brightness, 0, magenta_brightness)
    
            # Pre-generate consistent asteroid shapes (seeded by letter index)
            random.seed(42)  # Fixed seed for consistent shapes
            asteroid_shapes = []
            for i in range(len(title_text)):
                points = []
                num_points = 10  # More points for bigger asteroids
                asteroid_radius = 50  # BIGGER asteroids (was 30)
                for j in range(num_points):
                    angle = (j / num_points) * 2 * math.pi
                    # Fixed random variation per vertex
                    variation = random.randint(-8, 8) if j % 2 == 0 else 0
                    r = asteroid_radius + variation
                    points.append((math.cos(angle) * r, math.sin(angle) * r))
                asteroid_shapes.append(points)
            random.seed()  # Reset seed
    
            # Draw each letter on an asteroid
            for i, letter in enumerate(title_text):
                # Alternate between cyan and magenta
                color = cyan if i % 2 == 0 else magenta
                
                # Individual float and rotation for each asteroid
                time_offset = i * 0.3
                float_y = int(25 * math.sin(pygame.time.get_ticks() / 400 + time_offset))  # Bigger float (was 20)
                rotation = math.sin(pygame.time.get_ticks() / 800 + time_offset) * 0.1
                
                x_pos = x_start + (i * letter_spacing)
                y_pos = 180 + float_y  # Adjusted y position
                
                # Apply rotation to pre-generated shape
                asteroid_points = []
                for px, py in asteroid_shapes[i]:
                    # Rotate point
                    rotated_x = px * math.cos(rotation) - py * math.sin(rotation)
                    rotated_y = px * math.sin(rotation) + py * math.cos(rotation)
                    # Translate to position
                    asteroid_points.append((x_pos + rotated_x, y_pos + rotated_y))
                
                # Draw filled asteroid (dark brown/gray)
                pygame.draw.polygon(screen, (80, 60, 50), asteroid_points)
                # Asteroid outline - thicker for bigger asteroids
                pygame.draw.polygon(screen, (120, 100, 80), asteroid_points, 3)
                
                # Draw letter on top of asteroid
                letter_surface = big_font.render(letter, True, color)
                letter_rect = letter_surface.get_rect(center=(x_pos, y_pos))
                screen.blit(letter_surface, letter_rect)
    
            # Blinking prompt
            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            if blink:
                prompt = font.render("Press SPACE to Start", True, "white")
                screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
                
            # Add instructions
            instructions = [
                "Arrow Keys - Move",
                "Space - Shoot",
                "Collect powerups for weapon upgrades!"
            ]
            y_offset = 380
            for instruction in instructions:
                text = small_font.render(instruction, True, (150, 150, 150))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 30
    
            pygame.display.flip()
            continue

        # ---------------- GAME OVER SCREEN ----------------
        if game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Reset game
                    player.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    lives = 3
                    score = 0
                    current_weapon = 'single'
                    weapon_timer = 0

                    for a in asteroids:
                        a.kill()
                    for s in shots:
                        s.kill()
                    for p in powerups:
                        p.kill()

                    asteroid_field = AsteroidField()
                    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, count=150)

                    game_state = "playing"

            screen.fill("black")
            t = pygame.time.get_ticks() / 500
            starfield.twinkle(t)
            starfield.draw(screen)
            over = font.render("GAME OVER", True, "white")
            screen.blit(over, (SCREEN_WIDTH // 2 - over.get_width() // 2, 200))
            
            final_score = font.render(f"Final Score: {score}", True, "white")
            screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 250))
            
            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            if blink:
                prompt = font.render("Press SPACE to Restart", True, "white")
                screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 350))
            pygame.display.flip()
            continue


        # ---------------- DYING STATE ----------------
        if game_state == "dying":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            dying_timer -= dt
            
            screen.fill("black")
            starfield.update(dt)
            starfield.draw(screen)
            
            updatable.update(dt)
            for obj in drawable:
                obj.draw(screen)

            score_surface = font.render(f"Score: {score}", True, "white")
            screen.blit(score_surface, (10, 10))

            lives_surface = font.render(f"Lives: {lives}", True, "white")
            screen.blit(lives_surface, (10, 40))

            # Fade to black effect
            if dying_timer < 7:
                fade_alpha = int(255 * (1 - dying_timer / 7))
                fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.set_alpha(fade_alpha)
                fade_surface.fill("black")
                screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            dt = clock.tick(60) / 1000

            if dying_timer <= 0:
                game_state = "game_over"
            
            continue

        # ---------------- PLAYING STATE ----------------
        if game_state == "playing":
            log_state()
            screen.fill("black")
            starfield.update(dt)
            starfield.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return  # Exit game when ESC is pressed

            updatable.update(dt)
            for sprite in drawable:
                sprite.draw(screen)

            # Update weapon timer
            if weapon_timer > 0:
                weapon_timer -= dt
                if weapon_timer <= 0:
                    current_weapon = 'single'
                    weapon_timer = 0
                    player.weapon_type = 'single'  # Update player's weapon type!

            # Handle delayed respawn
            if respawn_timer > 0:
                respawn_timer -= dt
                if respawn_timer <= 0:
                    for p in updatable:
                        if isinstance(p, Player):
                            p.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.make_invincible(2)
                    player.weapon_type = current_weapon
            else:
                # Player–powerup collision
                for powerup in list(powerups):
                    if player.collides_with(powerup):
                        current_weapon = powerup.type
                        weapon_timer = powerup.duration
                        player.weapon_type = current_weapon
                        powerup.kill()
                        score += 50
                        log_event(f"powerup_collected_{powerup.type}")

                # Player–asteroid collision
                asteroid_hit = False
                for asteroid in asteroids:
                    if player.invincible_timer <= 0 and player.collides_with(asteroid):
                        log_event("player_hit")
                        lives -= 1

                        ShipExplosion(player.position.x, player.position.y)
                        
                        if lives <= 0:
                            game_state = "dying"
                            dying_timer = 10.0
                            player.kill()
                            break

                        for a in asteroids:
                            if a.position.distance_to(
                                pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            ) < 100:
                                a.kill()

                        respawn_timer = 2.0
                        player.kill()
                        
                        # Reset weapon on death
                        current_weapon = 'single'
                        weapon_timer = 0
                        
                        break
                if asteroid_hit:
                    break

                if game_state == "dying":
                    pygame.display.flip()
                    dt = clock.tick(60) / 1000
                    continue

            # Shot–asteroid collision
            # Process each shot-asteroid collision independently
            for shot in list(shots):
                hit_asteroid = None
                for asteroid in list(asteroids):
                    if shot.collides_with(asteroid):
                        hit_asteroid = asteroid
                        break
                
                if hit_asteroid:
                    log_event("asteroid_shot")
                    shot.kill()

                    pos = hit_asteroid.position.copy()
                    ParticleExplosion(pos.x, pos.y)

                    # Add points BEFORE splitting (check size of current asteroid)
                    if hit_asteroid.radius > 40:
                        score += 20
                    elif hit_asteroid.radius > 20:
                        score += 50
                    else:
                        score += 100

                    # Split the asteroid (this kills it and spawns smaller ones)
                    hit_asteroid.split()

                    # Only spawn powerups as UPGRADES, never downgrades
                    spawn_chance = 0.10  # 10% base chance
                    powerup_type = None
                    
                    if current_weapon == 'spread':
                        # Already have best weapon - no more spawns!
                        spawn_chance = 0.0
                    elif current_weapon == 'triple':
                        # Only allow spread upgrade
                        powerup_type = 'spread'
                    elif current_weapon == 'double':
                        # Only allow triple or spread
                        powerup_type = random.choice(['triple', 'spread'])
                    else:  # single
                        # Can get any upgrade
                        powerup_type = random.choices(
                            ['double', 'triple', 'spread'],
                            weights=[50, 35, 15]  # Double most common, spread rarest
                        )[0]
                    
                    if random.random() < spawn_chance and powerup_type:
                        PowerUp(pos.x, pos.y, powerup_type)

            # Drawing
            for obj in drawable:
                obj.draw(screen)

            # UI
            score_surface = font.render(f"Score: {score}", True, "white")
            screen.blit(score_surface, (10, 10))

            lives_surface = font.render(f"Lives: {lives}", True, "white")
            screen.blit(lives_surface, (10, 40))
            
            # DEBUG: Asteroid count
            #asteroid_count = len(asteroids)
            #debug_surface = small_font.render(f"Asteroids: {asteroid_count}", True, "yellow")
            #screen.blit(debug_surface, (10, 110))
            
            # Weapon display
            weapon_display_y = 70
            if current_weapon != 'single':
                weapon_config = PowerUp.TYPES[current_weapon]
                weapon_text = f"Weapon: {current_weapon.upper()}"
                weapon_surface = small_font.render(weapon_text, True, weapon_config['color'])
                screen.blit(weapon_surface, (10, weapon_display_y))
                
                # Timer bar
                bar_width = 100
                bar_height = 8
                bar_x = 10
                bar_y = weapon_display_y + 25
                
                # Background
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                
                # Fill based on remaining time
                fill_width = int(bar_width * (weapon_timer / weapon_config['duration']))
                pygame.draw.rect(screen, weapon_config['color'], (bar_x, bar_y, fill_width, bar_height))
                
                # Border
                pygame.draw.rect(screen, weapon_config['color'], (bar_x, bar_y, bar_width, bar_height), 1)
                
                # Time remaining
                time_text = small_font.render(f"{weapon_timer:.1f}s", True, "white")
                screen.blit(time_text, (bar_x + bar_width + 10, bar_y - 4))

            pygame.display.flip()
            dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
