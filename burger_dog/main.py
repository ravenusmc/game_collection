import pygame, random 

#init pygame 
pygame.init()

#Set Display Surface 
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

#SET FPS 
FPS = 60 
clock = pygame.time.Clock()

#SET GAME VALUES 
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5 
PLAYER_BOOST_VELOCITY = 10 
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3 
BURGER_ACCERLERATION = .25 
BUFFER_DISTANCE = 100

score = 0 
burger_points = 0 
burgers_eaten = 0 

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL

burger_velocity = STARTING_BURGER_VELOCITY

#SET Colors 
ORANGE = (246, 170, 54)
BLACK = (0,0,0)
WHITE = (255,255,255)

#Set Font 
font = pygame.font.Font("./assets/WashYourHand.ttf", 32)

#Set Text 
points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10,10)

score_text = font.render("Score: " + str(score), True, ORANGE)
score_rect = score_text.get_rect() 
score_rect.topleft = (10, 50)

title_text = font.render("Burger Dog", True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10 

eaten_text = font.render("Burgers Eaten: " + str(burgers_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()  
eaten_rect.centerx = WINDOW_WIDTH//2 
eaten_rect.y = 50 

lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect() 
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10, 50)

game_over_text = font.render("Final Score: " + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press Any Key to Play Again", True, ORANGE)
continue_rect = continue_text.get_rect() 
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set Sounds and Music
bark_sound = pygame.mixer.Sound("./assets/bark_sound.wav")
miss_sound = pygame.mixer.Sound("./assets/miss_sound.wav")
pygame.mixer.music.load("./assets/bd_background_music.wav")

#Set Images 
player_image_right = pygame.image.load("./assets/dog_right.png")
player_image_left = pygame.image.load("./assets/dog_left.png")

player_image = player_image_left
player_rect = player_image.get_rect() 
player_rect.centerx = WINDOW_WIDTH//2 
player_rect.bottom = WINDOW_HEIGHT

burger_image = pygame.image.load("./assets/burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32),  -BUFFER_DISTANCE)

#Main Game Loop
running = True 
while running: 
    #Check if user wants to quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    #Fill the surface 
    display_surface.fill(BLACK)

    #Blit the HUD 
    display_surface.blit(points_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, WHITE, (0,100), (WINDOW_WIDTH, 100), 3)

    #Blit the assets 
    display_surface.blit(player_image, player_rect)
    display_surface.blit(burger_image, burger_rect)

    #Update the Display 
    pygame.display.update()
    clock.tick(FPS)


#End the game 
pygame.quit()