import pygame
from pygame import Vector2
import math
import config
from config import *
import random
import math
import sympy

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)
WIDTH = 1920
HEIGHT = 1080
Screen_size = WIDTH, HEIGHT

class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
    
class Moving_objects(Drawable_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.pos = Vector2(0, 0)
        self.speed = Vector2(0, 0)
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 500.0
        
    def player_movement(self):
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        
        
class Player1(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(2, 3)
        self.pos = (30, 1010)
    
    """def collision_screen(self, player1_ob):
        #make asteroids wrap around to the opposite side of the screen when they leave it (borrowed from previous hand in boids.py)
        if self.rect.left > 1920: 
            pygame.kill(player1_ob)
        if self.rect.right < 0:
            pygame.kill(player1_ob)
        if self.rect.top > 1080:
            pygame.kill(player1_ob)
        if self.rect.bottom > 1080:
            pygame.kill(player1_ob)"""
        
    def update(self):
        self.player_movement()
        
    """def update(self):
        pygame.key.get_pressed(pygame.K_w)
            #apply thrust on object
        pygame.key.get_pressed(pygame.K_a)
            #rotate object left
        pygame.key.get_pressed(pygame.K_d)
            #rotate object right
        pygame.key.get_pressed(pygame.K_LSHIFT)
            #fire weapon"""
        
class Player2(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(2, 2)
        self.pos = (1850, 1010)
        
    """def collision_screen(self, player2_ob):
        #make asteroids wrap around to the opposite side of the screen when they leave it (borrowed from previous hand in boids.py)
        if self.rect.left > 1920: 
            pygame.kill(player2_ob)
        if self.rect.right < 0:
            pygame.kill(player2_ob)
        if self.rect.top > 1080:
            pygame.kill(player2_ob)
        if self.rect.bottom > 1080:
            pygame.kill(player2_ob)"""
    
    def update(self):
        self.player_movement()
        
    """def update(self):
        pygame.key.get_pressed(pygame.K_UP)
            #apply thrust on object
        pygame.key.get_pressed(pygame.K_LEFT)
            #rotate object left
        pygame.key.get_pressed(pygame.K_RIGHT)
            #rotate object right
        pygame.key.get_pressed(pygame.K_RSHIFT)
            #fire weapon"""
        
class Asteroids(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((70, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed.x = 1
        self.speed.y = 0
        self.pos1 = (0, 300)
        self.pos2 = (0, 600)
        self.pos3 = (0, 900)
    
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
    
    def update(self):
        self.screen_wrap()
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        
class Platforms(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((40, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos1 = (1870, 1030)
        self.pos2 = (50, 1030)
        
        
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080), 0, 0)
        self.player1 = pygame.sprite.Group()
        self.player2 = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
    
    def create_player1(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (30, 1010)
        self.player1_ob = Player1(GREEN, 30, 30, self.speed, self.pos)
        self.player1.add(self.player1_ob)
        self.all_sprites_list.add(self.player1_ob)
        
    def create_player2(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (1850, 1010)
        self.player2_ob = Player2(BLUE, 30, 30, self.speed, self.pos)
        self.player2.add(self.player2_ob)
        self.all_sprites_list.add(self.player2_ob)
        
    def create_asteroids(self):
        self.image = pygame.Surface((70, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos1 = (0, 300)
        self.pos2 = (0, 600)
        self.pos3 = (0, 900)
        self.asteroids_ob1 = Asteroids(RED, 70, 70, self.speed, self.pos1)
        self.asteroids_ob2 = Asteroids(RED, 70, 70, self.speed, self.pos2)
        self.asteroids_ob3 = Asteroids(RED, 70, 70, self.speed, self.pos3)
        self.asteroids.add(self.asteroids_ob1, self.asteroids_ob2, self.asteroids_ob3)
        self.all_sprites_list.add(self.asteroids_ob1, self.asteroids_ob2, self.asteroids_ob3)
        
    def create_platforms(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos1 = (1870, 1030)
        self.pos2 = (50, 1030)
        self.platform_ob1 = Platforms(GREY, 40, 50, self.speed, self.pos1)
        self.platform_ob2 = Platforms(GREY, 40, 50, self.speed, self.pos2)
        self.platforms.add(self.platform_ob1, self.platform_ob2)
        self.all_sprites_list.add(self.platform_ob1, self.platform_ob2)
    
    def collision_players(self):
        if pygame.sprite.groupcollide(self.player1, self.player2, True, True):
            print("YOU BOTH LOSE! LOSERS!") 
        
    def collision_p1asteroids(self):
        if pygame.sprite.groupcollide(self.player1, self.asteroids, True, False):
            print("Player 1 down, player 2 has won.")
    
    def collision_p2asteroids(self):
        if pygame.sprite.groupcollide(self.player2, self.asteroids, True, False):
            print("Player 2 down, player 1 has won.")
            
    def collision_p1platforms(self):
        if pygame.sprite.groupcollide(self.player1, self.platforms, False, False):
            print("You're all fueled up") #refill fuel
            
    def collision_p2platforms(self):
        if pygame.sprite.groupcollide(self.player2, self.platforms, False, False):
            print("You're all fueled up") #refill fuel 
    
    def setup(self):
        
        self.create_player1()
        self.create_player2()
        self.create_asteroids()
        self.create_platforms()
        
    def update_game(self):
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        
    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Mayhem')
        self.setup()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                """if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed(pygame.K_w):
                        #apply thrust on object
                    if pygame.key.get_pressed(pygame.K_a):
                        #rotate object left
                        pygame.transform.rotate(20)
                    if pygame.key.get_pressed(pygame.K_d):
                        #rotate object right
                        pygame.transform.rotate(-20)
                    if pygame.key.get_pressed(pygame.K_LSHIFT):
                        #fire weapon
                    if pygame.key.get_pressed(pygame.K_UP):
                        #apply thrust on object
                    if pygame.key.get_pressed(pygame.K_LEFT):
                        #rotate object left
                        pygame.transform.rotate(20)
                    if pygame.key.get_pressed(pygame.K_RIGHT):
                        #rotate object right
                        pygame.transform.rotate(-20)
                    if pygame.key.get_pressed(pygame.K_RSHIFT):
                        #fire weapon"""
            #self.move()
            self.update_game()
        pygame.quit()
        quit() 

if __name__ == '__main__':
    pygame.init()
    br = Game()
    br.game_loop()