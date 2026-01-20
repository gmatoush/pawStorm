# Class made to represent the health of the individual

import pygame

class Heart(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, x_pos, floor_height, width, height):

        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store the important variables
        self.x_pos = x_pos
        self.width = width
        self.height = height
        self.floor_height = floor_height

        # Load the iamge and scale it properly
        self.image = pygame.image.load("assets/sprites/health/heart.png")
        scale = self.height / self.image.get_height()
        new_width = int(self.image.get_width() * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_width, self.height))

        # Put the heart sign where it needs to go
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x_pos
        self.rect.centery = self.floor_height