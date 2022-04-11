"""This code was written by Magnus Lyngra"""
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
    def __init__(self, color, width, height, speed, pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

#Parent class. The child classes inherit from this which in turn inherits from Drawable_objects. Responsible for variables that move objects
class Moving_objects(Drawable_objects):
    """Parent class that inherits from Drawable Objects, but all other classes except for the game class inherits from it."""
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.pos = pos
        self.speed = Vector2(0, 0)
        self.rect = self.pos
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        
#Player 1 class. Holds the variables for the player 1 object.
class Player1(Moving_objects):
    """Player 1 class that holds the variables for the player 1 object.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(1, 1)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = pos
    
    #check for collision between screen and player1
    def collision_screen(self, player1_ob):
        
        if self.rect.left > 1920: 
            self.rect.left = 1920
            SCOREP1 -= 1
        if self.rect.right < 0:
            self.rect.right = 0
            SCOREP1 -= 1
        if self.rect.top > 1080:
            self.rect.top = 1080
            SCOREP1 -= 1
        if self.rect.bottom > 1080:
            self.rect.bottom = 1080
            SCOREP1 -= 1
    
    #updates the position of player 1
    def movement(self):
        
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.UP:
                self.rect.x += self.new_speed.x
                self.rect.y += self.new_speed.y"""
    
    #creates a missile object
    def create_missile1(self):
        return Missile1(GREEN, 5, 5, self.new_speed, self.pos)
    
#Player 2 class. Holds the variables for the player 2 object
class Player2(Moving_objects):
    """Player 2 class that holds the variables for the player 2 object.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(1, 1)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = pos
        
    #Checks for collisions between player 2 and the screen
    def collision_screen(self, player2_ob):
        #make asteroids wrap around to the opposite side of the screen when they leave it (borrowed from previous hand in boids.py)
        if self.rect.left > 1920: 
            self.rect.left = 1920
            SCOREP2 -= 1
        if self.rect.right < 0:
            self.rect.right = 0
            SCOREP2 -= 1
        if self.rect.top > 1080:
            self.rect.top = 1080
            SCOREP2 -= 1
        if self.rect.bottom > 1080:
            self.rect.bottom = 1080
            SCOREP2 -= 1
    
    #Updates the position of player 2
    def movement(self):
        
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.UP:
                self.rect.x += self.new_speed.x
                self.rect.y += self.new_speed.y"""
    
    #Creates another missile object
    def create_missile2(self):
        return Missile2(BLUE, 5, 5, self.new_speed, self.pos)

#First missile class. Holds the variables for the first missile object
class Missile1(Player1):
    """Missile 1 class that holds the variables for the Missile 1 object.

    Args:
        Player 1 (Parent): Player 1 is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.pos = (40, 1000)
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center = (self.pos))
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
    
    #Method responsible for updating the missile's position
    def update(self):
        
        self.rect.x += self.new_speed.x + 1
        self.rect.y += self.new_speed.y + 1

#Second missile class. Holds the variables for the second missile object  
class Missile2(Player2):
    """Missile 2 class that holds the variables for the Missile 2 object.

    Args:
        Player2 (Parent): Player2 is the parent class for this class and this class inherits from it
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.pos = (1860, 1000)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center = (self.pos))
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
    
    #Updates the position of the second missile object
    def update(self):
        
        self.rect.x += self.new_speed.x + 1
        self.rect.y += self.new_speed.y + 1

