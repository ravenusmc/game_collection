import pygame, random
vector = pygame.math.Vector2

# init pygame
pygame.init()

# set display surface (Tile size is 32X32 so 1280/32 = 40 tiles wide, 736/32 = 23 tiles high)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Knight")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Classes to control all aspects of game 
class Game():

    def __init__(self):
        pass 

    def update(self):
        pass 

    def draw(self):
        pass

    def add_zombie(self):
        pass 

    def check_collisions(self):
        pass 

    def check_round_completion(self):
        pass 

    def check_game_over(self):
        pass

    def start_new_round(self):
        pass 

    def pause_game(self):
        pass 

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image_int, main_group, sub_group=''):
        super().__init__() 
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/tiles/Tile (1).png"), (32,32))
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/tiles/Tile (2).png"), (32,32))
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/tiles/Tile (3).png"), (32,32))
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/tiles/Tile (4).png"), (32,32))
            sub_group.add(self)
        elif image_int == 5:
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/tiles/Tile (5).png"), (32,32))
            sub_group.add(self)
        #Add every tile to the main group 
        main_group.add(self)

        #Get Rect of image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
         
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass 

    def move(self):
        pass

    def check_collisions(self):
        pass 

    def check_animations(self):
        pass 

    def jump(self):
        pass 

    def fire(self):
        pass 

    def reset(self):
        pass 

    def animate(self):
        pass 

class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass 

class Zombie(pygame.sprite.Sprite):

    def __init__(self):
        pass 

    def update(self):
        pass

    def move(self):
        pass

    def check_collisions(self):
        pass 

    def check_animations(self):
        pass 
    
    def death(self):
        pass 

    def rise(self):
        pass

    def animate(self):
        pass 

class RubyMaker(pygame.sprite.Sprite):

    def __init__(self, x, y, main_group):
        super().__init__()
        #Animation Frames 
        self.ruby_sprites = []
        # Rotating 
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile000.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile001.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile002.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile003.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile004.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile005.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile006.png"), (64,64)))
         
        #load images and get rect 
        self.current_sprite = 0 
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect() 
        self.rect.bottomleft = (x,y)

        main_group.add(self)

    def update(self):
        self.animate(self.ruby_sprites, .25)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1: 
            self.current_sprite += speed 
        else: 
            self.current_sprite = 0 
        self.image = sprite_list[int(self.current_sprite)]

class Ruby(pygame.sprite.Sprite): 

    def __init__(self):
        pass 

    def update(self):
        pass 

    def check_collisions(self):
        pass 

    def move(self):
        pass

    def animate(self):
        pass 

class Portal(pygame.sprite.Sprite): 

    def __init__(self, x, y, color, portal_group):
        super().__init__()
        self.portal_sprites = []
        if color == "green":
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile000.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile001.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile002.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile003.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile004.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile005.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile006.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile007.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile008.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile009.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile010.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile011.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile012.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile013.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile014.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile015.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile016.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile017.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile018.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile019.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile020.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile021.png"), (72,72)))
        else: 
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile000.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile001.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile002.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile003.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile004.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile005.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile006.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile007.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile008.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile009.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile010.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile011.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile012.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile013.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile014.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile015.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile016.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile017.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile018.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile019.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile020.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/green/tile021.png"), (72,72)))


    def update(self):
        pass 

    def animate(self):
        if self.current_sprite < len(sprite_list) - 1: 
            self.current_sprite += speed 
        else: 
            self.current_sprite = 0 
        self.image = sprite_list[int(self.current_sprite)]

#Create Sprite group 
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group() 
my_player_group = pygame.sprite.Group() 
my_bullet_group = pygame.sprite.Group() 
my_zombie_group = pygame.sprite.Group()  
my_portal_group = pygame.sprite.Group()  
my_ruby_group = pygame.sprite.Group() 

#Create tile map 
# 0 -> no tile, 1 -> dirt 2-5 -> platforms, 6 -> ruby maker 7-8 -> platform, 9 - player
#23 rows and 40 columns 
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#Tile objects
for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        #Dirt Tile 
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, my_main_tile_group)
        elif tile_map[i][j] == 2: 
            Tile(j*32, i*32, 2, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 3: 
            Tile(j*32, i*32, 3, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 4: 
            Tile(j*32, i*32, 4, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 5: 
            Tile(j*32, i*32, 5, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 6: 
            RubyMaker(j*32, i*32, my_main_tile_group)
        elif tile_map[i][j] == 7: 
            pass
        elif tile_map[i][j] == 8: 
            pass
        elif tile_map[i][j] == 9: 
            pass
        

#Background Image
background_image = pygame.transform.scale(pygame.image.load("./assets/images/background.png"), (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         my_player.jump()

    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Draw the tiles 
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
