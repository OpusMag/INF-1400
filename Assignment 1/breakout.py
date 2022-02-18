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


def intersect_brick_red_ball(brick_red_position_x, 
                            brick_red_position_y, 
                            brick_red_size_x, 
                            brick_red_size_y, 
                            ball_pos, ball_radius):
    """ Determine if the red bricks and the ball intersects
    Parameters:
    brick_red_position_x       - Red brick's position on the x axis
    brick_red_position_y       - Red brick's position on the y axis
    brick_red_size_x           - Red brick's size on the x axis
    brick_red_size_y           - Red brick's size on the y axis
    ball_position              - A Vector2D representing the ball's position
    ball_radius                - Ball's radius
    Returns:
    None if no intersection.
    If the ball intersects with a red brick, it returns a normalized
    Vector2 pointing from brick_red to ball.
    """
    # vector from A to B
    dp1p2 = ball_pos - (brick_red_position_x + brick_red_position_y)

    if brick_red_size_x + brick_red_size_y + ball_radius >= pygame.math.Vector2.length(dp1p2):
        return dp1p2.normalize()
    else:
        return None

def intersect_brick_green_ball(brick_green_position_x, 
                                brick_green_position_y, 
                                brick_green_size_x, 
                                brick_green_size_y, 
                                ball_pos, ball_radius):
    """ Determine if the red bricks and the ball intersects
    Parameters:
    brick_green_position_x       - Green brick's position on the x axis
    brick_green_position_y       - Green brick's position on the y axis
    brick_green_size_x           - Green brick's size on the x axis
    brick_green_size_y           - Green brick's size on the y axis
    ball_position                - A Vector2D representing the ball's position
    ball_radius                  - Ball's radius
    Returns:
    None if no intersection.
    If the ball intersects with a green brick, it returns a normalized
    Vector2 pointing from brick_green to ball.
    """
    # vector from A to B
    dp1p2 = ball_pos - (brick_green_position_x + brick_green_position_y)

    if brick_green_size_x + brick_green_size_y + ball_radius >= pygame.math.Vector2.length(dp1p2):
        return dp1p2.normalize()
    else:
        return None

def intersect_brick_blue_ball(brick_blue_position_x, 
                                brick_blue_position_y, 
                                brick_blue_size_x, 
                                brick_blue_size_y, 
                                ball_pos, ball_radius):
    """ Determine if the blue bricks and the ball intersects
    Parameters:
    brick_blue_position_x       - Blue brick's position on the x axis
    brick_blue_position_y       - Blue brick's position on the y axis
    brick_blue_size_x           - Blue brick's size on the x axis
    brick_blue_size_y           - Blue brick's size on the y axis
    ball_position               - A Vector2D representing the ball's position
    ball_radius                 - Ball's radius
    Returns:
    None if no intersection.
    If the ball intersects with a blue brick, it returns a normalized
    Vector2 pointing from brick_blue to ball.
    """
    # vector from A to B
    dp1p2 = ball_pos - (brick_blue_position_x + brick_blue_position_y)

    if brick_blue_size_x + brick_blue_size_y + ball_radius >= pygame.math.Vector2.length(dp1p2):
        return dp1p2.normalize()
    else:
        return None

def breakout():
    #my implementation of breakout

    screen_res = (800, 600)
    pygame.init()
    
    #defining variables

    #brick colors used
    brick_red = (255, 0, 0)
    brick_green = (0, 255, 0)
    brick_blue = (0, 0, 255)
    
    #paddle color
    paddle_col = (255, 255, 255)
    
    #ball color
    ball_col = (192, 192, 192)

    #define number of bricks for each color
    brick_red_num = 20
    brick_green_num = 20
    brick_blue_num = 20

    #defining red brick variables
    brick_red_size_x = 20
    brick_red_size_y = 10
    brick_red_pos_x = 0
    brick_red_pos_y = 0

    #defining green brick variables
    brick_green_size_x = 20
    brick_green_size_y = 10
    brick_green_pos_x = 0
    brick_green_pos_y = 10

    #defining blue brick variables
    brick_blue_size_x = 20
    brick_blue_size_y = 10
    brick_blue_pos_x = 0
    brick_blue_pos_y = 20

    #defining paddle variables
    paddle_radius = 10
    paddle_pos_x = pygame.mouse.get_pos()
    paddle_pos_y = 590

    #defining ball variables
    ball_radius = 5
    ball_pos = Vector2(400, 300)
    ball_speed = Vector2(2, -2)

    object.brick_red = Brick_red
    object.brick_green = Brick_green
    object.brick_blue = Brick_blue
    object.paddle = Paddle
    object.ball = Ball

    screen = pygame.display.set_mode(screen_res)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    
