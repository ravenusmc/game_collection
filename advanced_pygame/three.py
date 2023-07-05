import pygame, random 

#init pygame 
pygame.init()

#Set display surface 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Group Collide")

#Set FPS and Clock 
FPS = 60 
clock = pygame.time.Clock()

#The main game loop 
running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = false 
    
    #Update the displah and tick clock 
    pygame.display.update()
    clock.tick(FPS)

#End the game 
pygame.quit()