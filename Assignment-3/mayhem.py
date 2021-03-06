"""This code was written by Magnus Lyngra"""
import os
import pygame
from pygame import Vector2
import math
import config
from config import *
import random
import math
import sympy
import cProfile

#Top parent class, responsible for variables needed to draw an object
class Drawable_objects(pygame.sprite.Sprite):
    """Top parent class. Responsible for variables needed to draw an object"""
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        #self.image.fill(self.color)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

#Parent class. The child classes inherit from this which in turn inherits from Drawable_objects. Responsible for variables that move objects
class Moving_objects(Drawable_objects):
    """Parent class that inherits from Drawable Objects, but all other classes except for the game class inherits from it."""
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2()
        #self.pos = Vector2(0, 0)
        self.thrust = Vector2()
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time
        self.max_speed = Vector2(-2, -2)
        
        
#Player 1 class. Holds the variables for the player 1 object.
class Player(Moving_objects):
    """Player 1 class that holds the variables for the player 1 object.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        #self.image = self.p1_img
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2(-1, -1)
        self.thrust = Vector2(0, -3)
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time
        
    def update(self):
        """updates the position of players
        """
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.rect.x += self.new_speed.x
            self.rect.y += self.new_speed.y
        elif pygame.KEYUP:
            self.rect.y += GRAVITY.y
        
            
    #def create_missile(self):
        #return Missile(GREEN, 5, 5, self.speed, self.pos)

#Player 1 class. Holds the variables for the player 1 object.
class Player2(Moving_objects):
    """Player 2 class that holds the variables for the player 2 object.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        #self.image = self.p2_img
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.speed = Vector2(-1, -1)
        self.thrust = Vector2(0, -3)
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time

    #updates the position of players
    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.rect.x += self.new_speed.x
            self.rect.y += self.new_speed.y
            
        elif pygame.KEYUP:
            self.rect.y += GRAVITY.y
    
    def rotate(self):
        self.player2_ob.new_speed.rotate_ip(5)
    
#First missile class. Holds the variables for the first missile object
class Missile(Player):
    """Missile 1 class that holds the variables for the Missile 1 object.

    Args:
        Player 1 (Parent): Player 1 is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = pos
        self.speed = Vector2(6, 0)
        self.thrust = Vector2(0, -5)
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time
    
    def update(self):
        """Method responsible for updating the missile's position
        """
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        
#First missile class. Holds the variables for the first missile object
class Missile2(Player):
    """Missile 1 class that holds the variables for the Missile 1 object.

    Args:
        Player 1 (Parent): Player 1 is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = pos
        self.speed = Vector2(-6, 0)
        self.thrust = Vector2(0, -5)
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time
    
    #Method responsible for updating the missile's position
    def update(self):
        
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        

#Class responsible for the asteroids object variables   
class Asteroids(Moving_objects):
    """Asteroids class that holds the variables for the Asteroids object.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        #self.image = self.asteroids_img
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed.x = 1
        self.speed.y = 0
        self.pos = pos
        
    def screen_wrap(self):
        """Method that ensures that when the asteroids leave the surface they reappear on the opposite side
        """
        if self.rect.left > 1920: 
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = 1920
        if self.rect.top > 1080:
            self.rect.bottom = 0
        if self.rect.bottom > 1080:
            self.rect.top = 0
    
    def update(self):
        """updates the position of the asteroids
        """
        self.screen_wrap()
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

#Class for the platforms. Holds the variables for the plattform object
class Platforms(Moving_objects):
    """Platforms class that holds the variables for the Platforms objects.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        #self.image = self.bg_img
        #self.image.fill(GREY)
        #self.rect = self.image.get_rect()
        #self.rect.x = self.pos[0] 
        #self.rect.y = self.pos[1]
        #self.pos = pos
        
