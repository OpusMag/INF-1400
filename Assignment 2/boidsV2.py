from pygame import Vector2
import pygame
import random
import math

#this is the class that holds the draw method that the other classes inherits from
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = (800, 600)
        #self.all_sprite_list = pygame.sprite.Group()
        #self.all_sprites_list.add(self.boids_ob, self.hoiks_ob, self.skyscraper_ob)
        self.max_speed = 5
        self.max_length = 1
        self.angle = 0
        self.boids_col = (255, 255, 255)
        self.hoiks_col = (255, 0, 0)
        self.skyscraper_col = (192, 192, 192)
    
    #method for drawing boids
    def draw(self):
        self.boids_pos = Vector2(0, 0)
        self.boids_size_x = 10
        self.boids_size_y = 10
        self.boids_speed = Vector2(10, 10)
        self.boids_rect = pygame.Rect(self.boids_pos[0], self.boids_pos[1], self.boids_size_x, self.boids_size_y)
        self.hoiks_pos = Vector2(10, 10)
        self.hoiks_size_x = self.hoiks_radius * 2
        self.hoiks_size_y = self.hoiks_radius * 2
        self.hoiks_radius = 10
        self.hoiks_speed = Vector2(1, 1)
        self.hoiks_rect = pygame.Rect(self.hoiks_pos[0], self.hoiks_pos[1], self.hoiks_size_x, self.hoiks_size_y)
        self.skyscraper_pos = Vector2(20, 20)
        self.skyscraper_size_x = 40
        self.skyscraper_size_y = 40
        self.skyscraper_rect = pygame.Rect(self.skyscraper_pos[0], self.skyscraper_pos[1], self.skyscraper_size_x, self.skyscraper_size_y)
    
    
#Here all the code for moving the self.boids and hoiks goes. Other classes inherits from this
class Moving_objects(Drawable_objects):
    def __init__(self):
        super().__init__()
        self.boids_pos = Vector2(1, 1)
        self.boids_size_x = 10
        self.boids_size_y = 10
        self.boids_speed = Vector2(10, 10)
        self.boids_rect = pygame.Rect(self.boids_pos.x, self.boids_pos.y, self.boids_size_x, self.boids_size_y)
        self.hoiks_pos = Vector2(10, 10)
        self.hoiks_radius = 10
        self.hoiks_size_x = self.hoiks_radius * 2
        self.hoiks_size_y = self.hoiks_radius * 2
        self.hoiks_speed = Vector2(1, 1)
        self.hoiks_rect = pygame.Rect(self.hoiks_pos.x, self.hoiks_pos.y, self.hoiks_size_x, self.hoiks_size_y)
        self.skyscraper_pos = Vector2(20, 20)
        self.skyscraper_size_x = 40
        self.skyscraper_size_y = 40
        self.skyscraper_rect = pygame.Rect(self.skyscraper_pos.x, self.skyscraper_pos.y, self.skyscraper_size_x, self.skyscraper_size_y)
        self.boids_rect.x += self.boids_speed.x
        self.boids_rect.y += self.boids_speed.y
        self.hoiks_rect.x += self.hoiks_speed.y
        self.hoiks_rect.x += self.hoiks_speed.y


