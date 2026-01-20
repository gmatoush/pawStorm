# Class made to represent the health bar
import pygame
from heart import Heart

class Health:

    # Initialize the iomport variables
    def __init__(self, floor_height, width, height):

        # Necessary inputs for each heart
        self.floor_height = floor_height
        
        # Necessary variables for spawning health bar
        self.width = width
        self.height = height
        self.health = pygame.sprite.Group()
        self.lives = 3
        self.max_lives = 5

    
    # Create a function that spawns the health bar
    def spawn_health(self):
        self.health.empty()
        gap = int(self.width * 0.1)
        x = int(self.width * 0.5)

        for _ in range(self.lives):
            heart = Heart(x, self.floor_height, self.height, self.width)
            self.health.add(heart)
            x += self.width + gap

    # draw all of the hearts
    def draw(self, screen):
        self.health.draw(screen)

    # Create a function that removes a heart if the lightning hits them
    def update(self):
        if self.lives <= 0:
            return

        self.lives -= 1
        hearts = self.health.sprites()
        if hearts:
            hearts[-1].kill()

    def add_life(self):
        if self.lives >= self.max_lives:
            return
        self.lives += 1
        self.spawn_health()

    def resize(self, floor_height, width, height):
        self.floor_height = floor_height
        self.width = width
        self.height = height
        self.spawn_health()
        

