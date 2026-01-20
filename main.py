# Example file showing a basic pygame "game loop"
import pygame
import ground
import user
import storm
import score
import enemy
import health

# pygame setup
pygame.init()
screen = pygame.display.set_mode(
    (1280, 720),
    pygame.RESIZABLE)

X_SCREEN, Y_SCREEN = screen.get_size()
clock = pygame.time.Clock()
running = True
SPRITES = pygame.sprite.Group() # Sprites holds all sprites used within the game
SCORE = 0

# Sprites being stored
floor = ground.Floor(X_SCREEN, Y_SCREEN)
player = user.User((Y_SCREEN - floor.floor_height),Y_SCREEN, X_SCREEN, 351, 180) #TODO: Change to scale properly
precip = storm.Storm(floor.floor_height, Y_SCREEN, X_SCREEN)
score_board = score.Scoreboard(pygame.font.SysFont(None, 40), X_SCREEN, Y_SCREEN)
lightning = enemy.Enemy(floor.floor_height, Y_SCREEN, X_SCREEN)
health_bar = health.Health((Y_SCREEN - floor.floor_height * 0.25), 64, 88)
health_bar.spawn_health()

SPRITES.add(floor, player)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            X_SCREEN, Y_SCREEN = screen.get_size()
            floor.resize(X_SCREEN, Y_SCREEN)
            player.resize(Y_SCREEN - floor.floor_height, Y_SCREEN, X_SCREEN)
            precip.resize(floor.floor_height, Y_SCREEN, X_SCREEN)
            lightning.resize(floor.floor_height, Y_SCREEN, X_SCREEN)
            health_bar.resize(Y_SCREEN - floor.floor_height * 0.25, 64, 88)
            score_board.resize(X_SCREEN, Y_SCREEN)

    # update player movement
    player.update()
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("pink")

    # RENDER YOUR GAME HERE
    # find the time since last check
    dt_ms = clock.get_time()
    SPRITES.draw(screen)
    precip.update(dt_ms)
    precip.draw(screen)
    lightning.update(dt_ms)
    lightning.draw(screen)
    health_bar.draw(screen)
    score_board.draw(screen)

    # Count it a score if the player touches a raindrop
    if pygame.sprite.spritecollide(player, precip.drops, True):
        score_board.score += 1
    
    if pygame.sprite.spritecollide(player, lightning.enemies, True):
        health_bar.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
