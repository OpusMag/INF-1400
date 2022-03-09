from pygame import Vector2
import pygame
import random

class Game_loop:

    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('Boids')
        clock = pygame.time.Clock()
        time_passed = clock.tick(30) / 1000.0

        all_sprites_list = pygame.sprite.Group()
        self.boids_ob = Drawable_objects(screen, (255, 255, 255), (random.randint(0, 800), random.randint(0, 800), random.randint(0, 800)) )
        self.hoiks_ob = Drawable_objects(screen, (255, 0, 0),(random.randint(0, 800), random.randint(0, 800)), 10, 0)
        self.skyscraper_ob = Drawable_objects(screen, (192, 192, 192),(random.randint(0, 800), random.randint(0, 800)), 50)
        all_sprites_list.add(self.boids_ob, self.hoiks_ob, self.skyscraper_ob)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                    all_sprites_list.draw(screen)

                    pygame.display.flip()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit() 

#Here all the code for moving the boids and hoiks goes. Other classes inherits from this
class Moving_objects(Drawable_objects):
    def __init__(self):
        #her ligger det meste av det gjenværende arbeidet
        #metode for separation
        #separation: steer to avoid crowding local flockmates
        
        #metode for alignment
        #alignment: steer towards the average heading of local flockmates
        
        #metode for cohesion
        #cohesion: steer to move towards the average position (center of mass) of local flockmates
        
        self.boids_rect[0] += self.boids_speed[0]
        self.boids_rect[1] += self.boids_speed[1]
        self.hoiks_rect[0] += self.boids_speed[0]
        self.hoiks_rect[1] += self.boids_speed[1]
        
        #collision control (gjenbruke det som gjelder kollisjon med skjermen fra forrige arbeidskrav? Ellers er det bare å bruke colliderect og så 
        # hvis en hoik kolliderer med en boid er det bare å fjerne boiden fra listen med boids)

#this is the class that holds the draw method that the other classes inherits from
class Drawable_objects(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = (800, 600)
        self.all_sprite_list = pygame.sprite.Group()
        self.boids_col = (255, 255, 255)
        self.boids_pos = Vector2(0, 0)
        self.boids_size_x = 10
        self.boids_size_y = 10
        self.boids_speed = Vector2(1, 1)
        self.boids_rect = pygame.Rect(self.boids_pos[0], self.boids_pos[1], self.boids_size_x, self.boids_size_y)
        pygame.draw.polygon(screen, (self.boids_col), (random.randint(0, 800), random.randint(0, 800), random.randint(0, 800)))
        self.hoiks_col = (255, 0, 0)
        self.hoiks_pos = Vector2(10, 10)
        self.hoiks_radius = 10
        self.hoiks_speed = Vector2(1, 1)
        self.hoiks_rect = pygame.Rect(self.hoiks_pos[0], self.hoiks_pos[1], self.hoiks_size_x, self.hoiks_size_y)
        pygame.draw.circle(screen, (self.hoiks_col), (self.hoiks_rect[0], self.hoiks_rect[1]), self.hoiks_radius)
        self.skycraper_col = (192, 192, 192)
        self.skyscraper_pos = Vector2(20, 20)
        self.skyscraper_size_x = 40
        self.skyscraper_size_y = 40
        self.skyscraper_rect = pygame.Rect(self.skyscraper_pos[0], self.skyscraper_pos[1], self.skyscraper_size_x, self.skyscraper_size_y)
        pygame.draw.rect(screen, self.skyscraper_rect[0], self.skyscraper_rect[1], 1)
        

class Boids(Moving_objects, Drawable_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #make boids
        self.boids = []
        self.single_boid = []
        for h in range (50):
            
            self.boids_ob.rect.x = self.rect[0]
            self.boids_ob.rect.y = self.rect[1]
            self.all_sprites_list.add(self.boids_ob)
        self.boids.append(self.single_boid)
    #move is inherited from Moving_objects
    #circles
    
class Hoiks(Moving_objects, Drawable_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #make hoiks
        self.hoiks = []
        self.single_hoik = []
        for i in range (5):
            
            self.hoiks_ob.rect.x = self.rect[0]
            self.hoiks_ob.rect.y = self.rect[1]
            self.all_sprites_list.add(self.hoiks_ob)
        self.hoiks.append(self.single_hoik)
    #move method is inherited from Moving_objects
    #draw method is inherited from Drawable_objects
    #triangles

class Skyscrapers(Drawable_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #make skyscrapers
        self.skyscraper = []
        self.single_skyscraper = []
        for j in range (5):
            
            self.skyscraper_ob.rect.x = self.rect[0]
            self.skyscraper_ob.rect.y = self.rect[1]
            self.all_sprites_list.add(self.skyscraper_ob)
        self.skyscraper.append(self.single_skyscraper)
    #draw method is inherited from Drawable_objects
    #rectangles

    """Hva må lages? Enkleste først? Statiske objekter på skjermen som boidsene skal unngå. Nummer 2: lag predators som flyr på tvers av skjermen 
    for å prøve og spise boidsene. Kan bare gi dem en fart og en retning og når de kommer til enden av skjermen kan de snu eller dukke opp der de
    startet igjen. De statiske bbjektene kan være firkanter, predators kan være trekanter og boidsene kan være sirkler."""