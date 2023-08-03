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

    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.round_number = 1 
        self.score = 0 

        self.player = player 
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        self.new_round_sound = pygame.mixer.Sound("./assets/new_round.wav")
        self.breach_sound = pygame.mixer.Sound("./assets/breach.wav")
        self.alien_hit_sound = pygame.mixer.Sound("./assets/alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("./assets/player_hit.wav")

        self.font = pygame.font.Font("./assets/Facon.ttf", 32)

    def update(self):
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        WHITE = (255,255,255)

        #Set Text 
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect() 
        score_rect.centerx = WINDOW_WIDTH//2
        score_rect.top = 10 

        round_text = self.font.render("Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect() 
        round_rect.topleft = (20, 10)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect() 
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        #Blit the HUD to display 
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, WHITE, (0,50), (WINDOW_WIDTH, 50), 4)
        pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)

    def shift_aliens(self):
        pass 

    def check_collisions(self):
        pass 

    def check_round_completion(self):
        pass
    
    def start_new_round(self):
        #Create a grid of aliens 11 Columns and 5 rows 
        for i in range(11):
            for j in range(5):
                alien = Alien(64 + i*64, 64 + j*64, self.round_number, self.alien_bullet_group)
                self.alien_group.add(alien)
        #Pause the game and prompt user to start 
        self.new_round_sound.play()
        self.pause_game()

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
        """Fire a bullet"""
        #Restrict the number of bullets on screen at a time
        if len(self.bullet_group) < 2:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH//2

class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, velocity, bullet_group):
        super().__init__()
        self.image = pygame.image.load("./assets/alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x
        self.starting_y = y 

        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group 

        self.shoot_sound = pygame.mixer.Sound("./assets/alien_fire.wav")

    def update(self):
        self.rect.x += self.direction * self.velocity

        #Randomly fire a bullet 
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.shoot_sound.play()
            self.fire()

    def fire(self):
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("./assets/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y 

        self.velocity = 10 
        bullet_group.add(self)

    def update(self):
        self.rect.y -= self.velocity 
        if self.rect.bottom < 0:
            self.kill()


class AlienBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("./assets/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y 

        self.velocity = 10
        bullet_group.add(self)
        
    def update(self):
        self.rect.y += self.velocity 
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

#Create Bullet groups 
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group() 

#Create a player group and player object 
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create an alien group 
my_alien_group = pygame.sprite.Group()

#Test alien group 
# for i in range(10):
#     alien = Alien(64 + i * 64, 100, 3, my_alien_bullet_group)
#     my_alien_group.add(alien)

#Create a game object
my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)
my_game.start_new_round()

#Main Game Loop 
running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 
        #The player wants to fire 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                my_player.fire()
    
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
    my_game.draw()
        

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()