#class for the red bricks
class Brick_red:
    def __init__(self, brick_red_pos_x, brick_red_pos_y, brick_red_size_x, brick_red_size_y):
        self.brick_red_size_x = brick_red_size_x
        self.brick_red_size_y = brick_red_size_y
        self.brick_red_pos_x = brick_red_pos_x
        self.brick_red_pos_y = brick_red_pos_y  
        
def draw(self):
    rect = pygame.rect(self, brick_red_pos_x, brick_red_pos_y, brick_red_size_x, brick_red_size_y)
    for brick_red in range(brick_red_num):
        pygame.draw.rect(screen, (255, 0, 0),
            (brick_red_pos_x * 2, brick_red_pos_y * 2, brick_red_size_x, brick_red_size_y))
    
#class for the green bricks
class Brick_green:
    def __init__(self, brick_green_pos_x, brick_green_pos_y, brick_green_size_x, brick_green_size_y):
        self.brick_green_size_x = brick_green_size_x
        self.brick_green_size_y = brick_green_size_y
        self.brick_green_pos_x = brick_green_pos_x
        self.brick_green_pos_y = brick_green_pos_y 
        
    def draw(self):
        rect = pygame.rect(self, brick_green_pos_x, brick_green_pos_y, brick_green_size_x, brick_green_size_y)
        for brick_green in range(brick_green_num):
            pygame.draw.rect(screen, (255, 0, 0),
            (brick_green_pos_x * 2, brick_green_pos_y * 2, brick_green_size_x, brick_green_size_y))

#class for the blue bricks
class Brick_blue:
    def __init__(self, brick_blue_pos_x, brick_blue_pos_y, brick_blue_size_x, brick_blue_size_y):
        self.brick_blue_size_x = brick_blue_size_x
        self.brick_blue_size_y = brick_blue_size_y
        self.brick_blue_pos_x = brick_blue_pos_x
        self.brick_blue_pos_y = brick_blue_pos_y  
    
    def draw(self):
        rect = pygame.rect(self, brick_blue_pos_x, brick_blue_pos_y, brick_blue_size_x, brick_blue_size_y)
        for brick_blue in range(brick_blue_num):
            pygame.draw.rect(screen, (255, 0, 0),
            (brick_blue_pos_x * 2, brick_blue_pos_y * 2, brick_blue_size_x, brick_blue_size_y))

#class and methods for the paddle
class Paddle():
    def __init__(self):
        self.paddle_radius = paddle_radius 
        self.paddle_pos_x = paddle_pos_x
        self.paddle_pos_y = paddle_pos_y  
        
    def move(self):
        self.paddle_pos_x = paddle_pos_x
        self.paddle_pos_y = paddle_pos_y

    def draw(self):
        circle = pygame.circle(self, paddle_radius, paddle_pos_x, paddle_pos_y)
        pygame.draw.circle(screen, (255, 255, 255), (paddle_radius, paddle_pos_x, paddle_pos_y))

#class and methods for the ball
class Ball():
    def __init__(self):
        self.ball_radius = ball_radius
        self.ball_pos = ball_pos 

    def move(self):
        self.ball_speed = ball_speed

    def draw(self):
        circle = pygame.circle(self, ball_radius, ball_pos, ball_speed)
        pygame.draw.rect(screen, (192, 192, 192), (ball_radius, ball_pos, ball_speed))

        #tests and handles intersections between paddle and ball
        impulse = intersect_paddle_ball(paddle_pos_x, 
                                paddle_pos_y, 
                                paddle_radius,
                                ball_pos,
                                ball_radius,
                                ball_speed)
        if impulse:
            ball_speed = ball_speed * -1

        #tests and handles intersections between red bricks and ball
        impulse = intersect_brick_red_ball(brick_red_pos_x,
                                    brick_red_pos_y,
                                    brick_red_size_x,
                                    brick_red_size_y,
                                    ball_pos,
                                    ball_radius,
                                    ball_speed)
        if impulse:
            ball_speed = ball_speed * -1
            del brick_red

        #tests and handles intersections between green bricks and ball
        impulse = intersect_brick_green_ball(brick_green_pos_x,
                                    brick_green_pos_y,
                                    brick_green_size_x,
                                    brick_green_size_y,
                                    ball_pos,
                                    ball_radius,
                                    ball_speed)
        if impulse:
            ball_speed = ball_speed * -1
            del brick_green
        
        #tests and handles intersections between blue bricks and ball
        impulse = intersect_brick_blue_ball(brick_blue_pos_x,
                                    brick_blue_pos_y,
                                    brick_blue_size_x,
                                    brick_blue_size_y,
                                    ball_pos,
                                    ball_radius,
                                    ball_speed)
        if impulse:
            ball_speed = ball_speed * -1
            del brick_blue
        
        pygame.display.update()

breakout()