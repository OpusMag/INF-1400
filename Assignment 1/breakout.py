from pygame import Vector2
import pygame
   
    #my implementation of breakout  
class Breakout:

    

    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), 0, 32)
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
            paddle_ob.draw_paddle(screen)
            brick_ob.create_bricks(rows, columns)
            brick_ob.draw_bricks(screen)
            ball_ob.draw_ball(screen)
            
            pygame.display.flip()
            pygame.display.update()
            screen.fill((0,0,0))
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
        self.paddle_pos = Vector2(400, 300)
        self.paddle_radius = 20
        self.paddle_speed = Vector2(10, 10)

    def draw_paddle(self, screen):
        #circle = pygame.circle(self.paddle_radius, self.paddle_pos_x, self.paddle_pos_y)
        #pygame.draw.circle(screen, (255, 255, 255), (round(self.paddle_pos_x), round(self.paddle_pos_y)), self.paddle_radius)
        pygame.draw.circle(screen, (255, 255, 255), (round(self.paddle_pos.x), round(self.paddle_pos.y)), self.paddle_radius)
            
    def move_paddle(self):
        paddle_pos = pygame.mouse.get_pos()
        self.paddle_pos.x = paddle_pos[0]
        self.paddle_pos.y = 600
        #pygame.display.update()
    
    def clear_screen(self):
        self.screen.fill(0, 0, 0)
        self.draw(self.screen)

#class and methods for the ball
class Ball:
    def __init__(self):
        self.ball_pos = Vector2(400, 300)
        self.ball_radius = 5
        self.ball_speed = Vector2(500, 500).normalize()
    
    def draw_ball(self, screen):
        #pygame.draw.crcle((screen), (192, 192, 192), (self.ball_pos_x, self.ball_pos_y), self.ball_radius)
        pygame.draw.circle(screen, (192, 192, 192), (round(self.ball_pos.x), round(self.ball_pos.y)), self.ball_radius, 0)
        
    def move_ball(self):
        self.ball_pos += self.ball_speed

    #edited pre code variables to fit with the variables I have used
    def intersect_brick_ball(brick_pos, brick_size_x, brick_size_y,
                               ball_pos, ball_radius, ball_speed):
        """ Determine if a rectangle and a circle intersects.
        Only works for a rectangle aligned with the axes.
        Parameters:
        rec_pos     - A Vector2 representing the position of the rectangles upper,left corner.
        sx          - Width of rectangle.
        sy          - Height of rectangle.
        circle_pos  - A Vector2 representing the circle's position.
        circle_radius - The circle's radius.
        circle_speed - A Vector2 representing the circles speed.
        Returns:
        None if no intersection. 
        If the rectangle and the circle intersect,returns a 
        normalized Vector2 pointing in the direction the circle will
        move after the collision.
        """

        # Position of the walls relative to the ball
        top = (brick_pos.y) - ball_pos.y
        bottom = (brick_pos.y + brick_size_y) - ball_pos.y
        left = (brick_pos.x) - ball_pos.x
        right = (brick_pos.x + brick_size_x) - ball_pos.x

        r = ball_radius
        intersecting = left <= r and top <= r and right >= -r and bottom >= -r

        if intersecting:
            # Now need to figure out the vector to return.
            impulse = ball_speed.normalize()

            if abs(left) <= r and impulse.x > 0:
                impulse.x = -impulse.x
            if abs(right) <= r and impulse.x < 0:
                impulse.x = -impulse.x
            if abs(top) <= r and impulse.y > 0:
                impulse.y = -impulse.y
            if abs(bottom) <= r and impulse.y < 0:
                impulse.y = -impulse.y
            return impulse.normalize()
        return None


    def intersect_paddle_ball(ball_pos, 
                            ball_radius, 
                            paddle_pos, 
                            paddle_radius):
        """ Determine if the red bricks and the ball intersects
        Parameters:
        paddle_pos             - Paddle's position on the x axis
        paddle_radius          - Paddle's size on the x axis
        brick_size_y           - Brick's size on the y axis
        ball_position          - A Vector2D representing the ball's position
        ball_radius            - Ball's radius
        Returns:
        None if no intersection.
        If the ball intersects with a red brick, it returns a normalized
        Vector2 pointing from brick_red to ball.
        """
        # vector from A to B
        dp1p2 = ball_pos - paddle_pos

        if paddle_radius + ball_radius >= pygame.math.Vector2.length(dp1p2):
            return dp1p2.normalize()
        else:
            return None
        
        """if self.ball_pos.x < 0:
            self.ball_speed = abs(Vector2(0, 30))
        if self.ball_pos.y < 0:
            self.ball_speed = abs(Vector2(30, 0))
        if self.ball_pos.x > 800:
            self.ball_speed = abs(Vector2(0, 30))
        if self.ball_pos.y > 600:
            self.ball_speed = abs(Vector2(30, 0))"""
    def collision_paddle_ball(ball_pos, ball_radius, paddle_pos, paddle_radius):
        impulse = intersect_paddle_ball(ball_pos, ball_radius,
                                    paddle_pos, paddle_radius)
        if impulse:
            ball_speed = ball_speed * -1

    def collision_brick_ball(brick_pos_x, brick_pos_y, brick_size_x, brick_size_y, ball_pos, ball_radius, ball_speed):
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
            kill(Brick)

if __name__ == '__main__':
    br = Breakout()
    br.game_loop()
    