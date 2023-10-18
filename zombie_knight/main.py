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

#Classes to control all aspects of the game
class Game():

    def __init__(self, player, zombie_group, platform_group, portal_group, bullet_group, ruby_group):
        self.STARTING_ROUND_TIME = 30
        self.STARTING_ZOMBIE_CREATION_TIME = 5
        self.score = 0 
        self.round_number = 1 
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

        #Fonts 
        self.title_font = pygame.font.Font("./assets/fonts/Poultrygeist.ttf", 48)
        self.HUD_FONT = pygame.font.Font("./assets/fonts/Pixel.ttf", 24)

        #Sounds 
        self.lost_ruby_sound = pygame.mixer.Sound("./assets/sounds/lost_ruby.wav")
        self.ruby_pickup_sound = pygame.mixer.Sound("./assets/sounds/ruby_pickup.wav")
        pygame.mixer.music.load("./assets/sounds/level_music.wav")


        #attach groups and sprites 
        self.player = player
        self.zombie_group = zombie_group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.ruby_group = ruby_group

    def update(self):
        #Update round time 
        self.frame_count += 1
        if self.frame_count % FPS == 0: 
             self.round_time -= 1 
             self.frame_count = 0
        self.check_collisions()
        self.add_zombie()
        self.check_round_completion()
        self.check_game_over()

    def draw(self):
        #set colors 
        WHITE = (255,255,255)
        GREEN = (25,200,25)

        score_text = self.HUD_FONT.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 50)

        #Health Text 
        health_text = self.HUD_FONT.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, WINDOW_HEIGHT - 25)

        #Title Font 
        title_text = self.title_font.render("Zombie Knight", True, GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 25)

        round_text = self.HUD_FONT.render("Night: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 50)

        time_text = self.HUD_FONT.render("Sunrise In: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 25)

        #Draw the HUD 
        display_surface.blit(score_text, score_rect)
        display_surface.blit(health_text, health_rect)
        display_surface.blit(title_text, title_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)

    def add_zombie(self):
        #Check to add a zombie every second of gameplay
        if self.frame_count % FPS == 0:
            if self.round_time % self.zombie_creation_time == 0:
                zombie = Zombie(self.platform_group, self.portal_group, self.round_number, 5 + self.round_number)
                self.zombie_group.add(zombie)  
                
    def check_collisions(self):
        #See if a player bullet collided with any zombie - in the zombie group
        collision_dict = pygame.sprite.groupcollide(self.bullet_group, self.zombie_group, True, False)
        if collision_dict: 
            for zombies in collision_dict.values():
                for zombie in zombies:
                    zombie.hit_sound.play()
                    zombie.is_dead = True
                    zombie.animate_death = True
        
        #See if a player stomped a dead zombie 
        collision_list = pygame.sprite.spritecollide(self.player, self.zombie_group, False)
        if collision_list: 
            for zombie in collision_list: 
                if zombie.is_dead == True:
                   zombie.kick_sound.play()
                   zombie.kill() 
                   self.score += 25 
                   ruby = Ruby(self.platform_group, self.portal_group)
                   self.ruby_group.add(ruby)

                #zombie not dead 
                else: 
                   self.player.health -= 20 
                   self.player.hit_sound.play() 
                   #move the player to not continually take damage 
                   self.player.position.x -= 256 * zombie.direction
                   self.player.rect.bottomleft = self.player.position 
        
        #See if a player collided with a ruby 
        if pygame.sprite.spritecollide(self.player, self.ruby_group, True):
            self.ruby_pickup_sound.play()
            self.score += 100
            self.player.health += 10 
            if self.player.health > self.player.STARTING_HEALTH:
                self.player.health = self.player.STARTING_HEALTH

        #See if a living zombie Collidied with a ruby
        for zombie in self.zombie_group:
            if zombie.is_dead == False: 
                if pygame.sprite.spritecollide(zombie, self.ruby_group, True):
                    self.lost_ruby_sound.play() 
                    zombie = Zombie(self.platform_group, self.portal_group, self.round_number, 5 + self.round_number)
                    self.zombie_group.add(zombie)
            if event.tpye == pygame.QUIT: 
                is_paused = False 
                running = False 
                pygame.mixer.music.stop()
                     
    def check_round_completion(self):
        if self.round_time == 0:
            self.start_new_round()

    def check_game_over(self):
        if self.player.health <= 0:
            pygame.mixer.music.stop()
            self.pause_game("Game Over! Final Score: " + str(self.score), "Press 'enter' to play again...")
            self.reset_game()

    def start_new_round(self):
        self.round_number += 1
        #Decrease Zombie Creation time 
        if self.round_number < self.STARTING_ZOMBIE_CREATION_TIME:
            self.zombie_creation_time -= 1 
        #Reset round values 
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()
        self.player.reset()
        self.pause_game("You Survived the Night!", "Press 'Enter' to continue...")

    def pause_game(self, main_text, sub_text):
        global running 
        pygame.mixer.music.pause()
        #Set Colors 
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        GREEN = (25, 200, 25)

        #Create main pause Text 
        main_text = self.title_font.render(main_text, True, GREEN)
        main_rect = main_text.get_rect() 
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text 
        sub_text = self.title_font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Display the pause text 
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True 
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        pygame.mixer.music.unpause()
                #User wants to quit 
                if event.type == pygame.QUIT: 
                    is_paused = False
                    running = False 
                    pygame.mixer.music.stop()
    
    def reset_game(self):
        self.score = 0 
        self.round_number = 1 
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

        self.player.health = self.player.STARTING_HEALTH
        self.player.reset()
        

    
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

    def __init__(self, x, y, platform_group, portal_group, bullet_group):
        super().__init__()
        self.HORIZONTAL_ACCELERATION = 2 
        self.HORIZONTAL_FRICTION = 0.15 
        self.VERTICAL_ACCLERATION = 0.8 #Gravity 
        self.VERTICAL_JUMP_SPEED = 18 
        self.STARTING_HEALTH = 100 

        #animation frames 
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        #Move
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (1).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (2).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (3).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (4).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (5).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (6).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (7).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (8).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (9).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/run/Run (10).png"), (64,64)))
        for sprite in self.move_right_sprites: 
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #Idle animations 
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (1).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (2).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (3).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (4).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (5).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (6).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (7).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (8).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (9).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/idle/Idle (10).png"), (64,64)))
        for sprite in self.idle_right_sprites: 
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #Jumping animations 
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (1).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (2).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (3).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (4).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (5).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (6).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (7).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (8).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (9).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/jump/Jump (10).png"), (64,64)))
        for sprite in self.jump_right_sprites: 
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #Attacking Animations 
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (1).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (2).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (3).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (4).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (5).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (6).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (7).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (8).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (9).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/player/attack/Attack (10).png"), (64,64)))
        for sprite in self.attack_right_sprites: 
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #Load Image and get rect 
        self.current_sprite = 0 
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        #attach sprite groups 
        self.platform_group = platform_group 
        self.portal_group = portal_group 
        self.bullet_group = bullet_group 

        #Animation booleans 
        self.animate_jump = False 
        self.animate_fire = False 

        #Load Sounds 
        self.jump_sound = pygame.mixer.Sound("./assets/sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("./assets/sounds/slash_sound.wav")
        self.portal_sound = pygame.mixer.Sound("./assets/sounds/portal_sound.wav")
        self.hit_sound = pygame.mixer.Sound("./assets/sounds/player_hit.wav")

        #Vectors 
        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

        #Set initial player values 
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y 


    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()

    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = 1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .5)
        else: 
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .5)
            else: 
                self.animate(self.idle_left_sprites, .5)
        
        #Calculate new values 
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        #Update rect based on calc
        if self.position.x < 0: 
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0 
        
        self.rect.bottomleft = self.position

    def check_collisions(self):
        #Collision check between player and platform 
        if self.velocity.y > 0: 
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0 
        
        if self.velocity.y < 0: 
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
            if collided_platforms:
                self.velocity.y = 0 
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position
        
        #Collision check for portals 
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150 
            # Top and Bottom 
            if self.position.y > WINDOW_HEIGHT//2: 
                self.position.y = 64 
            else: 
                self.position.y = WINDOW_HEIGHT - 132 
            self.rect.bottomleft = self.position

    def check_animations(self):
        #animate jump 
        if self.animate_jump:
            if self.velocity.x > 0: 
                self.animate(self.jump_right_sprites, .1)
            else: 
                self.animate(self.jump_left_sprites, .1)
        
        #Animate player attack 
        if self.animate_fire:
            if self.velocity.x > 0: 
                self.animate(self.attack_right_sprites, .25)
            else: 
                self.animate(self.attack_left_sprites, .25)

    def jump(self):
        #Only jump on platform 
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.jump_sound.play()
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
            self.animate_jump = True

    def fire(self):
        self.slash_sound.play()
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        self.animate_fire = True 

    def reset(self):
        self.position = vector(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1: 
            self.current_sprite += speed 
        else: 
            self.current_sprite = 0 
            if self.animate_jump:
                self.animate_jump = False
            #End attack animation 
            if self.animate_fire: 
                self.animate_fire = False
        self.image = sprite_list[int(self.current_sprite)]

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y, bullet_group, player):
        super().__init__() 
        self.VELOCITY = 20 
        self.RANGE = 500 

        #Load image and get rect 
        if player.velocity.x > 0: 
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/player/slash.png"), (32,32))
        else: 
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("./assets/images/player/slash.png"), True, False), (32,32))
            self.VELOCITY = -1 * self.VELOCITY
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.starting_x = x 
        bullet_group.add(self)

    def update(self):
        self.rect.x += self.VELOCITY
        if abs(self.rect.x - self.starting_x) > self.RANGE: 
            self.kill()

