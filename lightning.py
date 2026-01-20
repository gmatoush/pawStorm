
# Classes made to represent the enemies
import pygame
import utils

class Lightning(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, floor_height, screen_height, screen_width, x_pos, rain_width, rain_height):

        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store important sprite variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fall = True
        self.pos_y = 0
        self.speed = screen_height * 0.2
        self.floor_height = floor_height
        self.width = rain_width
        self.height = rain_height
        
        # load in the lightning bolt image
        self.image = pygame.image.load(utils.resource_path("assets/sprites/enemies/lighting.png"))

        # Scale the image properly
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

        # Put rain rectangle in the sky
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.right = x_pos

    # Function that makes the rain fall and kill it if touches palyer or ground
    def update(self):
        if self.fall:
            self.pos_y += self.speed
            self.rect.bottom = self.pos_y

        if self.rect.bottom >= (self.screen_height - self.floor_height):
            self.kill()

    def resize(self, floor_height, screen_height, screen_width):
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.speed = screen_height * 0.5

        
