# Example file showing a basic pygame "game loop"
import json
import os
import pygame
import random
import ground
import user
import storm
import score
import enemy
import health
import health_pickup
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
    lightning = enemy.Enemy(floor.floor_height, y_screen, x_screen, player.rect.width, tornado_warning_sfx)
    heart_pickups = health_pickup.HealthPickups(floor.floor_height, y_screen, x_screen)
    health_bar = health.Health((y_screen - floor.floor_height * 0.25), 64, 88)
    health_bar.spawn_health()
    sprites = pygame.sprite.Group()
    sprites.add(floor, player)
    end_animals = scale_animals(base_animals, int(floor.floor_height * 0.7))
    return floor, player, precip, score_board, lightning, heart_pickups, health_bar, sprites, end_animals

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(
    (1280, 720),
    pygame.RESIZABLE)

X_SCREEN, Y_SCREEN = screen.get_size()
clock = pygame.time.Clock()
running = True
game_started = False
game_over = False
splash_start_ms = pygame.time.get_ticks()
splash_duration_ms = 3000
show_splash = True
SPRITES = pygame.sprite.Group() # Sprites holds all sprites used within the game

start_music_path = utils.resource_path("assets/audio/start.mp3")
end_music_path = utils.resource_path("assets/audio/end.mp3")
rain_music_path = utils.resource_path("assets/audio/rain.mp3")
thunder_sfx = pygame.mixer.Sound(utils.resource_path("assets/audio/thunder.mp3"))
death_sfx = pygame.mixer.Sound(utils.resource_path("assets/audio/death.mp3"))
cat_sfx = pygame.mixer.Sound(utils.resource_path("assets/audio/cat.mp3"))
dog_sfx = pygame.mixer.Sound(utils.resource_path("assets/audio/dog.mp3"))
tornado_warning_sfx = pygame.mixer.Sound(utils.resource_path("assets/audio/tornado_warning.mp3"))
tornado_sfx = pygame.mixer.Sound(utils.resource_path("assets/audio/torando_sound.mp3"))
tornado_sfx.set_volume(1.0)
tornado_channel = pygame.mixer.Channel(2)
TORNADO_FADE_MS = 350
start_sfx = pygame.mixer.Sound(start_music_path)
start_channel = pygame.mixer.Channel(1)
START_FADE_MS = 2000
START_VOLUME_INTRO = 0.5
START_VOLUME_GAME = 0.2
current_music_path = None
current_state = "splash"
HIGH_SCORES_PATH = os.path.join(os.path.abspath("."), "high_scores.json")
HIGH_SCORES_LIMIT = 10
entering_name = False
name_input = ""
pending_score = 0
score_saved = False
last_difficulty_level = -1
tornado_audio_active = False

def play_music(path, loops=-1):
    global current_music_path
    if current_music_path == path:
        return
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops=loops)
    current_music_path = path

def play_start_audio(loops=-1):
    if start_channel.get_busy():
        return
    start_channel.set_volume(START_VOLUME_INTRO)
    start_channel.play(start_sfx, loops=loops, fade_ms=START_FADE_MS)

