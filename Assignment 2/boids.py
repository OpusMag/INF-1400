from email.mime import image
import numpy
from pygame import Vector2
import pygame
import random
from random import uniform
import math
from math import pi
import sympy
from sympy import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#this is the class that holds the draw method that the other classes inherits from
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    #method for drawing boids
    #def draw(self):
    
#Here all the code for moving the self.boids and hoiks goes. Other classes inherits from this
class Moving_objects(Drawable_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.pos = Vector2(random.randint(0, 1000), random.randint(0, 1000))
        self.speed = Vector2(1, 3)
        #pygame.Surface.get_rect()
        #de neste fire linjene fixed startposisjonen til skyscrapers og hoiks, men bare boids beveger seg? why?
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
		#set a random magnitude
        self.perception = 50
        vector = (numpy.random.rand(2) - 0.5)/2
        self.acceleration = Vector2(*vector) 
        self.velocity = Vector2(*vector)
        self.velocity.normalize()
        self.max_speed = 4
        self.max_power = 5
        self.max_length = 1
        self.size = 2
        self.stroke = 5
        self.angle = 0
        self.radius = 40
    
    def screen_wrap(self):
        #collision control: keep self.boids from flying off the screen (borrowed from previous hand in breakoutnovectorsorclasses.py)
        if self.rect.left > 1920: 
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = 1920
        if self.rect.top > 1080:
            self.rect.bottom = 0
        if self.rect.bottom > 1080:
            self.rect.top = 0
    
class Boids(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        #self.rect.x = self.pos[0] 
        #self.rect.y = self.pos[1]
        #self.boids = pygame.sprite.Group()
        #self.hoiks = pygame.sprite.Group()
        #self.skyscrapers = pygame.sprite.Group()
        #self.perception = 50
        vector = (numpy.random.rand(2) - 0.5)/2
        #self.acceleration = Vector2(*vector) 
        #self.velocity = Vector2(*vector)
        #self.velocity.normalize()
        #self.max_speed = 4
        #self.max_power = 5
        #self.max_length = 1
        #self.size = 2
        #self.stroke = 5
        #self.angle = 0
        #self.radius = 40
        #self.flock = []
        
    #def flock(self):
        #for i in range(50):
            #self.flock.append(Boids(random.randint(15, 1920-15), random.randint(15, 1080-15)))
        
        #method for separation
        #separation: steer to avoid crowding local flockmates
        #see source [9] in the report bibliography for the code that inspired the code for my separation, cohesion, alignment and behaviour methods
    
    #metode for alignment
        #alignment: steer towards the average heading of local flockmates
    def alignment(self, boids):
        steering = Vector2(*numpy.zeros(2))
        total = 0
        avg_vector= Vector2(*numpy.zeros(2))
        for boids_ob in boids:
            if numpy.linalg.norm(boids_ob.rect.center - self.rect.center) < self.perception:
                avg_vector += self.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector2(*avg_vector)
            avg_vector = (avg_vector/numpy.linalg.norm(avg_vector)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering
    
    #metode for cohesion
        #cohesion: steer to move towards the average position (center of mass) of local flockmates
    def cohesion(self, boids):
        steering = Vector2(*numpy.zeros(2))
        total = 0
        mass_center = Vector2(*numpy.zeros(2))
        for boids_ob in boids:
            if numpy.linalg.norm(boids_ob.rect.center - self.rect.center) < self.perception:
                mass_center += boids_ob.rect.center
                total += 1
        if total > 0:
            mass_center /= total
            mass_center = Vector2(*mass_center)
            cm_vector = mass_center - self.rect.center
            if numpy.linalg.norm(cm_vector) > 0:
                cm_vector = (cm_vector / numpy.linalg.norm(cm_vector)) * self.max_speed
            steering = cm_vector - self.velocity
            if numpy.linalg.norm(steering)> self.max_power:
                steering = (steering /numpy.linalg.norm(steering)) * self.max_power

        return steering
    
    def separation(self, boids):
        steering = Vector2(*numpy.zeros(2))
        total = 0
        avg_vector = Vector2(*numpy.zeros(2))
        for boids_ob in boids:
            distance = numpy.linalg.norm(boids_ob.rect.center - self.rect.center)
            if self.rect.center != boids_ob.rect.center and distance < self.perception:
                diff = self.rect.center - boids_ob.rect.center
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector2(*avg_vector)
            if numpy.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / numpy.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if numpy.linalg.norm(steering) > self.max_power:
                steering = (steering /numpy.linalg.norm(steering)) * self.max_power

        return steering
        
        
        #metode for avoid
        #avoid: stop boids from colliding with skyscrapers
    def behaviour(self):
        
        alignment = self.alignment(self.boids)
        cohesion = self.cohesion(self.boids)
        separation = self.separation(self.boids)

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation
    
    def update(self):
        #kan ikke bruke pos når du bruker vectorer, må bruker rect, så endre pos fra pos i alt som har med bevegelse å gjøre?
        #boid_screen_wrap()
        #self.rect.x += self.speed.x
        #self.rect.y += self.speed.y
        self.screen_wrap()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.velocity += self.acceleration
        #numpy.clip(self.velocity, 3, 3)
        if numpy.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / numpy.linalg.norm(self.velocity) * self.max_speed
        #self.angle = self.velocity.heading() + pi/2   
    
    """def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y"""
    
    #move is inherited from Moving_objects
    #circles
    
class Hoiks(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] 
        self.rect.y = self.pos[1]
        self.speed = Vector2(1, 1)
        self.hoiks = pygame.sprite.Group()
    
    """def hoik_screen_wrap(self):
        #screen wrap. Makes it so that when objects move out of the screen they reappear on the opposite side. Works but has a super long delay?
        if self.h_rect.left >= 1920: 
            self.h_rect.right = 0
        if self.h_rect.right <= 0:
            self.h_rect.left = 1920
        if self.h_rect.top > 1080:
            self.h_rect.bottom = 0
        if self.h_rect.bottom > 1080:
            self.h_rect.top = 0"""
    
    def update(self):
        self.screen_wrap()
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

    #move method is inherited from Moving_objects
    #draw method is inherited from Drawable_objects
    #triangles

class Skyscrapers(Moving_objects):
    def __init__(self, color, width, height, speed, pos):
        super().__init__(color, width, height, speed, pos)
        self.skyscrapers = pygame.sprite.Group()
    
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
        self.rect = self.image.get_rect()
        self.speed = Vector2(1, 1)
        self.pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        boids_ob = Boids(WHITE, 15, 15, self.speed, self.pos)
        self.boids.add(boids_ob)
        self.all_sprites_list.add(boids_ob)
        
    def create_hoiks(self):
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = Vector2(1, 3)
        self.pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        hoiks_ob = Hoiks(RED, 25, 25, self.speed, self.pos)
        self.hoiks.add(hoiks_ob)
        self.all_sprites_list.add(hoiks_ob)
    
    def create_skyscrapers(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = Vector2(0, 0)
        self.pos = (random.randint(0, 1000), random.randint(0, 1000)) 
        skyscraper_ob = Skyscrapers(GREEN, 50, 50, self.speed, self.pos)
        self.skyscrapers.add(skyscraper_ob)
        self.all_sprites_list.add(skyscraper_ob)
    
    def collision_hoiks(self):
        if pygame.sprite.groupcollide(self.boids, self.hoiks, True, False):
            self.image = pygame.transform.scale(self.image, (26, 26)) #legge til at størrelsen på hoiks skal øke når den "spiser" en boid
        
    def collision_skyscrapers(self):
        if pygame.sprite.groupcollide(self.boids, self.skyscrapers, True, False):
            print("a bird in the hand is better than two in the building")
        
    def setup(self):
        for h in range(100):
            self.create_boids()
        for i in range(3):
            self.create_hoiks()
        for j in range(4):
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
        self.collision_hoiks()
        self.collision_skyscrapers()
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