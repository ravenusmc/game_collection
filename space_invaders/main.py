import pygame, random 

pygame.init()

#Set display Surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

#SET FPS and Clock 
FPS = 60 
clock = pygame.time.Clock() 

#Define classes 
class Game():

    def __init__(self):
        pass 

    def update(self):
        pass 

    def draw(self):
        pass

    def shift_aliens(self):
        pass 

    def check_collisions(self):
        pass 

    def check_round_completion(self):
        pass
    
    def start_new_round(self):
        pass 

    def check_game_status(self):
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

    def fire(self):
        pass 

    def reset(self):
        pass 

class Alien(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass 

    def fire(self):
        pass 

    def reset(self):
        pass 

class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass 

class AlienBullet(pygame.sprite.Sprite):

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
        

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()