import pygame
import random

# init pygame
pygame.init()

# Set the display Surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("~SNAKE!~")

#Set FPS and Clock 
FPS = 20 
clock = pygame.time.Clock()

#Set game values
SNAKE_SIZE = 20 

head_x = WINDOW_WIDTH//2 
head_y = WINDOW_HEIGHT//2 + 100

snake_dx = 0
snake_dy = 0

score = 0 

#Set colors 
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)
WHITE = (255, 255, 255)

#Set fonts 
font = pygame.font.SysFont('gabriola', 48)

#Set text 
title_text = font.render("~~SNAKE~~", True, GREEN, DARKRED)
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

game_over_text = font.render("GAMEOVER", True, RED, DARKGREEN)
game_over_rect = game_over_rect.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press Any Key to Continue", True, RED, DARKGREEN)
continue_rect = continue_text.get_rect() 
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set sound 
pick_up_sound = pygame.mixer.Sound("./assets/pick_up_sound.wav")

#Set Shapes / images 

#The Main Game lopp
running = True 
while running:
    #Check to see if the user wants to quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 




#End the game 
pygame.quit()   