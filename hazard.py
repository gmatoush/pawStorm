
# Class made to represent the hazard warning for both enemies
import pygame

class Hazard(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, x_pos, width, height):

        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store the important variable
        self.x_pos = x_pos
        self.width = width
        self.height = height

        # Load the iamge and scale it properly
        self.image = pygame.image.load("assets/sprites/enemies/harzard.png")
        scale = self.height / self.image.get_height()
        new_width = int(self.image.get_width() * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_width, self.height))

        # Put the hazard sign where it needs to go
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x_pos