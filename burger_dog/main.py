import pygame, random 

#init pygame 
pygame.init()

#Set Display Surface 
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

#SET FPS 

#SET GAME VALUES 

#SET Colors 

#Set Font 

#Set Text 

#Set Sounds and Music

#Set Images 

#Main Game Loop
running = True 
while running: 
    #Check if user wants to quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

#End the game 
pygame.quit()
