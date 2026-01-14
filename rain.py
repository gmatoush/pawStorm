
# Class made to represent the rain following
import pygame
import random

class Rain(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, floor_height, screen_height, screen_width, x_pos):

        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store important sprite variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fall = True
        self.pos_y = 0
        self.speed = screen_height * 0.01
        self.floor_height = floor_height
        
        # Create an image of the rain and randomly choose the color
        self.img = None
        # TODO: Check the size of the image
        self.image = pygame.Surface([self.screen_width * 0.1, self.screen_height * 0.1])
        
        if random.randint(0,1):
            self.image.fill("white")

        else:
            self.image.fill("black")

        # Put user rectangle on the floor
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