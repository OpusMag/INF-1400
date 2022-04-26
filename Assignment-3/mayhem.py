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
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

#Parent class. The child classes inherit from this which in turn inherits from Drawable_objects. Responsible for variables that move objects
class Moving_objects(Drawable_objects):
    """Parent class that inherits from Drawable Objects, but all other classes except for the game class inherits from it."""
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2()
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
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.rot_img = self.image
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2(0, -5)
        self.thrust = Vector2(-5, -5)
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time

    #updates the position of player 1
    def update(self):
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.rect.x += self.new_speed.x
                        self.rect.y += self.new_speed.y
                        #if self.new_speed > Vector2(3, 3):
                            #self.new_speed = Vector2(3, 3)
                    elif event.key == pygame.K_UP:
                        self.rect.x += self.new_speed.x
                        self.rect.y += self.new_speed.y
                       # if self.new_speed > self.max_speed:
                            #self.new_speed = self.max_speed
            elif event.type == pygame.KEYUP:
                self.speed = Vector2(0, 0)
                self.speed += GRAVITY
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.UP:
                self.rect.x += self.new_speed.x
                self.rect.y += self.new_speed.y"""
    
#First missile class. Holds the variables for the first missile object
class Missile(Player):
    """Missile 1 class that holds the variables for the Missile 1 object.

    Args:
        Player 1 (Parent): Player 1 is the parent class for this class and this class inherits from it.
    """
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.speed = Vector2(0, 0)
        self.thrust = Vector2(-10, -10)
        self.acceleration = self.thrust + GRAVITY
        self.new_speed = self.speed + self.acceleration * self.time
    
    #Method responsible for updating the missile's position
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.rect.x += self.new_speed.x
                        self.rect.y += self.new_speed.y
                    elif event.key == pygame.K_RSHIFT:
                        self.rect.x += self.new_speed.x
                        self.rect.y += self.new_speed.y

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
       #make asteroids wrap around to the opposite side of the screen when they leave it (borrowed from previous hand in boids.py) 
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
        #self.image = pygame.Surface((40, 50))
        #self.image.fill(GREY)
        #self.rect = self.image.get_rect()
        #self.rect.x = self.pos[0] 
        #self.rect.y = self.pos[1]
        #self.pos = pos
        
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
        self.speed = Vector2(0, 0)
        self.p1_pos = (30, 1000)
        self.player1_ob = Player(GREEN, 30, 30, self.speed, self.p1_pos)
        self.player1.add(self.player1_ob)
        self.all_sprites_list.add(self.player1_ob)
    
    #creates player 2 object and adds it to its sprite group and the main sprite group for all the sprites
    def create_player2(self):
        self.image = pygame.Surface((30, 30))
        self.speed = Vector2(0, 0)
        self.p2_pos = (1850, 1000)
        self.player2_ob = Player(BLUE, 30, 30, self.speed, self.p2_pos)
        self.player2.add(self.player2_ob)
        self.all_sprites_list.add(self.player2_ob)
        
    def create_missile1(self, p1_pos):
        self.speed = Vector2(0, 0)
        self.pos = p1_pos
        self.missile1_ob = Missile(GREEN, 5, 5, self.speed, self.pos)
        self.missile1.add(self.missile1_ob)
        self.all_sprites_list.add(self.missile1_ob)
        
    def create_missile2(self, p2_pos):
        self.speed = Vector2(0, 0)
        self.pos = p2_pos
        self.missile2_ob = Missile(BLUE, 5, 5, self.speed, self.p2_pos)
        self.missile2.add(self.missile2_ob)
        self.all_sprites_list.add(self.missile2_ob)
    
    #creates asteroids object and adds it to its sprite group and the main sprite group for all the sprites
    def create_asteroids(self):
        self.speed = Vector2(1, 1)
        self.pos = (random.randint(0, 0), random.randint(100, 800))
        self.asteroids_ob = Asteroids(RED, 70, 70, self.speed, self.pos)
        self.asteroids.add(self.asteroids_ob)
        self.all_sprites_list.add(self.asteroids_ob)
    
    #creates first platform object and adds it to its sprite group and the main sprite group for all the sprites 
    def create_platform1(self):
        self.pos = (25, 1030)
        self.platform_ob1 = Platforms(GREY, 40, 50, self.speed, self.pos)
        self.platforms.add(self.platform_ob1)
        self.all_sprites_list.add(self.platform_ob1)
    
    #creates second platform object and adds it to its sprite group and the main sprite group for all the sprites
    def create_platform2(self):
        self.pos = (1845, 1030)
        self.platform_ob2 = Platforms(GREY, 40, 50, self.speed, self.pos)
        self.platforms.add(self.platform_ob2)
        self.all_sprites_list.add(self.platform_ob2)
    
    def collisions(self, player1_ob, player2_ob):
        #check for collision between screen and player1
        if player1_ob.rect.left > 1920: 
            player1_ob.rect.left = 1920
            self.speed *= -1
            SCOREP1 -= 1
        if player1_ob.rect.right < 0:
            player1_ob.rect.right = 0
            self.speed *= -1
            SCOREP1 -= 1
        if player1_ob.rect.top > 1080:
            player1_ob.rect.top = 1080
            self.speed *= -1
            SCOREP1 -= 1
        if player1_ob.rect.bottom > 1080:
            player1_ob.rect.bottom = 1080
            self.speed *= -1
            SCOREP1 -= 1
    
    #Checks for collisions between player 2 and the screen
        
        if player2_ob.rect.left > 1920: 
            player2_ob.rect.left = 1920
            self.speed *= -1
            SCOREP2 -= 1
        if player2_ob.rect.right < 0:
            player2_ob.rect.right = 0
            self.speed *= -1
            SCOREP2 -= 1
        if player2_ob.rect.top > 1080:
            player2_ob.rect.top = 1080
            self.speed *= -1
            SCOREP2 -= 1
        if player2_ob.rect.bottom > 1080:
            player2_ob.rect.bottom = 1080
            self.speed *= -1
            SCOREP2 -= 1    
    
    
    #checks for collisions between players. Destroys them if they collide
        if pygame.sprite.groupcollide(self.player1, self.player2, True, True):
            print("YOU BOTH LOSE! LOSERS!")
            
    #checks for collisions between player 1 and asteroids. Destroys player and reduces score by 1 if they collide
        if pygame.sprite.groupcollide(self.player1, self.asteroids, True, False):
            print("Player 1 down, player 2 has won.")
            SCOREP1 -= 1
            
    #checks for collisions between player 2 and asteroids. Destroys player and reduces score by 1 if they collide
        if pygame.sprite.groupcollide(self.player2, self.asteroids, True, False):
            print("Player 2 down, player 1 has won.")
            SCOREP2 -= 1
            
    #checks for collision between player 1 and platforms. Resets fuel if they collide
        if pygame.sprite.groupcollide(self.player1, self.platforms, False, False):
            print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            FUEL = 50
            
    #checks for collisions between player 2 and platforms. Resets fuel if they collide
        if pygame.sprite.groupcollide(self.player2, self.platforms, False, False):
            print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            FUEL = 50
            
    #checks for collisions between player 1 and player 2's missile. If they collide, player 1 loses a point and is destroyed
        if pygame.sprite.groupcollide(self.player1, self.missile2, True, True):
            SCOREP1 -= 1
            
    #checks for collisions between player 2 and player 1's missile. If they collide, player 2 loses a point and is destroyed        
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
    
    
    
    #text for displaying each player's score ingame
    def score_text(self):
        self.font = pygame.font.Font(None, 60)
        self.p1_score = self.font.render(str(SCOREP1), 1, WHITE)
        self.screen.blit(self.p1_score, (900,10))
        self.p2_score = self.font.render(str(SCOREP2), 1, WHITE)
        self.screen.blit(self.p2_score, (1420,10))
    
    #text for fuel count   
    def score_fuel(self):
        self.font = pygame.font.Font(None, 60)
        self.fuel_count = "Fuel: "
        self.p1_fuel = self.font.render(str(FUEL), 1, WHITE)
        self.screen.blit(self.p1_fuel, (700, 1040))
        self.p2_fuel = self.font.render(str(FUEL), 1, WHITE)
        self.screen.blit(self.p2_fuel, (1220, 1040))
    
    #text for displaying the winner of the game if they reach 50 points
    def winner_text(self):
        self.font = pygame.font.Font(None, 200)
        self.p1w = "Player 1 has won the game"
        self.p2w = "Player 2 has won the game"
        if SCOREP1 >= 50:
            self.p1_winner = self.font.render(str(self.p1w), 1, WHITE)
            self.screen.blit(self.p1_winner, (700,10))
        if SCOREP2 >= 50:
            self.p2_winner = self.font.render(str(self.p2w), 1, WHITE)
            self.screen.blit(self.p2_winner, (1220,10))
            
    #updates the surface, sprites and draws the sprites
    def update_game(self):
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        self.screen.blit(self.p1_score, (700,10))
        self.screen.blit(self.p2_score, (1220,10))
        self.screen.blit(self.p1_fuel, (700,1040))
        self.screen.blit(self.p2_fuel, (1220,1040))
        pygame.display.flip()
    
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
                    #if event.key == pygame.K_w:
                        #apply thrust on object
                        #Player.update(self)
                        #need to update pos of missile as well
                    if event.key == pygame.K_a:
                        #rotate object left
                        self.rot_img = pygame.transform.rotate(self.image, 20)
                        return self.rot_img
                    if event.key == pygame.K_d:
                        #rotate object right
                        self.rot_img = pygame.transform.rotate(self.image, -20)
                        return self.rot_img
                    if event.key == pygame.K_LSHIFT:
                        #fire weapon
                        self.create_missile2(self.p2_pos)
                        self.missile2.add(self.missile2_ob)
                        self.all_sprites_list.add(self.missile2_ob)
                        #self.rect.x += self.speed.x
                        #self.rect.y += self.speed.y
                    #if event.key == pygame.K_UP:
                        #apply thrust on object
                        #Player.update(self)
                        #need to update pos of missile as well
                    if event.key == pygame.K_LEFT:
                        #rotate object left
                        self.rot_img = pygame.transform.rotate(self.image, 20)
                        return self.rot_img
                    if event.key == pygame.K_RIGHT:
                        #rotate object right
                        self.rot_img = pygame.transform.rotate(self.image, -20)
                        return self.rot_img
                    if event.key == pygame.K_RSHIFT:
                        #fire weapon
                        self.create_missile1(self.p1_pos)
                        self.missile1.add(self.missile1_ob)
                        self.all_sprites_list.add(self.missile1_ob)
                        #self.rect.x += self.speed.x
                        #self.rect.y += self.speed.y
                elif event.type == pygame.KEYUP:
                    self.speed += GRAVITY
                    
                pygame.time.set_timer(fuel_loss, 1000)
                if pygame.event == fuel_loss:
                    FUEL - 5
                    if FUEL == 0:
                        pygame.sprite.Sprite.kill(self.player1_ob, self.player2_ob)
                        print("You have run out of fuel and are now floating aimlessly into space. Look for a tesla, maybe it has some fuel")


            #self.move()
            self.score_text()
            self.score_fuel()
            self.winner_text()
            self.collisions(self.player1_ob, self.player2_ob)
            self.update_game()
            
        pygame.quit()
        quit() 

#for initiating the game
if __name__ == '__main__':
    pygame.init()
    br = Game()
    br.game_loop()