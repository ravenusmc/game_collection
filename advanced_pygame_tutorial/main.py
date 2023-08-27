import pygame 
vector = pygame.math.Vector2

#init pygame 
pygame.init() 

#set display surface (Tile size is 32X32 so 960/32 = 30 tiles wide, 64/32 = 20 tiles high)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a Tile Map!")

#Set FPS and clock 
FPS = 60 
clock = pygame.time.Clock()

#Classes 
class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        if image_int == 1: 
            self.image = pygame.image.load("./assets/dirt.png")
        elif image_int == 2: 
            self.image = pygame.image.load("./assets/grass.png")
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("./assets/water.png")
            sub_group.add(self)
        #add every tile 
        main_group.add(self)

        self.rect = self.image.get_rect() 
        self.rect.topleft = (x,y)


class Player(pygame.sprite.Sprite):

    def __init__(self, x,y):
        super().__init__() 
        self.image = pygame.image.load("./assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        #Kinematics vectors 
        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)

    
    def update(self):
        pass



#Create Sprite group 
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

#Create the tile map 0 -> no tile, 1 -> dirt, 2 - grass 3 ->water
#20 rows 30 columns 
tile_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2],
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,4,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1]
]

#create individual tile object from the tile map 
for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1: 
            Tile(j*32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(j*32, i*32 + 32)
            my_player_group.add(my_player)
            # Tile(j*32, i*32, 4, main_tile_group, player_tile_group)

#Load background image 
background_image = pygame.image.load("./assets/background.png")   
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

#Main game loop 
running = True 
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    #Blit the background 
    display_surface.blit(background_image, background_rect)

    #Draw the tiles 
    main_tile_group.draw(display_surface)

    #update and draw sprites 
    my_player_group.update()
    my_player_group.draw(display_surface)
    
    pygame.display.update() 
    clock.tick(FPS)

#End the game 
pygame.quit() 
