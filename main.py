import pygame
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

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)

    from starfield import StarField
    StarField.containers = (updatable, drawable)
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, count=150)

    from particle import Particle
    from particle_explosion import ParticleExplosion

    Particle.containers = (updatable, drawable)



    clock = pygame.time.Clock()
    dt = 0

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    lives = 3
    asteroid_field = AsteroidField()
    score = 0

    while True:
        # ---------------- START SCREEN ----------------
        if game_state == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = "playing"

            screen.fill("black")
            title = font.render("ASTEROIDS", True, "white")
            prompt = font.render("Press SPACE to Start", True, "white")
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
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
                    StarField.containers = (updatable, drawable)
                    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, count=150)



                    game_state = "playing"

            screen.fill("black")
            over = font.render("GAME OVER", True, "white")
            prompt = font.render("Press SPACE to Restart", True, "white")
            screen.blit(over, (SCREEN_WIDTH // 2 - over.get_width() // 2, 200))
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
            pygame.display.flip()
            continue

        # ---------------- PLAYING STATE ----------------
        if game_state == "playing":
            log_state()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            updatable.update(dt)

            # Player–asteroid collision
            for asteroid in asteroids:
                if player.invincible_timer <= 0 and player.collides_with(asteroid):
                    log_event("player_hit")
                    lives -= 1

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
                    respawn_player(player)
                    player.make_invincible(2)
                    break

            # Shot–asteroid collision
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()

                        # Spawn explosion BEFORE splitting
                        pos = asteroid.position.copy()
                        ParticleExplosion(pos.x, pos.y, count=35)

                        asteroid.split()

                        # add points (only when a shot actually hits)
                        if asteroid.radius > 40:
                            score += 20
                        elif asteroid.radius > 20:
                            score += 50
                        else:
                            score += 100

            # Drawing
            screen.fill("black")
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

