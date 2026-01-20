# Class made to represent falling heart pickups
import pygame
import random
import utils


class HeartDrop(pygame.sprite.Sprite):
    def __init__(self, floor_height, screen_height, screen_width, x_pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.floor_height = floor_height
        self.pos_y = 0
        self.speed = screen_height * 0.007
        self.width = width
        self.height = height

        self.image = pygame.image.load(utils.resource_path("assets/sprites/health/heart.png")).convert_alpha()
        scale = self.height / self.image.get_height()
        new_width = int(self.image.get_width() * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_width, self.height))

        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = x_pos

    def update(self):
        self.pos_y += self.speed
        self.rect.bottom = self.pos_y
        if self.rect.bottom >= (self.screen_height - self.floor_height):
            self.kill()

    def resize(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.speed = screen_height * 0.007


class HealthPickups:
    def __init__(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.spawn_interval_ms = random.randint(9000, 14000)
        self.timer = 0
        self.drops = pygame.sprite.Group()

    def spawn_drop(self):
        x_pos = random.randint(round(self.screen_width * 0.2), round(self.screen_width * 0.8))
        drop = HeartDrop(self.floor_height, self.screen_height, self.screen_width, x_pos, 48, 48)
        self.drops.add(drop)

    def draw(self, screen):
        self.drops.draw(screen)

    def update(self, dt_ms):
        self.timer += dt_ms
        if self.timer >= self.spawn_interval_ms and not self.drops:
            self.spawn_drop()
            self.timer = 0
            self.spawn_interval_ms = random.randint(9000, 14000)
        self.drops.update()

    def resize(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        for drop in self.drops.sprites():
            drop.resize(floor_height, screen_height, screen_width)