#Class responsible for the asteroids object variables   
class Asteroids(Moving_objects):
    """Asteroids class that holds the variables for the Asteroids object.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((70, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed.x = 1
        self.speed.y = 0
        self.pos = pos
    
    #Method that ensures that when the asteroids leave the surface they reappear on the opposite side
    def screen_wrap(self):
        
        if self.rect.left > 1920: 
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = 1920
        if self.rect.top > 1080:
            self.rect.bottom = 0
        if self.rect.bottom > 1080:
            self.rect.top = 0
    
    #updates the position of the asteroids
    def update(self):
        self.screen_wrap()
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

#Class for the platforms. Holds the variables for the plattform object
class Platforms(Moving_objects):
    """Platforms class that holds the variables for the Platforms objects.

    Args:
        Moving_objects (Parent): Moving objects is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((40, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.pos = pos
        
#Game class. Responsible for the game loop, most of the collision detection and creating most of the objects apart from the missiles.    
class Game:
    """Game class that's responsible for creating most of the objects, doing most of the collision checks and running the game loop."""
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080), 0, 0)
        self.player1 = pygame.sprite.Group()
        self.player2 = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.missile1 = pygame.sprite.Group()
        self.missile2 = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
    
    #creates player 1 object and adds it to its sprite group and the main sprite group for all the sprites
    def create_player1(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2(1, 1)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.pos = (30, 1000)
        self.player1_ob = Player1(GREEN, 30, 30, self.speed, self.pos)
        self.player1.add(self.player1_ob)
        self.all_sprites_list.add(self.player1_ob)
    
    #creates player 2 object and adds it to its sprite group and the main sprite group for all the sprites
    def create_player2(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2(1, 1)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.pos = (1850, 1000)
        self.player2_ob = Player2(BLUE, 30, 30, self.speed, self.pos)
        self.player2.add(self.player2_ob)
        self.all_sprites_list.add(self.player2_ob)
        
    def create_missile1(self):
        self.image = pygame.Surface((5, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (30, 1000)
        self.missile1_ob = Missile1(GREEN, 5, 5, self.new_speed, self.pos)
        self.missiles.add(self.missile1_ob)
        self.all_sprites_list.add(self.missile1_ob)
        
    def create_missile2(self):
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (1850, 1000)
        self.missile2_ob = Missile2(BLUE, 5, 5, self.new_speed, self.pos)
        self.missiles.add(self.missile2_ob)
        self.all_sprites_list.add(self.missile2_ob)
    
    #creates asteroids object and adds it to its sprite group and the main sprite group for all the sprites
    def create_asteroids(self):
        self.image = pygame.Surface((70, 70))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.speed = Vector2(1, 1)
        self.pos = (random.randint(0, 0), random.randint(100, 800))
        self.asteroids_ob = Asteroids(RED, 70, 70, self.speed, self.pos)
        self.asteroids.add(self.asteroids_ob)
        self.all_sprites_list.add(self.asteroids_ob)
    
    #creates first platform object and adds it to its sprite group and the main sprite group for all the sprites 
    def create_platform1(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = (25, 1030)
        self.platform_ob1 = Platforms(GREY, 40, 50, self.speed, self.pos)
        self.platforms.add(self.platform_ob1)
        self.all_sprites_list.add(self.platform_ob1)
    
    #creates second platform object and adds it to its sprite group and the main sprite group for all the sprites
    def create_platform2(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = (1845, 1030)
        self.platform_ob2 = Platforms(GREY, 40, 50, self.speed, self.pos)
        self.platforms.add(self.platform_ob2)
        self.all_sprites_list.add(self.platform_ob2)
    
    #checks for collisions between players. Destroys them if they collide
    def collision_players(self):
        if pygame.sprite.groupcollide(self.player1, self.player2, True, True):
            print("YOU BOTH LOSE! LOSERS!")
    #checks for collisions between player 1 and asteroids. Destroys player and reduces score by 1 if they collide
    def collision_p1asteroids(self):
        if pygame.sprite.groupcollide(self.player1, self.asteroids, True, False):
            print("Player 1 down, player 2 has won.")
            SCOREP1 -= 1
    #checks for collisions between player 2 and asteroids. Destroys player and reduces score by 1 if they collide
    def collision_p2asteroids(self):
        if pygame.sprite.groupcollide(self.player2, self.asteroids, True, False):
            print("Player 2 down, player 1 has won.")
            SCOREP2 -= 1
    #checks for collision between player 1 and platforms. Resets fuel if they collide
    def collision_p1platforms(self):
        if pygame.sprite.groupcollide(self.player1, self.platforms, False, False):
            print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            FUEL = 50
    #checks for collisions between player 2 and platforms. Resets fuel if they collide
    def collision_p2platforms(self):
        if pygame.sprite.groupcollide(self.player2, self.platforms, False, False):
            print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            FUEL = 50
    #checks for collisions between player 1 and player 2's missile. If they collide, player 1 loses a point and is destroyed
    def collision_missile1(self):
        if pygame.sprite.groupcollide(self.player1, self.missile2, True, True):
            SCOREP1 -= 1
    #checks for collisions between player 2 and player 1's missile. If they collide, player 2 loses a point and is destroyed        
    def collision_missile2(self):
        if pygame.sprite.groupcollide(self.player2, self.missile1, True, True):
            SCOREP2 -= 1
    
    #Method for calling the methods that creates objects     
    def setup(self):
        self.create_player1()
        self.create_player2()
        #self.create_missile1()
        #self.create_missile2()
        for i in range(3):
            self.create_asteroids()
        self.create_platform1()
        self.create_platform2()
    
    #updates the surface, sprites and draws the sprites
    def update_game(self):
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
    
    #text for displaying each player's score ingame
    def score_text(self):
        font = pygame.font.Font(None, 60)
        p1_score = font.render(str(SCOREP1), 1, WHITE)
        self.screen.blit(p1_score, (700,10))
        p2_score = font.render(str(SCOREP2), 1, WHITE)
        self.screen.blit(p2_score, (1220,10))
    
    #text for displaying the winner of the game if they reach 50 points
    def winner_text(self):
        font = pygame.font.Font(None, 200)
        p1w = "Player 1 has won the game"
        p2w = "Player 2 has won the game"
        if SCOREP1 >= 50:
            p1_winner = font.render(str(p1w), 1, WHITE)
            self.screen.blit(p1_winner, (700,10))
        if SCOREP2 >= 50:
            p2_winner = font.render(str(p2w), 1, WHITE)
            self.screen.blit(p2_winner, (1220,10))
    
    #game loop/event loop, where all the magic happens, in particular checking if the player's controls are used and updating positions etc if they are
    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Mayhem')
        fuel_loss = pygame.USEREVENT + 1
        self.setup()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        #apply thrust on object
                        Player1.movement(self)
                    if event.key == pygame.K_a:
                        #rotate object left
                        pygame.transform.rotate(Player1.image, 20)
                    if event.key == pygame.K_d:
                        #rotate object right
                        pygame.transform.rotate(Player1.image, -20)
                    if event.key == pygame.K_LSHIFT:
                        #fire weapon
                        self.missile2.add(Player2.create_missile2(self))
                        self.all_sprites_list.add(Player2.create_missile2(self))
                    if event.key == pygame.K_UP:
                        #apply thrust on object
                        Player2.movement(self)
                    if event.key == pygame.K_LEFT:
                        #rotate object left
                        pygame.transform.rotate(Player2.rect, 20)
                    if event.key == pygame.K_RIGHT:
                        #rotate object right
                        pygame.transform.rotate(Player2.rect, -20)
                    if event.key == pygame.K_RSHIFT:
                        #fire weapon
                        self.missile1.add(Player1.create_missile1(self))
                        self.all_sprites_list.add(Player1.create_missile1(self))
                        
                pygame.time.set_timer(fuel_loss, 1000)
                if pygame.event == fuel_loss:
                    FUEL - 5
                    if FUEL == 0:
                        pygame.sprite.Sprite.kill(self.player1_ob, self.player2_ob)
                        print("You have run out of fuel and are now floating aimlessly into space. Look for a tesla, maybe it has some fuel")


            #self.move()
            self.score_text()
            self.winner_text()
            self.update_game()
        pygame.quit()
        quit() 

#for initiating the game
if __name__ == '__main__':
    pygame.init()
    br = Game()
    br.game_loop()