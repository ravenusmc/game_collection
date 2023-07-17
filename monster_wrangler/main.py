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

    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0
        self.round_time = 0
        self.frame_count = 0
        self.player = player 
        self.monster_group = monster_group
        #set sound and music 
        self.next_level_sound = pygame.mixer.Sound("./assets/next_level.wav")
        self.font = pygame.font.Font("./assets/Abrushow.ttf", 24)
        #set images 
        blue_image = pygame.image.load("./assets/blue_monster.png")
        green_image = pygame.image.load("./assets/green_monster.png")
        purple_image = pygame.image.load("./assets/purple_monster.png")
        yellow_image = pygame.image.load("./assets/yellow_monster.png")
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]
        self.target_monster_type = random.randint(0,3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]
        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH//2
        self.target_monster_rect.top = 30 

    
    def update(self):
        self.frame_count += 1
        if self.frame_count == FPS: 
            self.round_time += 1
            self.frame_count = 0 
        self.check_collisions()

    def draw(self):
        #Set Colors 
        WHITE = (255,255,255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        colors = [BLUE, GREEN, PURPLE, YELLOW]

        #Set Text 
        catch_text = self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH//2
        catch_rect.top = 5

        #score text 
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5,5)

        #Lives Text 
        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Current Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round time: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect() 
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        #Blit the HUD 
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH//2 - 32, 30, 64,64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0,100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)

    def check_collisions(self):
        #Check for collision between player and individual monster 
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        if collided_monster


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
my_game = Game(my_player, my_monster_group)

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


