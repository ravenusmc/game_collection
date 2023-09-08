# This is actually not a game but learning some more advanced techniques in pygame
# A simple map that allows a player to move around
import pygame
vector = pygame.math.Vector2

# init pygame
pygame.init()

# set display surface (Tile size is 32X32 so 960/32 = 30 tiles wide, 64/32 = 20 tiles high)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a Tile Map!")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Classes
class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.image.load("./assets/dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("./assets/grass.png")
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("./assets/water.png")
            sub_group.add(self)
        # add every tile
        main_group.add(self)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self):
        pygame.draw.rect(display_surface, (0,0,255), self.rect, 1)

# Player class - controls all aspects of the player
class Player(pygame.sprite.Sprite):
    """A player class the user can control"""

    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()
        #Animation Frames 
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = [] 

        #moving right sprites 
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (1).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (2).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (3).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (4).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (5).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (6).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (7).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Run (8).png"), (64,64)))
        
        #Moving left 
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #Idle Right 
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (1).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (2).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (3).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (4).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (5).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (6).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (7).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/boy/Idle (8).png"), (64,64)))

        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]

        # self.image = pygame.image.load("./assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.starting_x = x
        self.starting_y = y
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        # Kinematics vectors (first value is the x, second value is the y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # Kinematic constants
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = .5  # Gravity
        self.VERTICAL_JUMP_SPEED = 15  # determines how high can jump

    def update(self):
        pygame.draw.rect(display_surface, (0,255,0), self.rect, 1)
        #Creating a mask
        self.mask = pygame.mask.from_surface(self.image)
        #Draw the mask 
        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image, (255,0,0), True, mask_outline)
        self.move()
        self.check_collisions()

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .2)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .2)
        else: 
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .2)
            else: 
                self.animate(self.idle_left_sprites, .2)
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # update new rect based on calculations and add wrap around motion
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        self.rect.bottomleft = self.position
    
    def check_collisions(self):
        # Check for collisions
        collided_platforms = pygame.sprite.spritecollide(
            self, self.grass_tiles, False, pygame.sprite.collide_mask)
        if collided_platforms:
            if self.velocity.y > 0: 
                self.position.y = collided_platforms[0].rect.top + 10
                self.velocity.y = 0
        # Check with collisions with water
        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            print("You can't Swim!")
            self.position = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)

    def jump(self):
        # only jump if on a grass tile
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = self.VERTICAL_JUMP_SPEED * -1
    
    def animate(self, sprite_list, speed):
        #Loop through sprite list 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else: 
            self.current_sprite = 0 
        
        self.image = sprite_list[int(self.current_sprite)]


# Create Sprite group
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

# Create the tile map 0 -> no tile, 1 -> dirt, 2 - grass 3 ->water
# 20 rows 30 columns
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3,
        3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
]

# create individual tile object from the tile map
for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(
                j*32, i*32 + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)

# Load background image
background_image = pygame.image.load("./assets/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Main game loop - controls the main game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Draw the tiles
    main_tile_group.draw(display_surface)
    main_tile_group.update()

    # update and draw sprites
    my_player_group.update()
    my_player_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
