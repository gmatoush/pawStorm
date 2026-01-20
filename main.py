# Example file showing a basic pygame "game loop"
import pygame
import ground
import user
import storm
import score
import enemy
import health
import utils


icon = pygame.image.load(utils.resource_path("assets/icon/icon.png"))
pygame.display.set_icon(icon)
pygame.display.set_caption("Paw Storm")

def scale_animals(base_animals, target_height):
    scaled = []
    for animal in base_animals:
        scale = target_height / animal.get_height()
        new_width = int(animal.get_width() * scale)
        scaled.append(pygame.transform.smoothscale(animal, (new_width, target_height)))
    return scaled

def create_game_state(x_screen, y_screen, base_animals):
    floor = ground.Floor(x_screen, y_screen)
    player = user.User((y_screen - floor.floor_height), y_screen, x_screen, 351, 180)
    precip = storm.Storm(floor.floor_height, y_screen, x_screen)
    score_board = score.Scoreboard(pygame.font.SysFont(None, 40), x_screen, y_screen)
    lightning = enemy.Enemy(floor.floor_height, y_screen, x_screen)
    health_bar = health.Health((y_screen - floor.floor_height * 0.25), 64, 88)
    health_bar.spawn_health()
    sprites = pygame.sprite.Group()
    sprites.add(floor, player)
    end_animals = scale_animals(base_animals, int(floor.floor_height * 0.7))
    return floor, player, precip, score_board, lightning, health_bar, sprites, end_animals

# pygame setup
pygame.init()
screen = pygame.display.set_mode(
    (1280, 720),
    pygame.RESIZABLE)

X_SCREEN, Y_SCREEN = screen.get_size()
clock = pygame.time.Clock()
running = True
game_started = False
game_over = False
splash_start_ms = pygame.time.get_ticks()
splash_duration_ms = 5000
show_splash = True
SPRITES = pygame.sprite.Group() # Sprites holds all sprites used within the game
SCORE = 0

