from pygame import Vector2
import pygame

class Game_loop:

    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('Boids')
        clock = pygame.time.Clock()
        time_passed = clock.tick(30) / 1000.0

        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(object_)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                    pygame.display.flip()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit() 

#Here all the code for moving the boids and hoiks goes. Other classes inherits from this
class Moving_objects:
    def __init__(self):
    def move():

#this is the class that holds the draw method that the other classes inherits from
class Drawable_objects:
    def __init__(self):
    
        def draw():

class Boids(Moving_objects, Drawable_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    #move is inherited from Moving_objects
    #circles
    
class Hoiks(Moving_objects, Drawable_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    #move method is inherited from Moving_objects
    #draw method is inherited from Drawable_objects
    #triangles

class Skyscrapers(Drawable_objects, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    #draw method is inherited from Drawable_objects
    #rectangles

    """Hva må lages? Enkleste først? Statiske objekter på skjermen som boidsene skal unngå. Nummer 2: lag predators som flyr på tvers av skjermen 
    for å prøve og spise boidsene. Kan bare gi dem en fart og en retning og når de kommer til enden av skjermen kan de snu eller dukke opp der de
    startet igjen. De statiske bbjektene kan være firkanter, predators kan være trekanter og boidsene kan være sirkler."""