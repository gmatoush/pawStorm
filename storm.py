
# Class made to add multiple different forms of the rain
import pygame
import random
from rain import Rain

class Storm:

    # Initialize the class to contain the drops
    def __init__(self, floor_height, screen_height, screen_width):
        
        # Necessary inputs for each raindrop
        self.floor_height = floor_height
        self.screen_height = screen_height
        self.screen_width = screen_width

        #Necessary variables for spawning more raindrops
        self.spawn_interval_ms = 1000
        self.timer = 0
        self.drops = pygame.sprite.Group()

    # Create a function that randomly spawns drops
    def spawn_drop(self):
        
        # randomly find the x_pos of the drop
        rain_x_pos = random.randint(round(self.screen_width * 0.2), 
                                    round(self.screen_width * 0.8))

        # Create the drop and add it to the group
        # TODO: Calculate actual heights
        drop = Rain(self.floor_height, self.screen_height, self.screen_width, rain_x_pos, 26 * 3, 30 * 3)
        self.drops.add(drop)

    # draw all of the drops
    def draw(self, screen):
        self.drops.draw(screen)
    

    # Create a function that spawns a new drop every x sec and updates the drops positions
    def update(self, dt_ms):

        # check if dt_ms is bigger than interval
        self.timer += dt_ms
        if self.timer >= self.spawn_interval_ms:
            self.spawn_drop()
            self.timer -= self.spawn_interval_ms

        # always update all the drops
        self.drops.update()

            
    



