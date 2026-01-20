
# Class made to create the ground
import pygame
import utils

class Floor(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, x, y_max_height):
        
        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store important sprite variables
        self.floor_height = int(y_max_height * 0.15)

        # Load and scale image
        self.base_image = pygame.image.load(utils.resource_path("assets/grounds/ground1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.base_image, (x, self.floor_height))

        # Put rectangle around the floor 
        self.rect = self.image.get_rect()
        self.rect.bottom = y_max_height

    def resize(self, x, y_max_height):
        self.floor_height = int(y_max_height * 0.15)
        self.image = pygame.transform.scale(self.base_image, (x, self.floor_height))
        self.rect = self.image.get_rect()
        self.rect.bottom = y_max_height