def load_high_scores(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    cleaned = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        score_value = entry.get("score")
        if isinstance(name, str) and isinstance(score_value, int):
            cleaned.append({"name": name[:12], "score": score_value})
    cleaned.sort(key=lambda item: item["score"], reverse=True)
    return cleaned[:HIGH_SCORES_LIMIT]

def save_high_scores(path, scores):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(scores, handle, indent=2)

def is_high_score(score_value, scores):
    if len(scores) < HIGH_SCORES_LIMIT:
        return True
    lowest = min(item["score"] for item in scores)
    return score_value > lowest

def insert_high_score(scores, name, score_value):
    scores.append({"name": name, "score": score_value})
    scores.sort(key=lambda item: item["score"], reverse=True)
    return scores[:HIGH_SCORES_LIMIT]

high_scores = load_high_scores(HIGH_SCORES_PATH)


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
floor, player, precip, score_board, lightning, heart_pickups, health_bar, SPRITES, end_animals = create_game_state(
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
            heart_pickups.resize(floor.floor_height, Y_SCREEN, X_SCREEN)
            health_bar.resize(Y_SCREEN - floor.floor_height * 0.25, 64, 88)
            score_board.resize(X_SCREEN, Y_SCREEN)
            end_animals = scale_animals(base_animals, int(floor.floor_height * 0.7))
        elif event.type == pygame.KEYDOWN and not game_started:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                game_started = True
        elif event.type == pygame.KEYDOWN and game_over:
            if entering_name:
                if event.key == pygame.K_RETURN:
                    trimmed_name = name_input.strip() or "Player"
                    high_scores = insert_high_score(high_scores, trimmed_name[:12], pending_score)
                    save_high_scores(HIGH_SCORES_PATH, high_scores)
                    entering_name = False
                    score_saved = True
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.unicode and len(name_input) < 12:
                    if event.unicode.isalnum() or event.unicode in (" ", "_", "-"):
                        name_input += event.unicode
            elif event.key == pygame.K_SPACE:
                floor, player, precip, score_board, lightning, heart_pickups, health_bar, SPRITES, end_animals = create_game_state(
                    X_SCREEN,
                    Y_SCREEN,
                    base_animals,
                )
                game_over = False
                game_started = True
                entering_name = False
                name_input = ""
                pending_score = 0
                score_saved = False
                last_difficulty_level = -1
                tornado_audio_active = False

    if show_splash:
        if pygame.time.get_ticks() - splash_start_ms >= splash_duration_ms:
            show_splash = False
            thunder_sfx.play()
        else:
            screen.blit(splash_bg, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            continue

    if not game_started:
        if current_state != "start":
            play_start_audio(loops=-1)
            current_state = "start"
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
        if current_state != "end":
            start_channel.stop()
            play_music(end_music_path, loops=-1)
            current_state = "end"
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

        prompt_text = score_board.font.render("Press SPACE to start again", True, score_board.color)
        prompt_rect = prompt_text.get_rect()
        prompt_rect.center = (X_SCREEN // 2, Y_SCREEN - (prompt_text.get_height() * 2))
        screen.blit(prompt_text, prompt_rect)

        scores_title = score_board.font.render("High Scores", True, score_board.color)
        title_rect = scores_title.get_rect()
        title_rect.centerx = X_SCREEN // 2
        title_rect.top = int(Y_SCREEN * 0.05)
        screen.blit(scores_title, title_rect)

        list_y = title_rect.bottom + 10
        if entering_name:
            name_prompt = score_board.font.render(f"New High Score! Name: {name_input}", True, score_board.color)
            name_rect = name_prompt.get_rect()
            name_rect.centerx = X_SCREEN // 2
            name_rect.top = list_y
            screen.blit(name_prompt, name_rect)
            list_y = name_rect.bottom + 8
        for i, entry in enumerate(high_scores[:HIGH_SCORES_LIMIT], start=1):
            line = score_board.font.render(f"{i}. {entry['name']} - {entry['score']}", True, score_board.color)
            line_rect = line.get_rect()
            line_rect.centerx = X_SCREEN // 2
            line_rect.top = list_y
            screen.blit(line, line_rect)
            list_y = line_rect.bottom + 6
        pygame.display.flip()
        clock.tick(60)
        continue

    if current_state != "game":
        play_music(rain_music_path, loops=-1)
        start_channel.set_volume(START_VOLUME_GAME)
        current_state = "game"
        
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
    if lightning.tornadoes:
        if not tornado_audio_active:
            tornado_channel.play(tornado_sfx, loops=-1, fade_ms=TORNADO_FADE_MS)
            tornado_audio_active = True
    elif tornado_audio_active:
        tornado_channel.fadeout(TORNADO_FADE_MS)
        tornado_audio_active = False
    heart_pickups.update(dt_ms)
    heart_pickups.draw(screen)
    health_bar.draw(screen)
    score_board.draw(screen)

    missed = precip.consume_missed()
    if missed:
        for _ in range(missed):
            health_bar.update()
        if health_bar.lives <= 0 and not game_over:
            death_sfx.play()
            game_over = True
            player.pos_y = player.floor_height
            player.rect.bottom = player.pos_y
            pending_score = score_board.score
            if is_high_score(pending_score, high_scores):
                entering_name = True
                name_input = ""
                score_saved = False
            else:
                entering_name = False
                score_saved = True

    # Count it a score if the player touches a raindrop
    captured = pygame.sprite.spritecollide(player, precip.drops, True)
    if captured:
        score_board.score += len(captured)
        for drop in captured:
            if getattr(drop, "animal_type", None) == "dog":
                dog_sfx.play()
            elif getattr(drop, "animal_type", None) == "cat":
                cat_sfx.play()

    if pygame.sprite.spritecollide(player, heart_pickups.drops, True):
        health_bar.add_life()

    difficulty_level = score_board.score // 10
    if difficulty_level != last_difficulty_level:
        precip.set_difficulty(difficulty_level)
        lightning.set_difficulty(difficulty_level)
        last_difficulty_level = difficulty_level
    
    if pygame.sprite.spritecollide(player, lightning.enemies, True):
        thunder_sfx.play()
        health_bar.update()
        if health_bar.lives <= 0 and not game_over:
            death_sfx.play()
            game_over = True
            player.pos_y = player.floor_height
            player.rect.bottom = player.pos_y
            pending_score = score_board.score
            if is_high_score(pending_score, high_scores):
                entering_name = True
                name_input = ""
                score_saved = False
            else:
                entering_name = False
                score_saved = True
    if pygame.sprite.spritecollide(player, lightning.tornadoes, False) and not game_over:
        margin_x = int(player.rect.width * 0.5)
        margin_y = int(player.rect.height * 0.5)
        min_x = player.rect.width + margin_x
        max_x = max(min_x, X_SCREEN - margin_x)
        min_y = player.rect.height + margin_y
        max_y = max(min_y, int(player.floor_height - margin_y))
        target_x = random.randint(min_x, max_x)
        target_y = random.randint(min_y, max_y)
        player.start_throw(target_x, target_y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
