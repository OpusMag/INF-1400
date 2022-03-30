from pygame import Vector2
import pygame
import random
from random import uniform
import math
from math import pi

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)

#this is the class that holds the draw method that the other classes inherits from
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, ob_pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    #method for drawing boids
    #def draw(self):
    
#Here all the code for moving the self.boids and hoiks goes. Other classes inherits from this
class Moving_objects(Drawable_objects):
    def __init__(self, color, width, height, speed, ob_pos):
        super().__init__(color, width, height, speed, ob_pos)
        self.b_pos = (random.randint(0, 1000), random.randint(0, 1000))
        self.h_pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        self.speed = Vector2(1, 1)
        #pygame.Surface.get_rect()
        #self.rect.x = self.b_pos[0] 
        #self.rect.y = self.b_pos[1]
        #self.rect.x += self.speed.x
        #self.rect.y += self.speed.y
        vector_x = uniform(-1, 1)
        vector_y = uniform(-1, 1)
        self.velocity = Vector2(vector_x, vector_y)
        self.velocity.normalize()
		#set a random magnitude
        self.velocity = self.velocity * uniform(1.5, 4)
        self.acceleration = Vector2()
        self.max_speed = 5
        self.max_length = 1
        self.size = 2
        self.stroke = 5
        self.angle = 0
        self.hue = 0
        self.toggles = {"separation":True, "alignment":True, "cohesion":True}
        self.values = {"separation":0.1, "alignment":0.1, "cohesion":0.1}
        self.radius = 40
    

class Boids(Moving_objects):
    def __init__(self, color, width, height, speed, ob_pos):
        super().__init__(color, width, height, speed, ob_pos)
        
    def collision_screen_b(self):
        #collision control: keep self.boids from flying off the screen (borrowed from previous hand in breakoutnovectorsorclasses.py)
        if self.b_pos[0] >= 1920 or self.b_pos[0] <= 0:
            self.b_speed[0] *= -1
        if self.b_pos[1] >= 1080 or self.b_pos[1] <= 0:
            self.b_speed[1] *= -1
            
    def collision_screen_h(self):
        #collision control: keep self.boids from flying off the screen (borrowed from previous hand in breakoutnovectorsorclasses.py)
        if self.h_pos[0] >= 1920 or self.h_rect[0] <= 0:
            self.h_speed[0] *= -1
        if self.h_pos[1] >= 1080 or self.h_pos[1] <= 0:
            self.h_speed[1] *= -1
            
    def collision_hoiks(self):
        if pygame.sprite.groupcollide(self.boids, self.hoiks, True, False):
            pass #legge til at størrelsen på hoiks skal øke når den "spiser" en boid
        
    def collision_skyscrapers(self):
        if pygame.sprite.groupcollide(self.boids, self.skyscrapers, True, False):
            pass
        
        #method for separation
        #separation: steer to avoid crowding local flockmates
        #see source [9] in the report bibliography for the code that inspired the code for my separation, cohesion, alignment and behaviour methods
    def separation(self):
        sum = 0
        steer = Vector2(0, 0)
        #single_boid = []
        #self.boids = []
        for single_boid in self.boids:
            distance = math.hypot(single_boid[0] - self.boids[0], single_boid[1] - self.boids[1])
            if single_boid is not self and distance < self.radius:
                temporary = math.hypot(single_boid[0] - self.boids[0], single_boid[1] - self.boids[1])
                temporary = temporary/(distance ** 2)
                steer.add(temporary)
                sum += 1

        if sum > 0:
            steer = steer / sum
            steer.normalize()
            steer = steer * self.max_speed
            steer = steer - self.speed
            steer.limit(self.max_length)
        
        return steer
        
        #metode for alignment
        #alignment: steer towards the average heading of local flockmates
    def alignment(self):
        sum = 0
        steer = Vector2(0, 0)
        for single_boid in self.boids:
            distance = math.hypot(single_boid[0] - self.boids[0], single_boid[1] - self.boids[1])
            if single_boid is not self and distance < self.radius:
                velocity = self.velocity.normalize()
                steer.add(velocity)
                self.color = (155, 155, 155)
                sum += 1


        if sum > 0:
            steer = steer / sum
            steer.normalize()
            steer = steer * self.max_speed
            steer = steer - self.velocity.normalize()
            steer.limit(self.max_length)
            return steer
        
        #metode for cohesion
        #cohesion: steer to move towards the average position (center of mass) of local flockmates
    def cohesion(self):
        sum = 0
        steer = Vector2()
        #single_boid = []
        #self.boids = []
        for single_boid in self.boids:
            distance = math.hypot(single_boid[0] - self.boids[0], single_boid[1] - self.boids[1])
            if single_boid is not self and distance < self.radius:
                steer.add(self.boids)
                sum += 1

        if sum > 0:
            steer = steer / sum
            steer = steer - self.b_pos
            steer.normalize()
            steer = steer * self.max_speed
            steer = steer - self.velocity
            steer.limit(self.max_length)

        return steer
        
        #metode for avoid
        #avoid: stop boids from colliding with skyscrapers
    def behaviour(self):
        self.speed.reset()

        if self.separation == True:
            avoid = self.separation(self.boids)
            avoid = avoid * self.separation
            self.velocity.add(avoid)

        if self.cohesion == True:
            cohesion = self.cohesion(self.boids)
            cohesion = cohesion * self.cohesion
            self.velocity.add(cohesion)

        if self.alignment == True:
            align = self.alignment(self.boids)
            align = align * self.alignment
            self.velocity.add(align)
    
    def update(self):
        self.b_pos = self.b_pos + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit(self.max_speed)
        self.angle = self.velocity.heading() + pi/2
        
    """def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y"""
    
    #move is inherited from Moving_objects
    #circles
    
