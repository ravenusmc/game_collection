import pygame, random 

pygame.init() 

#Set Display Surface 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sprite Groups!")

#Set FPS and Clock 
FPS = 60
clock = pygame.time.Clock()

#Player Class - class creates a player
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, monster_group):
        super().__init__()
        self.image = pygame.image.load("./assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velocity = 5
        self.monster_group = monster_group
    
    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
    
    def check_collisions(self):
        if pygame.sprite.spritecollide(self, self.monster_group, True):
            print(len(self.monster_group))

#Monster class
class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/blue_monster.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.velocity = random.randint(1,5)
    
    def update(self):
        self.rect.y += self.velocity
 
#Create a monster group and create 10 monsters
monster_group = pygame.sprite.Group()
for i in range(10):
    monster = Monster(i * 64, 10)
    monster_group.add(monster)

#Create a player group and add a player 
player_group = pygame.sprite.Group()
player = Player(500,500, monster_group)
player_group.add(player)

#The main game loop 
running = True 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 
    
    #Fill the display 
    display_surface.fill((0,0,0))

    #Update and Draw Assets 
    player_group.update()
    player_group.draw(display_surface)
    monster_group.update()
    monster_group.draw(display_surface)
    
    #update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#End the game 
pygame.quit()