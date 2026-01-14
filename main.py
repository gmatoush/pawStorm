# Example file showing a basic pygame "game loop"
import pygame
import ground
import user
import storm

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
X_SCREEN, Y_SCREEN = screen.get_size()
clock = pygame.time.Clock()
running = True
SPRITES = pygame.sprite.Group() # Sprites holds all sprites used within the game
SCORE = 0

# Sprites being stored
floor = ground.Floor(X_SCREEN, Y_SCREEN)
player = user.User((Y_SCREEN - floor.floor_height),Y_SCREEN, X_SCREEN, 100, 100)
precip = storm.Storm(floor.floor_height, Y_SCREEN, X_SCREEN)

SPRITES.add(floor, player)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Count it a score if the player touches a raindrop
    if pygame.sprite.spritecollide(player, precip.drops, True):
        SCORE += 1
    print(SCORE)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()