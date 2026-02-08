import pygame
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
import sys


def respawn_player(player):
    player.position.x = SCREEN_WIDTH / 2
    player.position.y = SCREEN_HEIGHT / 2
    player.velocity = pygame.Vector2(0, 0)
    player.rotation = 0


def main():
    print("Starting Asteroids with pygame version: 2.6.1")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    game_state = "start"

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    from ship_explosion import ShipExplosion
    ShipExplosion.containers = (particles, updatable, drawable)
    from shipparticle import ShipParticle
    ShipParticle.containers = (particles, updatable, drawable)
    from starfield import StarField
    #StarField.containers = (updatable, drawable)
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



    while True:
        # ---------------- START SCREEN ----------------
        if game_state == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = "playing"

            screen.fill("black")
            #starfield.update(dt)
            t = pygame.time.get_ticks() / 500
            starfield.twinkle(t)
            starfield.draw(screen)


            title = font.render("ASTEROIDS", True, "white")
            t2 = pygame.time.get_ticks() / 300
            offset = int(10 * math.sin(t))
            title_y = 200 + offset

            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            if blink:
                prompt = font.render("Press SPACE to Start", True, "white")
                #screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
                screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
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

                    for a in asteroids:
                        a.kill()
                    for s in shots:
                        s.kill()

                    asteroid_field = AsteroidField()

                    # Reset starfield
                    from starfield import StarField
                    #StarField.containers = (updatable, drawable)
                    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, count=150)



                    game_state = "playing"

            screen.fill("black")
            #starfield.update(dt)
            t = pygame.time.get_ticks() / 500
            starfield.twinkle(t)
            starfield.draw(screen)
            over = font.render("GAME OVER", True, "white")
            screen.blit(over, (SCREEN_WIDTH // 2 - over.get_width() // 2, 200))
            blink = (pygame.time.get_ticks() // 500) % 2 == 0
            if blink:
                prompt = font.render("Press SPACE to Restart", True, "white")
                #screen.blit(over, (SCREEN_WIDTH // 2 - over.get_width() // 2, 200))
                screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
            pygame.display.flip()
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

            updatable.update(dt)
            for sprite in drawable:
                sprite.draw(screen)

            # Handle delayed respawn
            if respawn_timer > 0:
                respawn_timer -= dt
                if respawn_timer <= 0:

                    # Remove any leftover player sprite
                    for p in updatable:
                        if isinstance(p, Player):
                            p.kill()

                    # Create new player

                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.make_invincible(2)

                  # Skip collision logic until ship is fully respawned
            else:

            # Player–asteroid collision
                for asteroid in asteroids:
                    if player.invincible_timer <= 0 and player.collides_with(asteroid):
                        log_event("player_hit")
                        lives -= 1

                    # Ship explosion BEFORE respawn

                        ShipExplosion(player.position.x, player.position.y)

                        if lives <= 0:
                            game_state = "game_over"
                            break

                    # Remove asteroids too close to respawn point
                        for a in asteroids:
                            if a.position.distance_to(
                                pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            ) < 100:
                                a.kill()

                    # Respawn the player
                    #respawn_player(player)                testing respawn delay code
                    #player.make_invincible(2)

                        respawn_timer = 2.0  # two second delay
                        player.kill()        # hide ship during explosion


                        break

            # Shot–asteroid collision
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()

                        # Spawn explosion BEFORE splitting
                        pos = asteroid.position.copy()
                        ParticleExplosion(pos.x, pos.y)

                        asteroid.split()

                        # add points (only when a shot actually hits)
                        if asteroid.radius > 40:
                            score += 20
                        elif asteroid.radius > 20:
                            score += 50
                        else:
                            score += 100

            # Drawing
            #screen.fill("black")
            for obj in drawable:
                obj.draw(screen)

            score_surface = font.render(f"Score: {score}", True, "white")
            screen.blit(score_surface, (10, 10))

            lives_surface = font.render(f"Lives: {lives}", True, "white")
            screen.blit(lives_surface, (10, 40))

            pygame.display.flip()
            dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()

