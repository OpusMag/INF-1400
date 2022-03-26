from pygame import Vector2
import pygame
import random
import math

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)

#this is the class that holds the draw method that the other classes inherits from
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, color, width, height, start_pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=start_pos)
        
        
    
    #method for drawing boids
    #def draw(self):
    
#Here all the code for moving the self.boids and hoiks goes. Other classes inherits from this
class Moving_objects(Drawable_objects):
    def __init__(self, color, width, height, speed):
        super().__init__(color, width, height, speed)
        self.max_speed = 5
        self.max_length = 1
        self.angle = 0
        
        self.speed = Vector2(10, 10)
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        
    def collision_screen(self):
        #collision control: keep self.boids from flying off the screen (borrowed from previous hand in breakoutnovectorsorclasses.py)
        if self.rect.right >= self.screen.x or self.rect.left <= 0:
            self.speed.x *= -1
        if self.rect.bottom >= self.screen.y:
            self.speed.x *= -1
        if self.rect.top <= 0:
            self.speed.y *= -1

class Boids(Moving_objects):
    def __init__(self, color, width, height, speed):
        super().__init__(color, width, height, speed)
        
    def make_location(self):
        self.boids_pos = Vector2((random.randint(0, 800)), (random.randint(0, 800)))
        
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
         
    def collision_hoiks(self):
        if pygame.sprite.spritecollide(self.boids, self.hoiks, True):
            self.boids.remove(self.boids)
        
    def collision_skyscrapers(self):
        if pygame.sprite.spritecollide(self.boids, self.skyscrapers, True):
            self.boids.remove(self.boids)
        
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
                speed = self.speed.Normalize()
                steer.add(speed)
                self.color = (255, 255, 255)
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
                steer.add(self.boids)
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
    def __init__(self, color, width, height, speed):
        super().__init__(color, width, height, speed)
        
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
    
    def make_location(self):
        self.hoiks_pos = Vector2((random.randint(0, 600)), (random.randint(0, 600)))    
    
    #move method is inherited from Moving_objects
    #draw method is inherited from Drawable_objects
    #triangles

class Skyscrapers(Moving_objects):
    def __init__(self, color, width, height, speed):
        super().__init__(color, width, height, speed)
        
    def make_location(self):
        self.skyscrapers_pos = Vector2((random.randint(0, 600)), (random.randint(0, 600)))
    #draw method is inherited from Drawable_objects
    #rectangles
    
class Simulation_loop(Moving_objects):
    def __init__(self):
        self.boids = pygame.sprite.Group()
        self.hoiks = pygame.sprite.Group()
        self.skyscrapers = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.screen = pygame.display.set_mode()
    
    def create_boids(self):
        self.boids_pos = Vector2(0, 0)
        boids_ob = Boids(WHITE, 10, 10, self.boids_pos)
        for h in range (50):
            boids_ob = Drawable_objects(WHITE, 10, 10, self.boids_pos)
            self.boids.add(boids_ob)
            self.all_sprites_list.add(boids_ob)
        #self.boids.append(self.single_boid)
        
    def create_hoiks(self):
        self.hoiks_pos = Vector2(10, 10)
        hoiks_ob = Hoiks(RED, 15, 15, self.hoiks_pos)
        for i in range (5):
            hoiks_ob = Drawable_objects(RED, 15, 15, self.hoiks_pos)
            self.hoiks.add(hoiks_ob)
            self.all_sprites_list.add(hoiks_ob)
    
    def create_skyscrapers(self):
        self.skyscraper_pos = Vector2(20, 20)
        skyscraper_ob = Skyscrapers(GREY, 20, 20, self.skyscraper_pos)
        for j in range (5):
            self.skyscraper_ob = Drawable_objects(GREY, 20, 20, self.skyscraper_pos)
            self.skyscrapers.add(skyscraper_ob)
            self.all_sprites_list.add(skyscraper_ob)

    def setup(self):
        self.create_boids()
        self.create_hoiks()
        self.create_skyscrapers()
        self.all_sprites_list()
        
    def run(self):
        self.setup()
        self.game_loop()
    
    def update_game(self):
        #Oppdaterer og tegner
        self.screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        
    def game_loop(self):
        pygame.init()
        pygame.display.set_caption('Boids')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                    pygame.display.flip()
            self.run()
        pygame.quit()
        quit() 
        
    """Hva må lages? Enkleste først? Statiske objekter på skjermen som self.boidsene skal unngå. Nummer 2: lag predators som flyr på tvers av skjermen 
    for å prøve og spise self.boidsene. Kan bare gi dem en fart og en retning og når de kommer til enden av skjermen kan de snu eller dukke opp der de
    startet igjen. De statiske bbjektene kan være firkanter, predators kan være trekanter og self.boidsene kan være sirkler."""
if __name__ == '__main__':
    pygame.init()
    br = Simulation_loop()
    br.game_loop()