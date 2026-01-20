# Class that spawns random lightniing and wind gusts
import pygame
import random
from lightning import Lightning
from hazard import Hazard
from tornado import Tornado

class Enemy:

    # Initialize the class to contain the enemies
    def __init__(self, floor_height, screen_height, screen_width, player_width, tornado_warning_sfx):

        # Necessary inputs for each enemy
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.tornado_min_width = player_width + 100
        self.tornado_warning_sfx = tornado_warning_sfx

        # Necessary variable for spawning more enemies
        self.lightning_min_interval_ms = 1000
        self.lightning_max_interval_ms = 10000
        self.spawn_interval_ms = random.randint(5000, 20000)
        self.timer = 0
        self.enemies = pygame.sprite.Group()
        self.warnings = pygame.sprite.Group()
        self.pending_strikes = []
        self.warning_delay_ms = 1000
        self.tornado_min_interval_ms = 6000
        self.tornado_max_interval_ms = 14000
        self.tornado_spawn_interval_ms = random.randint(7000, 15000)
        self.tornado_timer = 0
        self.tornadoes = pygame.sprite.Group()
        self.pending_tornadoes = []
        self.tornado_warning_delay_ms = 4000
        self.tornado_warning_offset = 24

    
    # Create a function that randomly spawns enemies
    def spawn_enemy(self):
        
        # update the spawn interval
        self.spawn_interval_ms = random.randint(self.lightning_min_interval_ms, self.lightning_max_interval_ms)

        # TODO: calculate actual height
        x_pos = random.randint(90, self.screen_width - 90)
        warning = Hazard(x_pos, 48, 45)
        warning.rect.bottom = self.screen_height - self.floor_height
        warning.kind = "lightning"
        warning.target_y = self.screen_height - self.floor_height
        self.warnings.add(warning)
        self.pending_strikes.append(
            {
                "x_pos": x_pos,
                "delay_ms": self.warning_delay_ms,
                "warning": warning,
            }
        )

    def spawn_tornado(self):
        self.tornado_spawn_interval_ms = random.randint(self.tornado_min_interval_ms, self.tornado_max_interval_ms)
        if self.tornado_warning_sfx:
            self.tornado_warning_sfx.play(loops=0)

        y_pos = self.screen_height - self.floor_height

        direction = random.choice((-1, 1))
        warning_x = 40 if direction == 1 else (self.screen_width - 40)
        warning = Hazard(warning_x, 48, 45)
        warning.rect.bottom = y_pos - self.tornado_warning_offset
        warning.kind = "tornado"
        warning.target_y = y_pos - self.tornado_warning_offset
        warning.direction = direction
        self.warnings.add(warning)
        self.pending_tornadoes.append(
            {
                "y_pos": y_pos,
                "direction": direction,
                "delay_ms": self.tornado_warning_delay_ms,
                "warning": warning,
            }
        )

    # draw the hazard, and then the lightning
    def draw(self, screen):
        self.warnings.draw(screen)
        self.enemies.draw(screen)
        self.tornadoes.draw(screen)

    def update(self, dt_ms):

        # check if dt_ms is bigger than interval
        self.timer += dt_ms
        if self.timer >= self.spawn_interval_ms and not self.pending_strikes and not self.enemies:
            self.spawn_enemy()
            self.timer -= self.spawn_interval_ms
        self.tornado_timer += dt_ms
        if self.tornado_timer >= self.tornado_spawn_interval_ms and not self.pending_tornadoes and not self.tornadoes:
            self.spawn_tornado()
            self.tornado_timer -= self.tornado_spawn_interval_ms

        # always update all the drops
        if self.pending_strikes:
            for strike in list(self.pending_strikes):
                strike["delay_ms"] -= dt_ms
                if strike["delay_ms"] <= 0:
                    enemy = Lightning(
                        self.floor_height,
                        self.screen_height,
                        self.screen_width,
                        strike["x_pos"],
                        88,
                        self.screen_height,
                    )
                    self.enemies.add(enemy)
                    strike["warning"].kill()
                    self.pending_strikes.remove(strike)

        if self.pending_tornadoes:
            for twister in list(self.pending_tornadoes):
                twister["delay_ms"] -= dt_ms
                if twister["delay_ms"] <= 0:
                    enemy = Tornado(
                        self.floor_height,
                        self.screen_height,
                        self.screen_width,
                        twister["y_pos"],
                        twister["direction"],
                        self.tornado_min_width,
                    )
                    self.tornadoes.add(enemy)
                    twister["warning"].kill()
                    self.pending_tornadoes.remove(twister)

        self.enemies.update()
        self.tornadoes.update()

    def resize(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width

        for warning in self.warnings.sprites():
            if getattr(warning, "kind", None) == "tornado":
                warning.rect.centerx = 40 if warning.direction == 1 else (self.screen_width - 40)
                warning.rect.centery = min(max(warning.target_y, 0), self.screen_height)
            else:
                warning.rect.bottom = self.screen_height - self.floor_height

        for strike in self.pending_strikes:
            strike["x_pos"] = min(max(strike["x_pos"], 0), self.screen_width)
        for twister in self.pending_tornadoes:
            twister["y_pos"] = min(max(twister["y_pos"], 0), self.screen_height)

        for enemy in self.enemies.sprites():
            enemy.resize(self.floor_height, self.screen_height, self.screen_width)
        for enemy in self.tornadoes.sprites():
            enemy.resize(self.floor_height, self.screen_height, self.screen_width)

    def set_difficulty(self, level):
        lightning_min = max(400, 1000 - (level * 60))
        lightning_max = max(1500, 10000 - (level * 400))
        if lightning_max <= lightning_min:
            lightning_max = lightning_min + 200
        self.lightning_min_interval_ms = lightning_min
        self.lightning_max_interval_ms = lightning_max

        tornado_min = max(2500, 6000 - (level * 200))
        tornado_max = max(4000, 14000 - (level * 400))
        if tornado_max <= tornado_min:
            tornado_max = tornado_min + 500
        self.tornado_min_interval_ms = tornado_min
        self.tornado_max_interval_ms = tornado_max
