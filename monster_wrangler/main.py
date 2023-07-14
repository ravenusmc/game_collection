#This game will have a knight who will attempt to collect monsters of a certain color
#In a way it kind of plays like pacman. 
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

#Game Class - controls main elements of the game
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

#Player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2 
        self.rect.bottom = WINDOW_HEIGHT
        self.lives = 5
        self.warps = 2 
        self.velocity = 8 
        self.catch_sound = pygame.mixer.Sound("./assets/catch.wav")
        self.die_sound = pygame.mixer.Sound("./assets/die.wav")
        self.warp_sound = pygame.mixer.Sound("./assets/warp.wav")

    def update(self):
        keys = pygame.key.get_pressed() 
        #Move the player
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity 
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity 
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity
        
    def warp(self):
        if self.warps > 0: 
            self.warps -= 1 
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.centerx = WINDOW//2 
        self.rect.bottom = WINDOW_HEIGHT

#Monster Class
class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        #Monster type is an int 0 -> Blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.type = monster_type
        #set random motion 
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.velocity = random.randint(1,5)

    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        #Bound the monster off display 
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx 
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy = -1 * self.dy    

#Create player group and obj 
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#Create a monster group 
my_monster_group = pygame.sprite.Group()
#Test Monster 
monster = Monster(500,500, pygame.image.load("./assets/green_monster.png"), 1)
my_monster_group.add(monster)

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

    #Update and draw sprite groups 
    my_player_group.update() 
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    #Update and draw the game 
    my_game.update() 
    my_game.draw()
    
    #Update clock 
    pygame.display.update()
    clock.tick(FPS)

#End the game 
pygame.quit()


