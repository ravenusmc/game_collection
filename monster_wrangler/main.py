import pygame, random 

#Init Pygame 
pygame.init()

#Display Window 
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

#SET FPS and Clock 
FPS = 60
clock = pygame.time.Clock() 

#Game Class 
class Game():

    def __init___(self):
        pass
    
    def update(self):
        pass

    def draw(self):
        pass
    
    def check_collisions(self):
        pass

    def start_new_round(self):
        pass 

    def choose_new_target(self):
        pass

    def pause_game(self):
        pass
    
    def reset_game(self):
        pass 

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass 

    def warp(self):
        pass 

    def reset(self):
        pass

class Monster(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass 


#Main Game Loop 
running = True 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    #Update clock 
    pygame.display.update()
    clock.tick(FPS)

#End the game 
pygame.quit()


