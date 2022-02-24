from pygame import Vector2
import pygame

#edited pre code variables to fit with the variables I have used
def intersect_paddle_ball(rec_pos, sx, sy,
                               ball_pos, ball_radius, ball_speed):
    """ Determine if a rectangle and a circle intersects.
    Only works for a rectangle aligned with the axes.
    Parameters:
    rec_pos     - A Vector2 representing the position of the rectangles upper,
                  left corner.
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
    top = (rec_pos.y) - ball_pos.y
    bottom = (rec_pos.y + sy) - ball_pos.y
    left = (rec_pos.x) - ball_pos.x
    right = (rec_pos.x + sx) - ball_pos.x

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


def intersect_brick_ball(brick_position_x, 
                            brick_position_y, 
                            brick_size_x, 
                            brick_size_y, 
                            ball_pos, ball_radius):
    """ Determine if the red bricks and the ball intersects
    Parameters:
    brick_position_x       - Brick's position on the x axis
    brick_position_y       - Brick's position on the y axis
    brick_size_x           - Brick's size on the x axis
    brick_size_y           - Brick's size on the y axis
    ball_position              - A Vector2D representing the ball's position
    ball_radius                - Ball's radius
    Returns:
    None if no intersection.
    If the ball intersects with a red brick, it returns a normalized
    Vector2 pointing from brick_red to ball.
    """
    # vector from A to B
    dp1p2 = ball_pos - (brick_position_x + brick_position_y)

    if brick_size_x + brick_size_y + ball_radius >= pygame.math.Vector2.length(dp1p2):
        return dp1p2.normalize()
    else:
        return None

class Game:
    #my implementation of breakout

       
    def init(screen_res):
        screen_res = (800, 600)
        pygame.init()
    
    def variables(brick_size_x, brick_size_y, brick_pos_x, brick_pos_y, brick_red_col, brick_green_col, brick_blue_col):
        #defining variables

        #defining brick variables
        brick_size_x = 40
        brick_size_y = 20
        brick_pos_x = 0
        brick_pos_y = 0
        brick_red_col = 255, 0, 0
        brick_green_col = 0, 255, 0
        brick_blue_col = 0, 0, 255

        #defining paddle variables
        paddle_pos_x = pygame.mouse.get_pos()[0]
        paddle_pos_y = 590
        paddle_radius = 20
        paddle_speed = Vector2(2,0)

        #defining ball variables
        ball_pos_x = 400
        ball_pos_y = 300
        ball_radius = 5
        ball_speed = Vector2(2, -2)

    def objects(brick_ob, paddle_ob, ball_ob):
        brick_ob = Brick(brick_pos_x, brick_pos_y, brick_size_x, brick_size_y, brick_red_col, brick_green_col, brick_blue_col)
        paddle_ob = Paddle(paddle_pos_x, paddle_pos_y, paddle_radius, paddle_speed)
        ball_ob = Ball(ball_pos_x, ball_pos_y, ball_radius, ball_speed)

    def game_init(screen, clock):
        screen = pygame.display.set_mode(screen_res)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
        
    def draw_screen(screen, screen_res):
        pygame.draw.rect(screen, (0, 0, 0), ((0, 0), screen_res))
        clock.tick(30)
        
    def draw_objects(screen, brick_ob, paddle_ob, ball_ob):
        brick_ob.draw(screen)
        paddle_ob.draw(screen)
        ball_ob.draw(screen)
    
#class for the bricks
    class Brick:

        def __init__(self, brick_pos_x, brick_pos_y, brick_size_x, brick_size_y, brick_red_col, brick_green_col, brick_blue_col):
            self.brick_size_x = brick_size_x
            self.brick_size_y = brick_size_y
            self.brick_pos_x = brick_pos_x
            self.brick_pos_y = brick_pos_y
            self.brick_red_col = brick_red_col
            self.brick_green_col = brick_green_col
            self.brick_blue_col = brick_blue_col
        
        def draw(self,screen):
            rect = pygame.Rect(self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y)
            for Brick in range(20):
                pygame.draw.rect(screen, (255, 0, 0),
                (self.brick_pos_x, self.brick_pos_y, self.brick_size_x, self.brick_size_y))
    

#class and methods for the paddle
    class Paddle():
        def __init__(self, paddle_pos_x, paddle_pos_y, paddle_radius, paddle_speed): 
            self.paddle_pos_x = paddle_pos_x
            self.paddle_pos_y = paddle_pos_y
            self.paddle_radius = paddle_radius
            self.paddle_speed = 10
        
        def move(self, screen):
            self.paddle_pos_x += pygame.mouse.get_pos(screen)[0]
            self.paddle_pos_y += 590

        def draw(self, screen):
            #circle = pygame.circle(self.paddle_radius, self.paddle_pos_x, self.paddle_pos_y)
            pygame.draw.circle(screen, (255, 255, 255), (self.paddle_pos_x, self.paddle_pos_y), self.paddle_radius)

#class and methods for the ball
    class Ball():
        def __init__(self, ball_pos_x, ball_pos_y, ball_radius, ball_speed):
            self.ball_pos_x = ball_pos_x
            self.ball_pos_y = ball_pos_y
            self.ball_radius = ball_radius
            self.ball_speed = Vector2(2, -2)

        def move(self):
            self.ball_pos_x += 1
            self.ball_pos_y += -1

        def draw(self, screen):
            #circle = pygame.Circle(self.ball_radius, self.ball_pos, self.ball_speed)
            pygame.draw.circle(screen, (192, 192, 192), (self.ball_pos_x, self.ball_pos_y), self.ball_radius)

        
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

                pygame.display.update()

def example2():
    V1 = Vector2(300, 300)
    V2 = Vector2(100, 100)

    V3 = V1 + V2

    print(V3)


if __name__ == '__main__':
    breakout()
    paddle.move(1)
    ball.move(1)