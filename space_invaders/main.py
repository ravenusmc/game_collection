#Space invaders...The classic arcade game
#This is actually the second time I've built this game.
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

#Game class will control main elements of game. 
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

    def __init__(self, bullet_group):
        super().__init__()
        self.image = pygame.image.load("./assets/player_ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.velocity = 8 

        self.bullet_group = bullet_group
        self.shoot_sound = pygame.mixer.Sound("./assets/player_fire.wav")


    def update(self):
        keys = pygame.key.get_pressed()

        #Move the player within the bounds of the screen 
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def fire(self):
        pass 

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH//2

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

#Create Bullet groups 
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group() 

#Create a player group and player object 
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create an alien group 
my_alien_group = pygame.sprite.Group()

#Create a game object
my_game = Game()

#Main Game Loop 
running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 
    
    #Fill the display 
    display_surface.fill((0,0,0))

    #Update and display all sprites
    my_player_group.update() 
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update() 
    my_alien_bullet_group.draw(display_surface)

    my_game.update()
    # my_game.draw(display_surface)
        

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()