class Zombie(pygame.sprite.Sprite):

    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        super().__init__()
        self.VERTICAL_ACCLERATION = 3 #Gravity 
        self.RISE_TIME = 2 
         
        #animation frames 
        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.die_right_sprites = []
        self.die_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []

        gender = random.randint(0,1)
        if gender == 0: 
            #walking 
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (1).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (2).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (3).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (4).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (5).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (6).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (7).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (8).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (9).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/walk/walk (10).png"), (64,64)))
            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))
            #dying 
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (1).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (2).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (3).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (4).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (5).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (6).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (7).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (8).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (9).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (10).png"), (64,64)))
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
            #Rising 
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (10).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (9).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (8).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (7).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (6).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (5).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (4).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (3).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (2).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/boy/dead/Dead (1).png"), (64,64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        else: 
            #walking 
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (1).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (2).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (3).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (4).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (5).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (6).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (7).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (8).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (9).png"), (64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/walk/walk (10).png"), (64,64)))
            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))
            #dying 
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (1).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (2).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (3).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (4).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (5).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (6).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (7).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (8).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (9).png"), (64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (10).png"), (64,64)))
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
            #Rising 
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (10).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (9).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (8).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (7).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (6).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (5).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (4).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (3).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (2).png"), (64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/zombie/girl/dead/Dead (1).png"), (64,64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #Load Image and get rect for zombie
        self.direction = random.choice([-1,1])
        self.current_sprite = 0 
        if self.direction == -1: 
            self.image = self.walk_left_sprites[self.current_sprite]
        else: 
            self.image = self.walk_right_sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, WINDOW_WIDTH - 100), -100)
        #attach sprite groups 
        self.platform_group = platform_group 
        self.portal_group = portal_group 

        #animation booleans 
        self.animate_death = False 
        self.animate_rise = False 

        #load sounds 
        self.hit_sound = pygame.mixer.Sound("./assets/sounds/zombie_hit.wav")
        self.kick_sound = pygame.mixer.Sound("./assets/sounds/zombie_kick.wav")
        self.portal_sound = pygame.mixer.Sound("./assets/sounds/portal_sound.wav")

        #Kinematics 
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(self.direction * random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

        #Intial zombie values
        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0
        
    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()
        #Determine when teh zombie should rise from the dead
        if self.is_dead:
            self.frame_count += 1
            if self.frame_count % FPS == 0:
                self.round_time += 1
                if self.round_time == self.RISE_TIME:
                    self.animate_rise = True
                    #When the zombie died, the image was kept as the last image
                    #When it rises, we want to start at index 0 of our rise_sprite lists
                    self.current_sprite = 0


    def move(self):
        if not self.is_dead:
            if self.direction == -1: 
                self.animate(self.walk_left_sprites, .5)
            else: 
                self.animate(self.walk_right_sprites, .5)

            #Calculate new values 
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration

            #Update rect based on calc
            if self.position.x < 0: 
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0 
            
            self.rect.bottomleft = self.position

    def check_collisions(self):
        #Collision check between zombie and platform 
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0 
        
        #Collision check for portals 
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150 
            # Top and Bottom 
            if self.position.y > WINDOW_HEIGHT//2: 
                self.position.y = 64 
            else: 
                self.position.y = WINDOW_HEIGHT - 132 
            self.rect.bottomleft = self.position


    def check_animations(self):
        #animate zombie death 
        if self.animate_death: 
            if self.direction == 1: 
                self.animate(self.die_right_sprites, .095)
            else: 
                self.animate(self.die_left_sprites, .5)
            
        #Animate the zombie rise 
        if self.animate_rise:
            if self.direction == 1: 
                self.animate(self.rise_right_sprites, 0.95)
            else: 
                self.animate(self.rise_left_sprites, 0.95)

    def death(self):
        pass 

    def rise(self):
        pass

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            #End the death animation
            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False
            #End the rise animation
            if self.animate_rise:
                self.animate_rise = False
                self.is_dead = False
            #End the rise animation 
            if self.animate_rise:
                self.animate_rise = False 
                self.is_dead = False
                self.frame_count = 0 
                self.round_time = 0 
    
        self.image = sprite_list[int(self.current_sprite)]

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

    def __init__(self, platform_group, portal_group):
        super().__init__() 
        self.VERTICAL_ACCLERATION = 3 
        self.HORIZONTAL_VELOCITY = 5

        self.ruby_sprites = []

        # Rotating 
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile000.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile001.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile002.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile003.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile004.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile005.png"), (64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile006.png"), (64,64)))

        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WINDOW_WIDTH//2, 100)

        self.platform_group = platform_group 
        self.portal_group = portal_group 

        #Load Sounds 
        self.portal_sound = pygame.mixer.Sound("./assets/sounds/portal_sound.wav")

        #Kinematic Vectors 
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(random.choice([-1 * self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

    def update(self):
        self.animate(self.ruby_sprites, .25)
        self.move()
        self.check_collisions()

    def check_collisions(self):
        #Collision check between ruby and platform 
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0 
        
        #Collision check for portals 
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150 
            # Top and Bottom 
            if self.position.y > WINDOW_HEIGHT//2: 
                self.position.y = 64 
            else: 
                self.position.y = WINDOW_HEIGHT - 132 
            self.rect.bottomleft = self.position

    def move(self):
        #Calculate new values 
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        #Update rect based on calc
        if self.position.x < 0: 
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0 
        
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1: 
            self.current_sprite += speed 
        else: 
            self.current_sprite = 0 
        self.image = sprite_list[int(self.current_sprite)]

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
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile004.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile005.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile006.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile007.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile008.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile009.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile010.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile011.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile012.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile013.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile014.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile015.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile016.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile017.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile018.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile019.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile020.png"), (72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("./assets/images/portals/purple/tile021.png"), (72,72)))

        #Load an image get a rect 
        self.current_sprite = random.randint(0, len(self.portal_sprites)-1)
        self.image = self.portal_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        portal_group.add(self)
        
    def update(self):
        self.animate(self.portal_sprites, .2)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1: 
            self.current_sprite += speed 
        else: 
            self.current_sprite = 0 
        self.image = sprite_list[int(self.current_sprite)]

#Create Sprite groups 
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group() 
my_player_group = pygame.sprite.Group() 
my_bullet_group = pygame.sprite.Group() 
my_zombie_group = pygame.sprite.Group()  
my_portal_group = pygame.sprite.Group()  
my_ruby_group = pygame.sprite.Group() 

#Create tile map for the game
# 0 -> no tile, 1 -> dirt 2-5 -> platforms, 6 -> ruby maker 7-8 -> portals, 9 - player
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
            Portal(j*32, i*32, 'green', my_portal_group)
        elif tile_map[i][j] == 8: 
            Portal(j*32, i*32, 'purple', my_portal_group)
        elif tile_map[i][j] == 9: 
            my_player = Player(j*32 -32, i*32 + 32, my_platform_group, my_portal_group, my_bullet_group)
            my_player_group.add(my_player)
      
#Background Image
background_image = pygame.transform.scale(pygame.image.load("./assets/images/background.png"), (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

#Create game object 
my_game = Game(my_player, my_zombie_group, my_platform_group, my_portal_group, my_bullet_group, my_ruby_group)
my_game.pause_game("Zombie Knight", "Press 'enter' to Begin")
pygame.mixer.music.play(-1,0.0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            #Player wants to jump
            if event.key == pygame.K_SPACE:
                my_player.jump()
            #Player wants to fire
            if event.key == pygame.K_UP: 
                my_player.fire()
            #Rain zombies...for testing purposes 
            if event.key == pygame.K_RETURN:
                zombie = Zombie(my_platform_group, my_portal_group, 2,7)
                my_zombie_group.add(zombie)


    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Draw the tiles 
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    #Update and draw sprite groups for the game
    my_portal_group.update()
    my_portal_group.draw(display_surface)

    my_player_group.update() 
    my_player_group.draw(display_surface)

    my_bullet_group.update()
    my_bullet_group.draw(display_surface)

    my_zombie_group.update() 
    my_zombie_group.draw(display_surface)
    
    my_ruby_group.update()
    my_ruby_group.draw(display_surface)

    #Update and draw game assets
    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
