from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GLine
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 3  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 45  # Height of a brick (in pixels).
BRICK_HEIGHT = 16  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 120  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 5  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 5  # Height of the paddle (in pixels).
PADDLE_OFFSET = 100  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 5.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 7.0  # Maximum initial horizontal speed for the ball.

INITIAL_LIVES = 5
score = 0  # Create a space to store the point.
win = False  # When all bricks are disappeared, the player win the the game. "win" will be changed into True.
reflecting_up = True
reflecting_left = True
reflecting_right = True


class Start:
    def __init__(self, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_spacing=BRICK_SPACING):
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = 650

        self.window = GWindow(width=500, height=700)
        image = GImage.from_file("/Users/Paul/Desktop/PyCharm Ball Game/Arial 開始畫面2.png")  # 圖片路徑需修改！！
        self.window.add(image)


class Win:
    def __init__(self):
        self.window = GWindow(width=500, height=700)
        image = GImage.from_file("/Users/Paul/Desktop/PyCharm Ball Game/Arial 獲勝畫面2.png")  # 圖片路徑需修改！！
        self.window.add(image)


class Gameover:
    def __init__(self):
        self.window = GWindow(width=500, height=700)
        image = GImage.from_file("/Users/Paul/Desktop/PyCharm Ball Game/Arial game over畫面2.png")  # 圖片路徑需修改！！
        self.window.add(image)
        # create a score label
        self.score = GLabel("SCORE: " + str("{:0>5d}".format(score)), x=100, y=450)
        self.score.font = "Arial-35"
        self.score.color = "#00C2CB"
        self.window.add(self.score)


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 lives=INITIAL_LIVES, title='Breakout'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = 650
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a black background
        self.black = GRect(width=window_width, height=window_height, x=0, y=0)
        self.black.filled = True
        self.window.add(self.black)

        # Create a white paddle.
        self.paddle = GRect(width=paddle_width, height=paddle_height, x=(window_width - paddle_width) / 2,
                            y=window_height - paddle_offset)
        self.paddle.filled = True
        self.paddle.color = "#C4D6BB"
        self.paddle.fill_color = "#C4D6BB"
        self.window.add(self.paddle)

        # Create a score label.
        self.score = GLabel("SCORE: " + str("{:0>5d}".format(score)), x=self.window.width - 200, y=82)
        self.score.font = "Arial-20"
        self.score.color = "#CB6CE6"
        self.window.add(self.score)

        # Create a life label
        self.lives = lives
        self.life = GLabel("LIVES: " + str(lives), x=self.window.width - 200, y=58)
        self.life.font = "Arial-20"
        self.life.color = "#CB6CE6"
        self.window.add(self.life)

        # create the topic label
        self.topic1 = GLabel("BR", x=32, y=60)
        self.topic1.font = "Arial-35"
        self.topic1.color = "#00C2CB"
        self.topic2 = GLabel("ICKS", x=78, y=60)
        self.topic2.font = "Arial-35"
        self.topic2.color = "#CB6CE6"
        self.topic3 = GLabel("BR", x=32, y=90)
        self.topic3.font = "Arial-35"
        self.topic3.color = "#00C2CB"
        self.topic4 = GLabel("EAKOUT", x=78, y=90)
        self.topic4.font = "Arial-35"
        self.topic4.color = "#CB6CE6"
        self.window.add(self.topic1)
        self.window.add(self.topic2)
        self.window.add(self.topic3)
        self.window.add(self.topic4)

        # Create a line over the bricks
        self.line1 = GRect(width=46, height=2, x=33, y=84)
        self.line1.filled = True
        self.line1.color = "#00C2CB"
        self.line1.fill_color = "#00C2CB"
        self.line2 = GRect(width=335, height=2, x=80, y=84)
        self.line2.filled = True
        self.line2.color = "#CB6CE6"
        self.line2.fill_color = "#CB6CE6"
        self.window.add(self.line1)
        self.window.add(self.line2)

        # 圖片路徑需修改！！
        image_path = "/Users/Paul/Desktop/PyCharm Ball Game/ghost.png"
        self.ghost = GImage(image_path)
        x = (window_width / 2) - 5
        y = BRICK_OFFSET - 25
        self.window.add(self.ghost, x, y)
        self.shift_x = 0

        # Center a ball in the graphical window.
        self.ball = GOval(ball_radius * 2, ball_radius * 2, x=(window_width - ball_radius) / 2,
                          y=(window_height - ball_radius) / 2)
        self.ball.color = "#C4D6BB"
        self.ball.filled = True
        self.ball.fill_color = "#C4D6BB"
        self.window.add(self.ball)
        self.start = False
        self.__dy = 0
        self.__dx = 0

        # Initialize our mouse listeners and connect the the paddle with the mouse.
        onmousemoved(self.track)
        onmouseclicked(self.switch_on)

        # Draw bricks.
        times_col = BRICK_COLS
        times_row = BRICK_ROWS
        y_co = 0
        x_co = 0
        reset = False
        color = 0
        for i in range(times_row):
            c = i % 14
            # Set the default color of bricks.
            if 0 <= c <= 1:
                color = "red"
            elif 2 <= c <= 3:
                color = "orange"
            elif 4 <= c <= 5:
                color = "yellow"
            elif 6 <= c <= 7:
                color = "green"
            elif 8 <= c <= 9:
                color = "blue"
            elif 10 <= c <= 11:
                color = "indigo"
            elif 12 <= c <= 13:
                color = "purple"

            if reset:
                x_co = 0
            for j in range(times_col):
                if x_co >= window_width:
                    pass
                else:
                    self.brick = GRect(width=BRICK_WIDTH, height=BRICK_HEIGHT, x=x_co,
                                       y=BRICK_OFFSET + y_co)  # Center of not?
                    self.brick.filled = True
                    self.brick.fill_color = color
                    self.brick.color = color
                    self.window.add(self.brick)
                    x_co += BRICK_SPACING + BRICK_WIDTH
            y_co += BRICK_SPACING + BRICK_HEIGHT
            reset = True

        self.set_velocity()

    # Default initial velocity for the ball and ghost.
    def set_velocity(self):
        self.__dx = random.randint(3, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        self.shift_x = random.randint(3, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        if random.random() > 0.5:
            self.shift_x = -self.shift_x

    # Function for ghost and ball to move.
    def move(self):

        # Set a switch to start.
        if self.start:
            self.ball.move(self.__dx, self.__dy)
            self.ghost.move(self.shift_x, 0)

        # Condition: reflects when ball or ghost touches border.
        if self.window.width - self.ball.width <= self.ball.x or self.ball.x <= 0:
            self.__dx = -self.__dx
        if self.ball.y <= 86:
            self.__dy = -self.__dy
        if self.ghost.x + 10 >= self.window.width or self.ghost.x <= 0:
            self.shift_x = -self.shift_x

    # Function to reflect the ball when it touches border.
    def reflect(self):
        global reflecting_up, reflecting_left, reflecting_right

        # lower middle point of the ball
        point00_x = self.ball.x + BALL_RADIUS
        point00_y = self.ball.y + BALL_RADIUS * 2

        # left middle point of the ball
        point01_x = self.ball.x
        point01_y = self.ball.y + BALL_RADIUS

        # right middle point of the ball
        point02_x = self.ball.x + BALL_RADIUS * 2
        point02_y = self.ball.y + BALL_RADIUS

        # Plus or minus 0.1 to prevent the function from detecting the ball itself.
        maybe_obj00 = self.window.get_object_at(point00_x, point00_y + 0.1)
        maybe_obj01 = self.window.get_object_at(point01_x - 0.1, point01_y)
        maybe_obj02 = self.window.get_object_at(point02_x + 0.1, point02_y)
        if maybe_obj00 is self.paddle:
            if reflecting_up == True:
                reflecting_up = False
                self.__dy = -self.__dy
            else:
                pass
        else:
            reflecting_up = True
        if maybe_obj01 is self.paddle:
            if reflecting_right == True:
                reflecting_right = False
                self.__dx = -self.__dx
            else:
                pass
        else:
            reflecting_right = True
        if maybe_obj02 is self.paddle:
            if reflecting_left == True:
                reflecting_left = False
                self.__dx = -self.__dx
            else:
                pass
        else:
            reflecting_left = True

    # Function to switch on when the game starts.
    def switch_on(self, event):
        self.start = True

    # Function to switch off when the game pauses.
    def switch_off(self):
        self.start = False

    # Function to track the mouse and connect it with the paddle.
    def track(self, event):
        x_smallest = 0
        self.paddle.x = event.x - self.paddle.width / 2

        if self.paddle.x > self.window.width - self.paddle.width or self.paddle.x == self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width
        elif self.paddle.x < x_smallest or self.paddle.x == x_smallest:
            self.paddle.x = x_smallest

    # Function to create a new ball when the ball is going out of the border.
    def reset_ball(self):
        self.set_ball_position()
        self.set_velocity()
        self.ball.filled = True
        self.ball.fill_color = "#C4D6BB"
        self.window.add(self.ball)
        self.switch_off()

    # Function to set the new ball in the middle of the window.
    def set_ball_position(self):
        self.ball.x = (self.window.width - BALL_RADIUS) / 2
        self.ball.y = (self.window.height - BALL_RADIUS * 2) / 2

    '''
    Function to remove bricks and reflect the ball 
    when four middle points touch any brickand to count the scores.
    '''

    def remove_and_score(self):

        # Count the score of the game.
        global score

        # top middle point of the ball.
        point1_x = self.ball.x + BALL_RADIUS
        point1_y = self.ball.y
        # left middle point of the ball.
        point2_x = self.ball.x
        point2_y = self.ball.y + BALL_RADIUS
        # botoom middle point of the ball.
        point3_x = self.ball.x + BALL_RADIUS
        point3_y = self.ball.y + BALL_RADIUS * 2
        # right middle point of the ball.
        point4_x = self.ball.x + BALL_RADIUS * 2
        point4_y = self.ball.y + BALL_RADIUS

        # Plus or minus 0.1 to prevent the function from detecting the ball itself.
        maybe_obj1 = self.window.get_object_at(point1_x, point1_y - 0.1)
        maybe_obj2 = self.window.get_object_at(point2_x - 0.1, point2_y)
        maybe_obj3 = self.window.get_object_at(point3_x, point3_y + 0.1)
        maybe_obj4 = self.window.get_object_at(point4_x + 0.1, point4_y)

        if (maybe_obj1 is not None and maybe_obj1 is not self.paddle
                and maybe_obj1 is not self.score and maybe_obj1 is not self.life
                and maybe_obj1 is not self.black and maybe_obj1 is not self.line1
                and maybe_obj1 is not self.line2 and maybe_obj1 is not self.topic3
                and maybe_obj1 is not self.topic4):
            self.window.remove(maybe_obj1)
            self.__dy = -self.__dy
            if maybe_obj1 is not self.ghost:
                score += 10
            # Condition: when hitting the ghost, win the game.
            else:
                score += 1000
            self.score.text = "SCORE: " + str("{:0>5d}".format(score))
            self.window.add(self.score)
        elif (maybe_obj2 is not None and maybe_obj2 is not self.paddle
              and maybe_obj2 is not self.score and maybe_obj2 is not self.life
              and maybe_obj2 is not self.black and maybe_obj2 is not self.line1
              and maybe_obj2 is not self.line2 and maybe_obj2 is not self.topic3
              and maybe_obj2 is not self.topic4):
            self.window.remove(maybe_obj2)
            self.__dx = -self.__dx
            if maybe_obj2 is not self.ghost:
                score += 10
            else:
                score += 1000
            self.window.remove(self.score)
            self.score.text = "SCORE: " + str("{:0>5d}".format(score))
            self.window.add(self.score)
        elif (maybe_obj3 is not None and maybe_obj3 is not self.paddle
              and maybe_obj3 is not self.score and maybe_obj3 is not self.life
              and maybe_obj3 is not self.black and maybe_obj3 is not self.line1
              and maybe_obj3 is not self.line2 and maybe_obj3 is not self.topic3
              and maybe_obj3 is not self.topic4):
            self.window.remove(maybe_obj3)
            self.__dy = -self.__dy
            if maybe_obj3 is not self.ghost:
                score += 10
            else:
                score += 1000
            self.window.remove(self.score)
            self.score.text = "SCORE: " + str("{:0>5d}".format(score))
            self.window.add(self.score)
        elif (maybe_obj4 is not None and maybe_obj4 is not self.paddle
              and maybe_obj4 is not self.score and maybe_obj4 is not self.life
              and maybe_obj4 is not self.black and maybe_obj4 is not self.line2
              and maybe_obj4 is not self.line2 and maybe_obj4 is not self.topic3
              and maybe_obj4 is not self.topic4):
            self.window.remove(maybe_obj4)
            self.__dx = -self.__dx
            if maybe_obj4 is not self.ghost:
                score += 10
            else:
                score += 1000
            self.window.remove(self.score)
            self.score.text = "SCORE: " + str("{:0>5d}".format(score))
            self.window.add(self.score)

    # function to show the remaining lives
    def countlives(self):
        if self.ball.y >= self.window.height:
            self.lives -= 1
            self.window.remove(self.life)
            self.life.text = "LIVES: " + str(self.lives)
            self.window.add(self.life)


    # Situation when the player wins the game.
    def finished(self):
        global win
        if score >= 1000:
            win = True
        return win
