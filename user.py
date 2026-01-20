
# Class made to create the person
import pygame

class User(pygame.sprite.Sprite):

    # Initialize the sprite
    def __init__(self, floor_height, screen_height, screen_width, user_width, user_height):

        # Call the parent class
        pygame.sprite.Sprite.__init__(self)

        # Store important sprite variables
        self.floor_height = floor_height
        self.pos_x = screen_width // 2 + (user_width // 2)
        self.pos_y = floor_height
        self.jump_percent = 0.1
        self.user_width = user_width
        self.user_height = user_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.jump_status = False
        self.jump = self.screen_height * 0.3
        self.speed = self.screen_width * 0.01

        # Create an image of the person
        self.right_flag = True # Creates a boolean flag saying that individual is moving right
        self.image = pygame.image.load("assets/sprites/person/user.png").convert_alpha()
        scale = self.user_height / self.image.get_height()
        new_w = int(self.image.get_width() * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_w, self.user_height))
        self.image_right = self.image
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        # Put user rectangle on the floor
        self.rect = self.image.get_rect()
        self.rect.bottom = self.pos_y
        self.rect.right = self.pos_x

    # Function updating the position of the user
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            
            # make sure player cannot exit the screen
            self.pos_x = max(self.pos_x - self.speed, self.rect.width)
            
            # make sure it is facing left
            if self.right_flag:
                self.image = self.image_left
                self.right_flag = False
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:

            # make sure player cannot exit the screen
            self.pos_x = min(self.pos_x + self.speed, self.screen_width)

            # make sure player is facing right
            if not self.right_flag:
                self.image = self.image_right
                self.right_flag = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:

            # mark jump boolean true
            if self.pos_y == self.floor_height:
                self.jump_status = True

        # Calculate slow jump up and jump down
        max_jump = self.floor_height - self.jump
        if self.jump_status and self.pos_y <= max_jump:
            self.jump_status = False

        elif self.jump_status and self.pos_y != max_jump:
            self.pos_y -= self.jump * self.jump_percent

        elif self.pos_y != self.floor_height:
            self.pos_y += self.jump * self.jump_percent


        self.rect.bottom = self.pos_y
        self.rect.right = self.pos_x
