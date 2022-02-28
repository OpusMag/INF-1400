import pygame

class Breakout:

    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), 0, 32)
        pygame.display.set_caption('Breakout')
        clock = pygame.time.Clock()
        rows = 3
        columns = 22
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #lag objekter
            brick_ob = Brick()
            ball_ob = Ball()
            paddle_ob = Paddle()
            #flytt objekter
            paddle_ob.move_paddle()
            ball_ob.move_ball()
            #tegn objekter
            brick_ob.create_bricks(rows, columns)
            brick_ob.draw_bricks(screen)
            ball_ob.draw_ball(screen)
            paddle_ob.draw_paddle(screen)
            
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()    
            
    #my implementation of breakout        
    
#class for the bricks
class Brick:

    def __init__(self):
        self.brick_pos_x = 1
        self.brick_pos_y = 1
        self.brick_size_x = 40
        self.brick_size_y = 20
        self.brick_red_col = 255, 0, 0
        self.brick_green_col = 0, 255, 0
        self.brick_blue_col = 0, 0, 255
        self.brick_col = 255, 255, 255
            
    def create_bricks(self, rows, columns):
        self.brick = []
        single_brick = []
        for rows in range(rows):
            brick_row = []
            for columns in range(columns):
                self.brick_pos_x = columns * self.brick_size_x
                self.brick_pos_y = rows * self.brick_size_y
                rect = pygame.Rect(self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y)
                if rows == 0:
                    brick_col = 255, 0, 0
                elif rows == 1:
                    brick_col = 0, 255, 0
                elif rows == 2:
                    brick_col = 0, 0, 255
                else:
                    brick_col = 255, 255, 255
                single_brick = [rect, brick_col]
                brick_row.append(single_brick)
            
            self.brick.append(brick_row)

        
    def draw_bricks(self, screen):
        self.screen = screen
        for row in self.brick:
            for brick in row:
                pygame.draw.rect(screen, brick[1], brick[0])

#class and methods for the paddle
class Paddle:
    def __init__(self): 
        self.paddle_pos_x = 400
        self.paddle_pos_y = 600
        self.paddle_radius = 20
        self.paddle_speed = [10, 10]
            
    def move_paddle(self):
        paddle_pos = pygame.mouse.get_pos()
        self.paddle_pos_x = paddle_pos[0]
        self.paddle_pos_y = 600
        #pygame.display.update()

    def draw_paddle(self, screen):
        #circle = pygame.circle(self.paddle_radius, self.paddle_pos_x, self.paddle_pos_y)
        #pygame.draw.circle(screen, (255, 255, 255), (round(self.paddle_pos_x), round(self.paddle_pos_y)), self.paddle_radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.paddle_pos_x), int(self.paddle_pos_y)), self.paddle_radius)

#class and methods for the ball
class Ball:
    def __init__(self):
        self.ball_pos_x = 400
        self.ball_pos_y = 300
        self.ball_speed = [10, 10]
        self.ball_radius = 10

    def move_ball(self):
        self.ball_pos_x += self.ball_speed[0]
        self.ball_pos_y += self.ball_speed[1]

        print(self.ball_speed)
        
    
    def draw_ball(self, screen):
        #pygame.draw.crcle((screen), (192, 192, 192), (self.ball_pos_x, self.ball_pos_y), self.ball_radius)
        pygame.draw.circle(screen, (192, 192, 192),
                           (int(self.ball_pos_x),
                           int(self.ball_pos_y)),
                           self.ball_radius)

if __name__ == '__main__':
    br = Breakout()
    br.game_loop()