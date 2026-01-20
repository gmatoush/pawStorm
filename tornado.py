# Class made to represent a tornado sweeping across the screen
import pygame
import utils


class Tornado(pygame.sprite.Sprite):
    def __init__(self, floor_height, screen_height, screen_width, y_pos, direction, min_width):
        pygame.sprite.Sprite.__init__(self)

        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.direction = direction
        self.speed = screen_width * 0.015
        self.min_width = min_width

        self.base_image = pygame.image.load(utils.resource_path("assets/sprites/enemies/tornado.png")).convert_alpha()
        self.height = int(self.screen_height * 0.18)
        scale = self.height / self.base_image.get_height()
        new_width = int(self.base_image.get_width() * scale)
        if new_width < self.min_width:
            scale = self.min_width / self.base_image.get_width()
            self.height = int(self.base_image.get_height() * scale)
            new_width = self.min_width
        self.image = pygame.transform.smoothscale(self.base_image, (new_width, self.height))

        self.rect = self.image.get_rect()
        start_x = -self.rect.width if self.direction == 1 else (self.screen_width + self.rect.width)
        self.pos_x = start_x
        self.rect.centerx = int(self.pos_x)
        self.rect.bottom = y_pos

    def update(self):
        self.pos_x += self.speed * self.direction
        self.rect.centerx = int(self.pos_x)

        if self.direction == 1 and self.rect.left > self.screen_width:
            self.kill()
        elif self.direction == -1 and self.rect.right < 0:
            self.kill()

    def resize(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.speed = screen_width * 0.015

        self.height = int(self.screen_height * 0.18)
        scale = self.height / self.base_image.get_height()
        new_width = int(self.base_image.get_width() * scale)
        if new_width < self.min_width:
            scale = self.min_width / self.base_image.get_width()
            self.height = int(self.base_image.get_height() * scale)
            new_width = self.min_width
        self.image = pygame.transform.smoothscale(self.base_image, (new_width, self.height))
        self.rect = self.image.get_rect(center=self.rect.center)
