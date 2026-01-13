
# Class made to represent the rain following
import pygame
import random

class Rain(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, floor_height, screen_height, screen_width):

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
        self.image = pygame.Surface([100, 100])
        
        if random.randint(0,1):
            self.image.fill("white")
            
        else:
            self.image.fill("black")

        # Put user rectangle on the floor
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.right = 200

    
    # Function that makes the rain fall and kill it if touches palyer or ground
    def update(self):
        if self.fall:
            self.pos_y += self.speed
            self.rect.bottom = self.pos_y

        if self.rect.bottom >= (self.screen_height - self.floor_height):
            self.kill()