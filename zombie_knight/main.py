import pygame, random
vector = pygame.math.Vector2

# init pygame
pygame.init()

# set display surface (Tile size is 32X32 so 1280/32 = 40 tiles wide, 736/32 = 23 tiles high)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Knight")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Classes 

class Game():

    def __init__(self):
        pass 

    def update(self):
        pass 

    def draw(self):
        pass

    def add_zombie(self):
        pass 

    def check_collisions(self):
        pass 

    def check_round_completion(self):
        pass 

    def check_game_over(self):
        pass

    def start_new_round(self):
        pass 

    def pause_game(self):
        pass 

class Tile(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    



#Background Image
background_image = pygame.transform.scale(pygame.image.load("./assets/images/background.png"), (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         my_player.jump()

    # Blit the background
    display_surface.blit(background_image, background_rect)

    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