class Floor(Moving_objects):
    """Floor class that keeps players from falling below the screen.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, image, width, height, speed, pos):
        super().__init__(color, image, width, height, speed, pos)
        
        
#Game class. Responsible for the game loop, most of the collision detection and creating most of the objects apart from the missiles.    
class Game:
    """Game class that's responsible for creating most of the objects, doing most of the collision checks and running the game loop."""
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080), 0, 0, pygame.SRCALPHA)
        self.player1 = pygame.sprite.Group()
        self.player2 = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.missile1 = pygame.sprite.Group()
        self.missile2 = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.score_pl1 = 0
        self.score_pl2 = 0
        self.currp1_fuel = 100
        self.currp2_fuel = 100
    
    def create_player1(self):
        """creates player 1 object and adds it to its sprite group and the main sprite group for all the sprites"""
        self.image = (self.p1_img, pygame.SRCALPHA)
        self.speed = Vector2(0, 0)
        self.pos = Vector2(0, -0.2)
        self.pos.xy = 30, 1000
        self.dir = Vector2(0, 5)
        self.dir = Vector2(0, 5)
        self.player1_ob = Player(BLUE, self.p1_img, 40, 40, self.speed, self.pos)
        self.player1.add(self.player1_ob)
        self.all_sprites_list.add(self.player1_ob)
    
    def create_player2(self):
        """creates player 2 object and adds it to its sprite group and the main sprite group for all the sprites
        """
        self.image = self.p2_img
        self.speed = Vector2(0, 0)
        self.pos = Vector2(0, -0.2)
        self.pos.xy = 1850, 1000
        self.dir = Vector2(0, 5)
        self.n_dir = Vector2(0, -5)
        self.player2_ob = Player2(GREEN, self.p2_img, 40, 40, self.speed, self.pos)
        self.player2.add(self.player2_ob)
        self.all_sprites_list.add(self.player2_ob)
        
    def create_missile1(self):
        """creates missile 1 object and adds it to its sprite group and the main sprite group for all the sprites
        """
        self.pos = self.player1_ob.pos
        self.missile1_ob = Missile(BLUE, self.missile1_img, 15, 15, self.speed, (self.player1_ob.rect.x, self.player1_ob.rect.y))
        self.missile1.add(self.missile1_ob)
        self.all_sprites_list.add(self.missile1_ob)
        
    def create_missile2(self):
        """creates missile 1 object and adds it to its sprite group and the main sprite group for all the sprites
        """
        self.pos = self.player2_ob.pos
        self.missile2_ob = Missile2(GREEN, self.missile2_img, 15, 15, self.speed, (self.player2_ob.rect.x, self.player2_ob.rect.y))
        self.missile2.add(self.missile2_ob)
        self.all_sprites_list.add(self.missile2_ob)
        print(self.player2_ob.pos)
        
    def create_asteroids(self):
        """creates asteroids object and adds it to its sprite group and the main sprite group for all the sprites
        """
        self.speed = Vector2(1, 1)
        self.pos_a = (random.randint(0, 0), random.randint(100, 800))
        self.asteroids_ob = Asteroids(RED, self.asteroids_img, 100, 100, self.speed, self.pos_a)
        self.asteroids.add(self.asteroids_ob)
        self.all_sprites_list.add(self.asteroids_ob)
    
    def create_platform1(self):
        """creates first platform object and adds it to its sprite group and the main sprite group for all the sprites 
        """
        self.pos_pf1 = (25, 1030)
        self.platform_ob1 = Platforms(GREY, self.platform_img, 70, 50, self.speed, self.pos_pf1)
        self.platforms.add(self.platform_ob1)
        self.all_sprites_list.add(self.platform_ob1)
    
    def create_platform2(self):
        """creates second platform object and adds it to its sprite group and the main sprite group for all the sprites
        """
        self.pos_pf2 = (1845, 1030)
        self.platform_ob2 = Platforms(GREY, self.platform_img, 70, 50, self.speed, self.pos_pf2)
        self.platforms.add(self.platform_ob2)
        self.all_sprites_list.add(self.platform_ob2)
    
    def create_floor(self):
        """creates first platform object and adds it to its sprite group and the main sprite group for all the sprites 
        """
        self.pos = (1, 1075)
        self.speed = Vector2(0, 0)
        self.floor_ob = Floor(BLACK, self.image, 1920, 10, self.speed, self.pos)
        self.floor.add(self.floor_ob)
        self.all_sprites_list.add(self.floor_ob)
    
    def collisions(self, player1_ob, player2_ob):
        """check for collision between screen and player1
        """
        
        if player1_ob.rect.left > 1920: 
            player1_ob.rect.left = 1920
            
        if player1_ob.rect.left < 0:
            player1_ob.rect.left = 0
        
        if player1_ob.rect.right > 1920: 
            player1_ob.rect.right = 1920
            
        if player1_ob.rect.right < 0:
            player1_ob.rect.right = 0
        
        if player1_ob.rect.top > 1920: 
            player1_ob.rect.top = 1920
        
        if player1_ob.rect.top < 0:
            player1_ob.rect.top = 0
        
        if player1_ob.rect.bottom > 1920: 
            player1_ob.rect.bottom = 1920
            
        if player1_ob.rect.bottom < 0:
            player1_ob.rect.bottom = 0
            
    #Checks for collisions between player 2 and the screen
        
        if player2_ob.rect.left > 1920: 
            player2_ob.rect.left = 1920
            
        if player2_ob.rect.left < 0:
            player2_ob.rect.left = 0
        
        if player2_ob.rect.right > 1920: 
            player2_ob.rect.right = 1920
            
        if player2_ob.rect.right < 0:
            player2_ob.rect.right = 0
        
        if player2_ob.rect.top > 1920: 
            player2_ob.rect.top = 1920
        
        if player2_ob.rect.top < 0:
            player2_ob.rect.top = 0
        
        if player2_ob.rect.bottom > 1920: 
            player2_ob.rect.bottom = 1920
            
        if player2_ob.rect.bottom < 0:
            player2_ob.rect.bottom = 0
            
        if player2_ob.rect.y > 1080:
            player2_ob.rect.y = 1080
            
    
    #checks for collisions between players. Destroys them if they collide
        if pygame.sprite.groupcollide(self.player1, self.player2, True, True):
            print("YOU BOTH LOSE! LOSERS!")
            
    #checks for collisions between player 1 and asteroids. Destroys player and reduces score by 1 if they collide
        if pygame.sprite.groupcollide(self.player1, self.asteroids, True, False):
            print("Player 1 down, player 2 has won.")
            
    #checks for collisions between player 2 and asteroids. Destroys player and reduces score by 1 if they collide
        if pygame.sprite.groupcollide(self.player2, self.asteroids, True, False):
            print("Player 2 down, player 1 has won.")
            
    #checks for collision between player 1 and platforms. Resets fuel if they collide
        if pygame.sprite.groupcollide(self.player1, self.platforms, False, False):
            #print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            self.player1_ob.rect.x = 29
            self.player1_ob.rect.y = 989
            self.currp1_fuel = 100
            
    #checks for collisions between player 2 and platforms. Resets fuel if they collide
        if pygame.sprite.groupcollide(self.player2, self.platforms, False, False):
            #print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            self.player2_ob.rect.x = 1849
            self.player2_ob.rect.y = 989
            self.currp2_fuel = 100
            
        #checks for collision between player 1 and floor. 
        if pygame.sprite.groupcollide(self.player1, self.floor, False, False):
            self.player1_ob.rect.y = 1045
            
            
    #checks for collisions between player 2 and floor. 
        if pygame.sprite.groupcollide(self.player2, self.floor, False, False):
            self.player2_ob.rect.y = 1045
            
    #checks for collisions between player 1 and player 2's missile. If they collide, player 1 loses a point and is destroyed
        if pygame.sprite.groupcollide(self.player1, self.missile2, False, True):
            self.score_pl1 -= 1
            self.score_pl2 += 1
            
    #checks for collisions between player 2 and player 1's missile. If they collide, player 2 loses a point and is destroyed        
        if pygame.sprite.groupcollide(self.player2, self.missile1, False, True):
            self.score_pl2 -= 1
            self.score_pl1 += 1
         
    def setup(self):
        """Method for calling the methods that creates objects
        """
        self.create_player1()
        self.create_player2()
        for i in range(3):
            self.create_asteroids()
        self.create_platform1()
        self.create_platform2()
        self.create_floor()
    
    def score_text(self):
        """text for displaying each player's score ingame
        """
        self.font = pygame.font.Font(None, 60)
        self.p1_score = self.font.render(str(self.score_pl1), 1, WHITE)
        self.screen.blit(self.p1_score, (900,10))
        self.p2_score = self.font.render(str(self.score_pl2), 1, WHITE)
        self.screen.blit(self.p2_score, (1420,10))
     
    def score_fuel(self):
        """text for fuel count  
        """
        self.font = pygame.font.Font(None, 60)
        self.fuel_count = "Fuel: "
        self.p1_fuel = self.font.render(str(self.currp1_fuel), 1, WHITE)
        self.screen.blit(self.p1_fuel, (400, 1040))
        self.p2_fuel = self.font.render(str(self.currp2_fuel), 1, WHITE)
        self.screen.blit(self.p2_fuel, (1120, 1040))
    
    """def winner_text(self):
        text for displaying the winner of the game if they reach 50 points
        
        self.font = pygame.font.Font(None, 50)
        self.p1w = "Player 1 has won the game"
        self.p2w = "Player 2 has won the game"
        if self.score_pl1 == 50:
            self.p1_winner = self.font.render(str(self.p1w), 1, WHITE)
            
        if self.score_pl2 == 50:
            self.p2_winner = self.font.render(str(self.p2w), 1, WHITE)"""
            
            
            
    def update_game(self):
        """updates the surface, sprites and draws the sprites
        """
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.p1_score, (700,10))
        self.screen.blit(self.p2_score, (1220,10))
        self.screen.blit(self.p1_fuel, (680,1040))
        self.screen.blit(self.p2_fuel, (1200,1040))
        self.screen.blit(self.p1_img, (self.player1_ob.rect.x, self.player1_ob.rect.y))
        self.screen.blit(self.p2_img, (self.player2_ob.rect.x, self.player2_ob.rect.y))
        for self.missile1_ob in self.missile1:
            self.screen.blit(self.missile1_img, (self.missile1_ob.rect.x, self.missile1_ob.rect.y))
        for self.missile2_ob in self.missile2:
            self.screen.blit(self.missile2_img, (self.missile2_ob.rect.x, self.missile2_ob.rect.y))
        self.screen.blit(self.platform_img, (self.platform_ob1.rect.x, self.platform_ob1.rect.y))
        self.screen.blit(self.platform_img, (self.platform_ob2.rect.x, self.platform_ob2.rect.y))
        for self.asteroids_ob in self.asteroids:
            self.screen.blit(self.asteroids_img, (self.asteroids_ob.rect.x, self.asteroids_ob.rect.y))
        
        #self.screen.blit(self.p1_winner, (700,10))
        #self.screen.blit(self.p2_winner, (1220,10))
        pygame.display.flip()
    
    def game_loop(self):
        """game loop/event loop, where all the magic happens, in particular checking if the player's controls are used and updating positions etc if they are
        """
        pygame.init()
        pygame.display.set_caption('Mayhem')
        self.p1_img = pygame.image.load(os.path.join("Assignment-3", 'enterprise.jpeg')).convert_alpha()
        self.p2_img = pygame.image.load(os.path.join("Assignment-3", 'borgcube.jpeg')).convert_alpha()
        self.platform_img = pygame.image.load(os.path.join("Assignment-3", 'platform.png')).convert_alpha()
        self.bg_img = pygame.image.load(os.path.join("Assignment-3", 'spacebg.jpeg'))
        self.asteroids_img = pygame.image.load(os.path.join("Assignment-3", 'asteroids.jpeg')).convert_alpha()
        self.missile1_img = pygame.image.load(os.path.join("Assignment-3", 'missile1.jpg')).convert_alpha()
        self.missile2_img = pygame.image.load(os.path.join("Assignment-3", 'missile2.jpg')).convert_alpha()
        fuel_loss = pygame.USEREVENT + 1
        pygame.time.set_timer(fuel_loss, 1000)
        pygame.mixer.music.load(os.path.join("Assignment-3", "trololo.mp3"))
        pygame.mixer.music.play(-1)
        self.setup()
        
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == fuel_loss and self.player1_ob.rect.x != 30 and self.player1_ob.rect.y != 1000:
                    self.currp1_fuel -= 2
                    
                if event.type == fuel_loss and self.player2_ob.rect.x != 1850 and self.player2_ob.rect.y != 1000:
                    self.currp2_fuel -= 2
                    
                            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                #rotate object left
                self.player1_ob.new_speed = self.player1_ob.new_speed.rotate(-3)
                print(self.player1_ob.speed)
                #self.rot_img = pygame.transform.rotate(self.image, 20)
                # draw the rotated image to the pygame app main window screen.
                #self.rot_img.blit(self.screen, self.p2_pos)
                        
            if pressed[pygame.K_d]:
                #rotate object right
                self.player1_ob.new_speed = self.player1_ob.new_speed.rotate(3)
                #self.rot_img = pygame.transform.rotate(self.image, -20)
                # draw the rotated image to the pygame app main window screen.
                #self.rot_img.blit(self.screen, self.p2_pos)
                        
            if pressed[pygame.K_LSHIFT]:
                #fire weapon
                self.create_missile1()
                self.missile1.add(self.missile1_ob)
                self.all_sprites_list.add(self.missile1_ob)
                self.missile1_ob.update()
                        
            if pressed[pygame.K_LEFT]:
                #rotate object left
                self.player2_ob.new_speed = self.player2_ob.new_speed.rotate(-3)
                #self.rot_img = pygame.transform.rotate(self.image, 20)
                # draw the rotated image to the pygame app main window screen.
                #self.rot_img.blit(self.screen, self.p1_pos)w
                        
            if pressed[pygame.K_RIGHT]:
                #rotate object right
                self.player2_ob.new_speed = self.player2_ob.new_speed.rotate(3)
                #self.rot_img = pygame.transform.rotate(self.image, -20)
                # draw the rotated image to the pygame app main window screen.
                #self.rot_img.blit(self.screen, self.p1_pos)
                        
            if pressed[pygame.K_RSHIFT]:
                #fire weapon
                self.create_missile2()
                self.missile2.add(self.missile2_ob)
                self.all_sprites_list.add(self.missile2_ob)
                self.missile2_ob.update()
                        
            if event.type == pygame.KEYUP:
                self.speed += GRAVITY
            
            if self.currp1_fuel <= 0:
                self.player1_ob.rect.y -= -3
                print("You have run out of fuel and are now floating aimlessly into space. Look for a tesla, maybe it has some fuel")
            if self.currp2_fuel <= 0:
                self.player2_ob.rect.y -= -3
                print("You have run out of fuel and are now floating aimlessly into space. Look for a tesla, maybe it has some fuel")

            #self.move()
            self.score_text()
            self.score_fuel()
            #self.winner_text()
            self.collisions(self.player1_ob, self.player2_ob)
            self.update_game()
            
        pygame.quit()
        quit() 

"""for initiating the game"""
if __name__ == '__main__':
    pygame.init()
    br = Game()
    br.game_loop()