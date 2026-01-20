
# Class made to represent the rain following
import pygame
import random

class Rain(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, floor_height, screen_height, screen_width, x_pos, rain_width, rain_height):

        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store important sprite variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fall = True
        self.pos_y = 0
        self.speed = screen_height * 0.01
        self.floor_height = floor_height
        self.width = rain_width
        self.height = rain_height
        
        # Create an image of the rain and randomly choose the animal
        self.cats = ["cat1.png", "cat2.png", "cat3.png"]
        self.dogs = ["dog1.png", "dog2.png", "dog3.png"]
        
        idx = random.randint(0,2)
        if random.randint(0,1):
            self.image = pygame.image.load(f"assets/sprites/dogs/{self.dogs[idx]}")

        else:
            self.image = pygame.image.load(f"assets/sprites/cats/{self.cats[idx]}")

        # Scale the image properly
        scale = self.height / self.image.get_height()
        new_width = int(self.image.get_width() * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_width, self.height))

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
        self.speed = screen_height * 0.01
