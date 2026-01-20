# Class that spawns random lightniing and wind gusts
import pygame
import random
from lightning import Lightning
from hazard import Hazard

class Enemy:

    # Initialize the class to contain the enemies
    def __init__(self, floor_height, screen_height, screen_width):

        # Necessary inputs for each enemy
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width

        # Necessary variable for spawning more enemies
        self.spawn_interval_ms = random.randint(5000, 20000)
        self.timer = 0
        self.enemies = pygame.sprite.Group()
        self.warnings = pygame.sprite.Group()
        self.pending_strikes = []
        self.warning_delay_ms = 1000

    
    # Create a function that randomly spawns enemies
    def spawn_enemy(self):
        
        # update the spawn interval
        self.spawn_interval_ms = random.randint(1000, 10000)

        # TODO: calculate actual height
        x_pos = random.randint(90, self.screen_width - 90)
        warning = Hazard(x_pos, 48, 45)
        warning.rect.bottom = self.screen_height - self.floor_height
        self.warnings.add(warning)
        self.pending_strikes.append(
            {
                "x_pos": x_pos,
                "delay_ms": self.warning_delay_ms,
                "warning": warning,
            }
        )

    # draw the hazard, and then the lightning
    def draw(self, screen):
        self.warnings.draw(screen)
        self.enemies.draw(screen)

    def update(self, dt_ms):

        # check if dt_ms is bigger than interval
        self.timer += dt_ms
        if self.timer >= self.spawn_interval_ms and not self.pending_strikes and not self.enemies:
            self.spawn_enemy()
            self.timer -= self.spawn_interval_ms

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

        self.enemies.update()

    def resize(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width

        for warning in self.warnings.sprites():
            warning.rect.bottom = self.screen_height - self.floor_height

        for strike in self.pending_strikes:
            strike["x_pos"] = min(max(strike["x_pos"], 0), self.screen_width)

        for enemy in self.enemies.sprites():
            enemy.resize(self.floor_height, self.screen_height, self.screen_width)
