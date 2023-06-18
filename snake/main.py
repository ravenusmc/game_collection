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
FPS = 5 
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
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press Any Key to Continue", True, RED, DARKGREEN)
continue_rect = continue_text.get_rect() 
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set sound 
pick_up_sound = pygame.mixer.Sound("./assets/pick_up_sound.wav")

#Set Shapes / images 
#Rectangle you need (top-left x, top-Left y, width, height)
apple_coord = (500,500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)
head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
body_coords = []

#The Main Game lopp
running = True 
while running:
    #Check to see if the user wants to quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        
        #Move the snake 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT:
                snake_dx = 1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN: 
                snake_dx = 0 
                snake_dy = 1 * SNAKE_SIZE

    #Update head coordinate
    body_coords.insert(0, head_coord)
    body_coords.pop()

    #Update the x and y position of snakes head 
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    #Check for game over by going off screen
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_coords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #Pause the game 
        is_paused = True 
        while is_paused:
            for event in pygame.event.get():
                # The player wants to play again 
                if event.type == pygame.KEYDOWN: 
                    score = 0 
                    head_x = WINDOW_WIDTH//2 
                    head_y = WINDOW_HEIGHT//2
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
                    body_coords = []
                    snake_dx = 0
                    snake_dy = 0
                    is_paused = False 
                if event.type == pygame.QUIT: 
                    is_paused = False 
                    running = False 

    #Check for collisions 
    if head_rect.colliderect(apple_rect):
        score += 1 
        pick_up_sound.play()

        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coords.append(head_coord)
    
    #Update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)

    #Fill the surface
    display_surface.fill(WHITE)
    
    #blit the HUD 
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)

    #blit the assets 
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)

    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    #Incrase FPS 
    # if score != 0 and score % 2 == 0:
    #     print('HERE')
    #     FPS += 5

    #Update the display 
    pygame.display.update()
    clock.tick(FPS)


#End the game 
pygame.quit()   