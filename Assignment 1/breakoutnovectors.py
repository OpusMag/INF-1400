from pygame import Vector2
import pygame
   
    #my implementation of breakout  
class Breakout:

    

    def game_loop(self):
        pygame.init()
        self.screen_x = 800
        self.screen_y = 600
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y), 0, 32)
        pygame.display.set_caption('Breakout')
        clock = pygame.time.Clock()
        time_passed = clock.tick(30) / 1000.0
        rows = 3
        columns = 22
        brick_ob = Brick()
        ball_ob = Ball()
        paddle_ob = Paddle()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            #flytt objekter
            paddle_ob.move_paddle()
            ball_ob.move_ball()
            #tegn objekter
            paddle_ob.draw_paddle(self.screen)
            brick_ob.create_bricks(rows, columns)
            brick_ob.draw_bricks(self.screen)
            ball_ob.draw_ball(self.screen)
            
            pygame.display.flip()
            pygame.display.update()
            self.screen.fill((0,0,0))
            clock.tick(60)
        pygame.quit()
        quit()         
    
#class for the bricks
class Brick:

    def __init__(self):
        self.brick_pos = Vector2(1, 1)
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
                self.brick_pos.x = columns * self.brick_size_x
                self.brick_pos.y = rows * self.brick_size_y
                rect = pygame.Rect(self.brick_pos.x, self.brick_pos.y, self.brick_size_x, self.brick_size_y)
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
                pygame.draw.rect(screen, brick[1], brick[0], 1)

#class and methods for the paddle
class Paddle:
    def __init__(self): 
        self.paddle_pos = pygame.mouse.get_pos()
        self.paddle_pos_x = self.paddle_pos[0]
        self.paddle_pos_y = self.paddle_pos[1]
        self.paddle_radius = 20
        self.paddle_speed_x = 10
        self.paddle_speed_y = 10
        self.paddle_rect = pygame.Rect(self.paddle_pos_x, self.paddle_pos_y, self.paddle_radius * 2, self.paddle_radius * 2)

    def draw_paddle(self, screen):
        #circle = pygame.circle(self.paddle_radius, self.paddle_pos_x, self.paddle_pos_y)
        #pygame.draw.circle(screen, (255, 255, 255), (round(self.paddle_pos_x), round(self.paddle_pos_y)), self.paddle_radius)
        pygame.draw.circle(screen, (255, 255, 255), (self.paddle_rect.x, self.paddle_rect.y), self.paddle_radius)
            
    def move_paddle(self):
        self.paddle_rect.x += self.paddle_pos[0]
        self.paddle_rect.y += self.paddle_pos[1]
        #self.paddle_pos.x = paddle_pos[0]
        #self.paddle_rect.y = 600
        #pygame.display.update()
    
    def clear_screen(self):
        self.screen.fill(0, 0, 0)
        self.draw(self.screen)

#class and methods for the ball
class Ball:
    def __init__(self):
        self.ball_pos_x = 400
        self.ball_pos_y = 300
        self.ball_radius = 5
        self.ball_speed_x = 1
        self.ball_speed_y = 1
        self.ball_rect = pygame.Rect(self.ball_pos_x, self.ball_pos_y, self.ball_radius * 2, self.ball_radius * 2)
    
    def draw_ball(self, screen):
        #pygame.draw.crcle((screen), (192, 192, 192), (self.ball_pos_x, self.ball_pos_y), self.ball_radius)
        pygame.draw.circle(screen, (192, 192, 192), (self.ball_rect.x, self.ball_rect.y), self.ball_radius)
        
    def move_ball(self):
        self.screen_x = 800
        self.screen_y = 600
        self.ball_rect.x += self.ball_speed_x
        self.ball_rect.y += self.ball_speed_y

        if self.ball_rect.right >= self.screen_x or self.ball_rect.left <= 0:
            self.ball_speed_x * -1
        if self.ball_rect.bottom >= self.screen_y or self.ball_rect.top <= 0:
            self.ball_speed_y * -1
    

if __name__ == '__main__':
    br = Breakout()
    br.game_loop()
    