import pygame 

pygame.init() 

#Set Display Surface 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sprite Groups!")

#The main game loop 
running = True 
While running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

#End the game 
pygame.quit()