# Sprites being stored
base_start_bg = pygame.image.load(utils.resource_path("assets/backgrounds/start.png")).convert()
base_game_bg = pygame.image.load(utils.resource_path("assets/backgrounds/background.png")).convert()
base_end_bg = pygame.image.load(utils.resource_path("assets/backgrounds/end.png")).convert()
base_splash = pygame.image.load(utils.resource_path("assets/icon/icon.png")).convert_alpha()
start_bg = pygame.transform.smoothscale(base_start_bg, (X_SCREEN, Y_SCREEN))
game_bg = pygame.transform.smoothscale(base_game_bg, (X_SCREEN, Y_SCREEN))
end_bg = pygame.transform.smoothscale(base_end_bg, (X_SCREEN, Y_SCREEN))
splash_bg = pygame.transform.smoothscale(base_splash, (X_SCREEN, Y_SCREEN))
base_animals = [
    pygame.image.load(utils.resource_path("assets/sprites/dogs/dog1.png")).convert_alpha(),
    pygame.image.load(utils.resource_path("assets/sprites/dogs/dog2.png")).convert_alpha(),
    pygame.image.load(utils.resource_path("assets/sprites/dogs/dog3.png")).convert_alpha(),
    pygame.image.load(utils.resource_path("assets/sprites/cats/cat1.png")).convert_alpha(),
    pygame.image.load(utils.resource_path("assets/sprites/cats/cat2.png")).convert_alpha(),
    pygame.image.load(utils.resource_path("assets/sprites/cats/cat3.png")).convert_alpha(),
]
floor, player, precip, score_board, lightning, health_bar, SPRITES, end_animals = create_game_state(
    X_SCREEN,
    Y_SCREEN,
    base_animals,
)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            X_SCREEN, Y_SCREEN = screen.get_size()
            start_bg = pygame.transform.smoothscale(base_start_bg, (X_SCREEN, Y_SCREEN))
            game_bg = pygame.transform.smoothscale(base_game_bg, (X_SCREEN, Y_SCREEN))
            end_bg = pygame.transform.smoothscale(base_end_bg, (X_SCREEN, Y_SCREEN))
            splash_bg = pygame.transform.smoothscale(base_splash, (X_SCREEN, Y_SCREEN))
            floor.resize(X_SCREEN, Y_SCREEN)
            player.resize(Y_SCREEN - floor.floor_height, Y_SCREEN, X_SCREEN)
            precip.resize(floor.floor_height, Y_SCREEN, X_SCREEN)
            lightning.resize(floor.floor_height, Y_SCREEN, X_SCREEN)
            health_bar.resize(Y_SCREEN - floor.floor_height * 0.25, 64, 88)
            score_board.resize(X_SCREEN, Y_SCREEN)
            end_animals = scale_animals(base_animals, int(floor.floor_height * 0.7))
        elif event.type == pygame.KEYDOWN and not game_started:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                game_started = True
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                floor, player, precip, score_board, lightning, health_bar, SPRITES, end_animals = create_game_state(
                    X_SCREEN,
                    Y_SCREEN,
                    base_animals,
                )
                game_over = False
                game_started = True

    if show_splash:
        if pygame.time.get_ticks() - splash_start_ms >= splash_duration_ms:
            show_splash = False
        else:
            screen.blit(splash_bg, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            continue

    if not game_started:
        screen.blit(start_bg, (0, 0))
        intro_lines = [
            "Can you catch all of the animals?",
            "Watch out for lightning warnings.",
        ]
        intro_y = Y_SCREEN // 2
        pulse = 0.95 + (0.1 * (pygame.time.get_ticks() % 1000) / 1000)
        for i, line in enumerate(intro_lines):
            intro_text = score_board.font.render(line, True, "white")
            angle = -6 if i % 2 == 0 else 6
            intro_text = pygame.transform.rotate(intro_text, angle)
            scaled_w = int(intro_text.get_width() * pulse)
            scaled_h = int(intro_text.get_height() * pulse)
            intro_text = pygame.transform.smoothscale(intro_text, (scaled_w, scaled_h))
            intro_rect = intro_text.get_rect()
            intro_rect.center = (
                int(X_SCREEN * 0.25) if i == 0 else int(X_SCREEN * 0.75),
                intro_y,
            )
            screen.blit(intro_text, intro_rect)
        pygame.display.flip()
        clock.tick(60)
        continue
    if game_over:
        screen.blit(end_bg, (0, 0))
        screen.blit(floor.image, floor.rect)
        player.rect.bottom = floor.rect.top
        screen.blit(player.image, player.rect)

        gap = 16
        total_width = sum(animal.get_width() for animal in end_animals)
        if end_animals:
            total_width += gap * (len(end_animals) - 1)
        start_x = player.rect.centerx - (total_width // 2)
        start_x = max(10, min(start_x, X_SCREEN - total_width - 10))
        y_bottom = floor.rect.top
        x = start_x
        for animal in end_animals:
            rect = animal.get_rect()
            rect.bottom = y_bottom
            rect.left = x
            screen.blit(animal, rect)
            x = rect.right + gap

        end_text = score_board.font.render("THE END", True, score_board.color)
        score_text = score_board.font.render((f"Score: {score_board.score}"), True, score_board.color)
        prompt_text = score_board.font.render("Press SPACE to start again", True, score_board.color)

        end_rect = end_text.get_rect()
        end_rect.center = (X_SCREEN // 2, (Y_SCREEN // 2) - end_text.get_height())
        screen.blit(end_text, end_rect)

        score_rect = score_text.get_rect()
        score_rect.center = (X_SCREEN // 2, Y_SCREEN // 2)
        screen.blit(score_text, score_rect)

        prompt_rect = prompt_text.get_rect()
        prompt_rect.center = (X_SCREEN // 2, (Y_SCREEN // 2) + score_text.get_height() + 10)
        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()
        clock.tick(60)
        continue

    # update player movement
    player.update()

    # draw background
    screen.blit(game_bg, (0, 0))

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
        if health_bar.lives <= 0:
            game_over = True
            player.pos_y = player.floor_height
            player.rect.bottom = player.pos_y

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
