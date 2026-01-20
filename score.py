import pygame

class Scoreboard:

    # Initialize the class to make the scoreboard look good
    def __init__(self, font, max_width, floor_height):

        # Variables required to keep track of the scoreboard
        self.score = 0
        self.font = font
        self.width = max_width
        self.height = floor_height
        self.color = "black"


    # Function for adding to the score
    def add_score(self):
        self.score += 1

    
    # Function to draw the scoreboard onto the screen
    def draw(self, screen):
        text = self.font.render((f"Score: {self.score}"), True, self.color)
        screen.blit(text, (self.width - (self.width * 0.1), self.height * 0.95))
    
    