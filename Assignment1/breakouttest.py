from pygame import Vector2
import pygame


class Breakout:

    brick_pos_x = 0
    brick_pos_y = 0
    brick_size_x = 40
    brick_size_y = 20
    brick_red_col = 255, 0, 0
    brick_green_col = 0, 255, 0
    brick_blue_col = 0, 0, 255
    rows = 3
    columns = 20
    paddle_pos_x = 400
    paddle_pos_y = 590
    paddle_radius = 20
    paddle_speed = (0, 1)
    ball_pos_x = 400
    ball_pos_y = 300
    ball_radius = 10
    ball_speed = (0, -1)
            
    #my implementation of breakout
    def __init__(self):
            
            self.screen_res = (800, 600)
            self.screen = pygame.display.set_mode()
            self.columns = 20
            self.rows = 3
            self.brick_size_x = 40
            self.brick_size_y = 20
            self.brick_pos_x = 20 * self.columns
            self.brick_pos_y = 0
            self.brick_red_col = 255, 0, 0
            self.brick_green_col = 0, 255, 0
            self.brick_blue_col = 0, 0, 255

    #paddle_variable(self, paddle_pos_x, paddle_pos_y, paddle_radius, paddle_speed):
    #defining paddle variables
            pygame.init()
            self.paddle_pos_x = pygame.mouse.get_pos()[0]
            self.paddle_pos_y = 590
            self.paddle_radius = 20
            self.paddle_speed = Vector2(2,0)

    #ball_variables(self, ball_pos_x, ball_pos_y, ball_radius, ball_speed):
    #defining ball variables
            self.ball_pos_x = 400
            self.ball_pos_y = 300
            self.ball_radius = 5
            self.ball_speed = Vector2(2, -2)
       
    
            
    #brick_variables(self, brick_size_x, brick_size_y, brick_pos_x, brick_pos_y, brick_red_col, brick_green_col, brick_blue_col):
    #defining brick variables
    
#class for the bricks
    class Brick:

        def __init__(self, brick_pos_x, brick_pos_y, brick_size_x, brick_size_y, brick_red_col, brick_green_col, brick_blue_col):
            self.brick_pos_x = brick_pos_x
            self.brick_pos_y = brick_pos_y
            self.brick_size_x = brick_size_x
            self.brick_size_y = brick_size_y
            self.brick_red_col = brick_red_col
            self.brick_green_col = brick_green_col
            self.brick_blue_col = brick_blue_col
            
        def create_bricks(self, brick_size_x, brick_size_y, rows, columns):
            self.brick_size_x = 40
            self.brick_size_y = 20
            self.rows = 3
            self.columns = 20
            self.brick_red_col = (255, 0, 0)
            self.brick_green_col = (0, 255, 0)
            self.brick_blue_col = (0, 0, 255)
            self.brick = []

            single_brick = []
            for row in range(rows):
                brick_row = []
            for cols in range(columns):
                brick_pos_x = columns * brick_size_x
                brick_pos_y = rows * brick_size_y
                rect = pygame.Rect(self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y)
                if row == 1:
                    brick_col = 255, 0, 0
                elif row == 2:
                    brick_col = 0, 255, 0
                elif row == 3:
                    brick_col = 0, 0, 255
                single_brick = [rect, brick_col]
                brick_row.append(single_brick)
            
            self.brick.append(brick_row)

        
        def draw_bricks(self):
            screen_res = (800, 600)
            screen = pygame.display.set_mode(screen_res)
            for row in self.brick:
                for brick in row:
                    pygame.draw.rect(screen, brick[1], brick[0])

    
    brick_ob = Brick(brick_pos_x, brick_pos_y, brick_size_x, brick_size_y, brick_red_col, brick_green_col, brick_blue_col)
    brick_ob.create_bricks(brick_size_x, brick_size_y, rows, columns)
    brick_ob.draw_bricks()

#class and methods for the paddle
    class Paddle:
        def __init__(self, paddle_pos_x, paddle_pos_y, paddle_radius, paddle_speed): 
            self.paddle_pos_x = paddle_pos_x
            self.paddle_pos_y = paddle_pos_y
            self.paddle_radius = paddle_radius
            self.paddle_speed = paddle_speed
            
        def move_paddle(self):
            self.paddle_pos_x = pygame.mouse.get_pos()[0]

        def draw_paddle(self):
            screen_res = (800, 600)
            screen = pygame.display.set_mode(screen_res)
            #circle = pygame.circle(self.paddle_radius, self.paddle_pos_x, self.paddle_pos_y)
            pygame.draw.circle(screen, (255, 255, 255), (self.paddle_pos_x, self.paddle_pos_y), self.paddle_radius)

    paddle_ob = Paddle(paddle_pos_x, paddle_pos_y, paddle_radius, paddle_speed)
    paddle_ob.draw_paddle()
    paddle_ob.move_paddle()

#class and methods for the ball
    class Ball:
        def __init__(self, ball_pos_x, ball_pos_y, ball_radius, ball_speed):
            self.ball_pos_x = ball_pos_x
            self.ball_pos_y = ball_pos_y
            self.ball_radius = ball_radius
            self.ball_speed = Vector2(2, -2)

        def move_ball(self):
            self.ball_pos_x += 1
            self.ball_pos_y += -1
        
        def collision_paddle(impulse, paddle_pos_x, paddle_pos_y, paddle_radius, ball_pos, ball_radius, ball_speed):
            #tests and handles intersections between paddle and ball
            impulse = intersect_paddle_ball(paddle_pos_x, 
                                        paddle_pos_y, 
                                        paddle_radius,
                                        ball_pos,
                                        ball_radius,
                                        ball_speed)
            if impulse:
                ball_speed = ball_speed * -1

        def collision_brick(brick_pos_x, brick_pos_y, brick_size_x, brick_size_y, ball_pos, ball_radius, ball_speed):
            #tests and handles intersections between bricks and ball
            impulse = intersect_brick_ball(brick_pos_x,
                                            brick_pos_y,
                                            brick_size_x,
                                            brick_size_y,
                                            ball_pos,
                                            ball_radius,
                                            ball_speed)
            if impulse:
                ball_speed = ball_speed * -1
                del brick

        def draw_ball(self):
            screen_res = (800, 600)
            screen = pygame.display.set_mode(screen_res)
            #circle = pygame.Circle(self.ball_radius, self.ball_pos, self.ball_speed)
            pygame.draw.circle(screen, (192, 192, 192), (self.ball_pos_x, self.ball_pos_y), self.ball_radius)

    ball_ob = Ball(ball_pos_x, ball_pos_y, ball_radius, ball_speed)
    ball_ob.draw_ball()
    ball_ob.move_ball()

    class Game_loop:
        def __init__(self):
            pygame.init()
            screen_res = (800, 600)
            screen = pygame.display.set_mode((800, 600))
            pygame.draw.rect(screen, (0, 0, 0), ((0, 0), screen_res))
            pygame.display.set_caption('Breakout')
            clock = pygame.time.Clock()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                pygame.display.update()
                clock.tick(60)
            pygame.quit()
            quit()    


if __name__ == '__main__':
    br = Breakout()
    br.Game_loop()
    