class Boids(Moving_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #make self.boids
        
        
    def collision_screen(self):
        #collision control: keep self.boids from flying off the screen (borrowed from previous hand in breakoutnovectorsorclasses.py)
        if self.boids_rect.right >= self.screen_x or self.boids_rect.left <= 0:
            self.boids_speed_x *= -1
        if self.boids_rect.bottom >= self.screen_y:
            self.boids_speed_x *= -1
        if self.boids_rect.top <= 0:
            self.boids_speed_y *= -1
    
    def collision_hoiks(self):
        #collision control between hoiks and boids (taken and modified from breakoutnovectorsorclasses.py handed in for last work requirement)
        #boid count is reduced by one if a hoik hits a boid to simulate the hoik "eating" the boid
        #collision detection between ball and paddle
        collision_tolerance = 5
        if pygame.Rect.colliderect(self.hoiks_rect, self.boids_rect):
            if abs(self.hoiks_rect.bottom - self.boids_rect.top) < collision_tolerance:
                self.boid_count = self.boid_count - 1
            if abs(self.hoiks_rect.top - self.boids_rect.bottom) < collision_tolerance:
                self.boid_count = self.boid_count - 1
            if abs(self.hoiks_rect.left - self.boids_rect.right) < collision_tolerance:
                self.boid_count = self.boid_count - 1
            if abs(self.hoiks_rect.right - self.boids_rect.left) < collision_tolerance:
                self.boid_count = self.boid_count - 1
        
        #method for separation
        #separation: steer to avoid crowding local flockmates
        #see source [9] in the report bibliography for the code that inspired the code for my separation, cohesion, alignment and behaviour methods
    def separation(self):
        sum = 0
        steer = Vector2()

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
        steer = Vector2()
        for single_boid in self.boids:
            distance = math.hypot(single_boid[0] - self.boids[0], single_boid[1] - self.boids[1])
            if single_boid is not self and distance < self.radius:
                speed = self.boid.speed.Normalize()
                steer.add(speed)
                self.boid.color = (255, 255, 255)
                sum += 1


        if sum > 0:
            steer = steer / sum
            steer.normalize()
            steer = steer * self.max_speed
            steer = steer - self.speed.Normalize()
            steer.limit(self.max_length)
            return steer
        
        #metode for cohesion
        #cohesion: steer to move towards the average position (center of mass) of local flockmates
    def cohesion(self):
        sum = 0
        steer = Vector2()

        for single_boid in self.boids:
            distance = math.hypot(single_boid[0] - self.boids[0], single_boid[1] - self.boids[1])
            if single_boid is not self and distance < self.radius:
                steer.add(self.boid)
                sum += 1

        if sum > 0:
            steer = steer / sum
            steer = steer - self.position
            steer.normalize()
            steer = steer * self.max_speed
            steer = steer - self.speed
            steer.limit(self.max_length)

        return steer
        
        #metode for avoid
        #avoid: stop boids from colliding with skyscrapers
    def behaviour(self):
        self.acceleration.reset()

        if self.separation == True:
            avoid = self.separation(self.boids)
            avoid = avoid * self.separation
            self.acceleration.add(avoid)

        if self.cohesion == True:
            cohesion = self.cohesion(self.boids)
            cohesion = cohesion * self.cohesion
            self.acceleration.add(cohesion)

        if self.alignment == True:
            align = self.alignment(self.boids)
            align = align * self.alignment
            self.acceleration.add(align)
    #move is inherited from Moving_objects
    #circles
    
class Hoiks(Moving_objects, pygame.sprite.Sprite):
    def __init__(self, screen, hoiks_rect, hoiks_speed_x, hoiks_speed_y):
        super().__init__(self, screen, hoiks_rect, hoiks_speed_x, hoiks_speed_y)
        #collision control hoiks: keep hoiks from flying off the screen (borrowed from previous hand in breakoutnovectorsorclasses.py)
        if self.hoiks_rect.right >= self.screen_x or self.hoiks_rect.left <= 0:
            self.hoiks_speed_x *= -1
        if self.hoiks_rect.bottom >= self.screen_y:
            self.hoiks_speed_x *= -1
        if self.hoiks_rect.top <= 0:
            self.hoiks_speed_y *= -1
        
    #move method is inherited from Moving_objects
    #draw method is inherited from Drawable_objects
    #triangles

class Skyscrapers(Moving_objects, pygame.sprite.Sprite):
    def __init__(self, skyscraper_rect):
        super().__init__(self, skyscraper_rect)
        self.skyscraper_rect = pygame.Rect(self.skyscraper_pos.x, self.skyscraper_pos.y, self.skyscraper_size_x, self.skyscraper_size_y)
    #draw method is inherited from Drawable_objects
    #rectangles
    
class Simulation_loop(Moving_objects):
    
    
    def create_boids(self):
        boids_ob = Simulation_loop()
        boids_ob.create_boids()
        self.boids_pos = Vector2(0, 0)
        self.boids_size_x = 10
        self.boids_size_y = 10
        self.boids_speed = Vector2(10, 10)
        self.boids_rect = pygame.Rect(self.boids_pos.x, self.boids_pos.y, self.boids_size_x, self.boids_size_y)
        boids_ob = Boids()
        self.boids = []
        self.single_boid = []
        self.boid_count = 0
        for h in range (50):
            self.boids_ob.rect.x = self.boids_rect.x
            self.boids_ob.rect.y = self.boids_rect.y
            self.all_sprites_list.add(self.boids_ob)
        self.boids.append(self.single_boid)
        self.boid_count += 1
        
    def create_hoiks(self):
        hoiks_ob = Simulation_loop()
        hoiks_ob.create_hoiks()
        self.hoiks_pos = Vector2(10, 10)
        self.hoiks_radius = 10
        self.hoiks_size_x = self.hoiks_radius * 2
        self.hoiks_size_y = self.hoiks_radius * 2
        self.hoiks_speed = Vector2(1, 1)
        self.hoiks_rect = pygame.Rect(self.hoiks_pos.x, self.hoiks_pos.y, self.hoiks_size_x, self.hoiks_size_y)
        hoiks_ob = Hoiks()
        self.hoiks = []
        self.single_hoik = []
        self.hoik_count = 0
        for i in range (5):
            self.hoiks_ob.rect.x = self.hoiks_rect.x
            self.hoiks_ob.rect.y = self.hoiks_rect.y
            self.all_sprites_list.add(self.hoiks_ob)
        self.hoiks.append(self.single_hoik)
        self.hoik_count += 1
    
    def create_skyscraper(self):
        skyscraper_ob = Simulation_loop()
        skyscraper_ob.create_skyscraper()
        self.skyscraper_pos = Vector2(20, 20)
        self.skyscraper_size_x = 40
        self.skyscraper_size_y = 40
        self.skyscraper_rect = pygame.Rect(self.skyscraper_pos.x, self.skyscraper_pos.y, self.skyscraper_size_x, self.skyscraper_size_y)
        skyscraper_ob = Skyscrapers()
        self.skyscraper = []
        self.single_skyscraper = []
        for j in range (5):
            self.skyscraper_ob.rect.x = self.skyscraper_rect.x
            self.skyscraper_ob.rect.y = self.skyscraper_rect.y
            self.all_sprites_list.add(self.skyscraper_ob)
        self.skyscraper.append(self.single_skyscraper)


    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('Boids')
        clock = pygame.time.Clock()
        time_passed = clock.tick(30) / 1000.0
        all_sprites_list = pygame.sprite.Group()
        #all_sprites_list.add(self.boids_ob, self.hoiks_ob, self.skyscraper_ob)
        boids_ob = Simulation_loop()
        boids_ob.create_boids()
        hoiks_ob = Simulation_loop()
        hoiks_ob.create_hoiks()
        skyscraper_ob = Simulation_loop()
        skyscraper_ob.create_skyscraper()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                    pygame.display.flip()
            
            #self.boids_ob.Moving_Objects()
            #self.hoiks_ob.Moving_Objects()
            #self.skyscraper_ob.Moving_Objects()
            pygame.display.update()
            all_sprites_list.draw(screen)
            for i in range (50):
                pygame.draw.polygon(screen, (self.boids_col), ([[50, 50], [25, 50], [50, 100]]))
            for j in range (5):
                pygame.draw.circle(screen, (self.hoiks_col), (self.hoiks_rect.x, self.hoiks_rect.y), self.hoiks_radius)
            for j in range (5):
                pygame.draw.rect(screen, (self.skyscraper_col), self.skyscraper_rect)
            clock.tick(60)
        pygame.quit()
        quit() 
        
    """Hva må lages? Enkleste først? Statiske objekter på skjermen som self.boidsene skal unngå. Nummer 2: lag predators som flyr på tvers av skjermen 
    for å prøve og spise self.boidsene. Kan bare gi dem en fart og en retning og når de kommer til enden av skjermen kan de snu eller dukke opp der de
    startet igjen. De statiske bbjektene kan være firkanter, predators kan være trekanter og self.boidsene kan være sirkler."""
if __name__ == '__main__':
    br = Simulation_loop()
    br.game_loop()