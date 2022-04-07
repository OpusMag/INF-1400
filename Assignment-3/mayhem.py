import pygame
from pygame import Vector2
import math
import config
from config import *
import random
import math
import sympy

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
        self.pos = pos
        self.speed = Vector2(0, 0)
        self.rect = self.pos
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        
        
class Player1(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(0, 0)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
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
        
    def update(self):
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.UP:
                self.rect.x += self.new_speed.x
                self.rect.y += self.new_speed.y"""
    
    def create_missile1(self):
        return Missile1(GREEN, 5, 5, self.speed, self.pos)
    
        
class Player2(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(0, 0)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = pos
        
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
    
    def update(self):
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.rect.x += self.new_speed.x
        self.rect.y += self.new_speed.y
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.UP:
                self.rect.x += self.new_speed.x
                self.rect.y += self.new_speed.y"""
    
    def create_missile2(self):
        return Missile2(BLUE, 5, 5, self.speed, self.pos)

class Missile1(Player1):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center = (self.pos))
        
    def update(self):
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.rect.x += self.new_speed.x + 1
        self.rect.x += self.new_speed.x + 1
        
class Missile2(Player1):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center = (self.pos))
        
    def update(self):
        self.acceleration = self.thrust + self.gravity
        self.new_speed = self.speed + self.acceleration * self.time
        self.rect.x += self.new_speed.x + 1
        self.rect.x += self.new_speed.x + 1
        
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
        self.pos = pos
    
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
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.pos = pos
        
        
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080), 0, 0)
        self.player1 = pygame.sprite.Group()
        self.player2 = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
    
    def create_player1(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = (30, 1000)
        self.player1_ob = Player1(GREEN, 30, 30, self.speed, self.pos)
        self.player1.add(self.player1_ob)
        self.all_sprites_list.add(self.player1_ob)
    
    def create_player2(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.gravity = Vector2(-2, -2)
        self.thrust = Vector2(1, 1)
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick(30) / 1000.0
        self.pos = (1850, 1000)
        self.player2_ob = Player2(BLUE, 30, 30, self.speed, self.pos)
        self.player2.add(self.player2_ob)
        self.all_sprites_list.add(self.player2_ob)
        
    """def create_missile1(self):
        self.image = pygame.Surface((5, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (30, 1000)
        self.missile1_ob = Missile1(GREEN, 5, 5, self.speed, self.pos)
        self.missiles.add(self.missile1_ob)
        self.all_sprites_list.add(self.missile1_ob)
        
    def create_missile2(self):
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (30, 1000)
        self.missile2_ob = Missile2(BLUE, 5, 5, self.speed, self.pos)
        self.missiles.add(self.missile2_ob)
        self.all_sprites_list.add(self.missile2_ob)"""
        
    def create_asteroids(self):
        self.image = pygame.Surface((70, 70))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (random.randint(0, 0), random.randint(100, 800))
        self.asteroids_ob = Asteroids(RED, 70, 70, self.speed, self.pos)
        self.asteroids.add(self.asteroids_ob)
        self.all_sprites_list.add(self.asteroids_ob)
        
    def create_platform1(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = (25, 1030)
        self.platform_ob1 = Platforms(GREY, 40, 50, self.speed, self.pos)
        self.platforms.add(self.platform_ob1)
        self.all_sprites_list.add(self.platform_ob1)
    
    def create_platform2(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = (1845, 1030)
        self.platform_ob2 = Platforms(GREY, 40, 50, self.speed, self.pos)
        self.platforms.add(self.platform_ob2)
        self.all_sprites_list.add(self.platform_ob2)
    
    def collision_players(self):
        if pygame.sprite.groupcollide(self.player1, self.player2, True, True):
            print("YOU BOTH LOSE! LOSERS!")
            self.player1.kill()
            self.player2.kill()
    def collision_p1asteroids(self):
        if pygame.sprite.groupcollide(self.player1, self.asteroids, True, False):
            print("Player 1 down, player 2 has won.")
            SCOREP1 -= 1
            self.player1.kill()
    def collision_p2asteroids(self):
        if pygame.sprite.groupcollide(self.player2, self.asteroids, True, False):
            print("Player 2 down, player 1 has won.")
            SCOREP2 -= 1
            self.player2.kill()
    def collision_p1platforms(self):
        if pygame.sprite.groupcollide(self.player1, self.platforms, False, False):
            print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            FUEL = 50
    def collision_p2platforms(self):
        if pygame.sprite.groupcollide(self.player2, self.platforms, False, False):
            print("You're all fueled up") #refill fuel, maybe reset the event loop timer somehow?
            FUEL = 50
    
    def collision_missile1(self):
        if pygame.sprite.groupcollide(self.player1, self.missiles, True, True):
            SCOREP1 -= 1
            
    def collision_missile2(self):
        if pygame.sprite.groupcollide(self.player2, self.missiles, True, True):
            SCOREP2 -= 1
            
    def setup(self):
        
        self.create_player1()
        self.create_player2()
        #self.create_missile1()
        #self.create_missile2()
        for i in range(3):
            self.create_asteroids()
        self.create_platform1()
        self.create_platform2()
        
    def update_game(self):
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
    
    def score_text(self):
        font = pygame.font.Font(None, 60)
        p1_score = font.render(str(SCOREP1), 1, WHITE)
        self.screen.blit(p1_score, (700,10))
        p2_score = font.render(str(SCOREP2), 1, WHITE)
        self.screen.blit(p2_score, (1220,10))
        
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
                        Player1.update(self)
                    if event.key == pygame.K_a:
                        #rotate object left
                        pygame.transform.rotate(Player1.image, 20)
                    if event.key == pygame.K_d:
                        #rotate object right
                        pygame.transform.rotate(Player1.image, -20)
                    if event.key == pygame.K_LSHIFT:
                        #fire weapon
                        self.missiles.add(Player2.create_missile2(self))
                        self.all_sprites_list.add(Player2.create_missile2(self))
                    if event.key == pygame.K_UP:
                        #apply thrust on object
                        Player2.update(self)
                    if event.key == pygame.K_LEFT:
                        #rotate object left
                        pygame.transform.rotate(Player2.rect, 20)
                    if event.key == pygame.K_RIGHT:
                        #rotate object right
                        pygame.transform.rotate(Player2.rect, -20)
                    if event.key == pygame.K_RSHIFT:
                        #fire weapon
                        self.missiles.add(Player1.create_missile1(self))
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

if __name__ == '__main__':
    pygame.init()
    br = Game()
    br.game_loop()