class Hoiks(Moving_objects):
    def __init__(self, color, width, height, speed, ob_pos):
        super().__init__(color, width, height, speed, ob_pos)
        
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

    #move method is inherited from Moving_objects
    #draw method is inherited from Drawable_objects
    #triangles

class Skyscrapers(Moving_objects):
    def __init__(self, color, width, height, speed, ob_pos):
        super().__init__(color, width, height, speed, ob_pos)
        
    
    #draw method is inherited from Drawable_objects
    #rectangles
    
class Simulation_loop:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080), 0, 0)
        self.boids = pygame.sprite.Group()
        self.hoiks = pygame.sprite.Group()
        self.skyscrapers = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        
        #self.rect = pygame.Surface.get_rect(self)
    
    def create_boids(self):
        self.image = pygame.Surface((15, 15))
        self.image.fill(WHITE)
        self.b_rect = self.image.get_rect()
        self.b_speed = Vector2(1, 1)
        self.b_pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        boids_ob = Boids(WHITE, 15, 15, self.b_speed, self.b_pos)
        self.boids.add(boids_ob)
        self.all_sprites_list.add(boids_ob)
        
    def create_hoiks(self):
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.h_rect = self.image.get_rect()
        self.h_speed = Vector2(2, 8)
        self.h_pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        hoiks_ob = Hoiks(RED, 25, 25, self.h_speed, self.h_pos)
        self.hoiks.add(hoiks_ob)
        self.all_sprites_list.add(hoiks_ob)
    
    def create_skyscrapers(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.s_rect = self.image.get_rect()
        self.s_speed = Vector2(0, 0)
        self.s_pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        skyscraper_ob = Skyscrapers(GREY, 50, 50, self.s_speed, self.s_pos)
        self.skyscrapers.add(skyscraper_ob)
        self.all_sprites_list.add(skyscraper_ob)
    
    
        
    def setup(self):
        for h in range(50):
            self.create_boids()
        for i in range(5):
            self.create_hoiks()
        for j in range(5):
            self.create_skyscrapers()
        
    def run(self):
        self.setup()
        
    #def move(self):
        #self.collision_screen_b()
        #self.collision_screen_h()
        #self.collision_hoiks()
        #self.collision_skyscrapers()
        #self.separation()
        #self.alignment()
        #self.cohesion()
        #self.behaviour()
    
    def update_game(self):
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        
    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Boids')
        self.run()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            #self.move()
            self.update_game()
        pygame.quit()
        quit() 
        
    """Hva må lages? Enkleste først? Statiske objekter på skjermen som self.boidsene skal unngå. Nummer 2: lag predators som flyr på tvers av skjermen 
    for å prøve og spise self.boidsene. Kan bare gi dem en fart og en retning og når de kommer til enden av skjermen kan de snu eller dukke opp der de
    startet igjen. De statiske bbjektene kan være firkanter, predators kan være trekanter og self.boidsene kan være sirkler."""
if __name__ == '__main__':
    pygame.init()
    br = Simulation_loop()
    br.game_loop()