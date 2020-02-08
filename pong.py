# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    hor_vel = random.randrange(120, 240) / 60.0
    ver_vel = random.randrange(60, 180) / 60.0
#    ball_vel = [1.6, -1.1]
    if direction == "RIGHT":
        ball_vel = [hor_vel, -ver_vel]
    elif direction == "LEFT":
        ball_vel = [-hor_vel, -ver_vel]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # positioning the paddles 
    paddle1_pos = (HEIGHT / 2)
    paddle2_pos = (HEIGHT / 2)
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    # Randomizing initial ball direction
    random_direction = random.randrange(0,2)
    if random_direction == 0:
        spawn_ball("RIGHT")
    else:
        spawn_ball("LEFT")   

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, player1, player2
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]	
    ball_pos[1] += ball_vel[1]
    
    if ( ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS ):
        ball_vel[1] = - ball_vel[1]

    # test whether the ball touches/collides with the left and right gutters
    if ( ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS) ):
        if ( ball_pos[1] <= paddle1_pos + ( PAD_HEIGHT / 2 )
            and ball_pos[1] >= paddle1_pos - ( PAD_HEIGHT / 2 )):
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            score2 += 1
            spawn_ball("RIGHT")
    elif ( ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS) ):
        if ( ball_pos[1] <= paddle2_pos + ( PAD_HEIGHT / 2 )
            and ball_pos[1] >= paddle2_pos - ( PAD_HEIGHT / 2 )):
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            score1 += 1
            spawn_ball("LEFT")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    if ( ( paddle1_pos + paddle1_vel ) >= HALF_PAD_HEIGHT 
        and ( paddle1_pos + paddle1_vel) <= HEIGHT - HALF_PAD_HEIGHT ):
        paddle1_pos += paddle1_vel
    if ( ( paddle2_pos + paddle2_vel ) >= HALF_PAD_HEIGHT 
        and ( paddle2_pos + paddle2_vel) <= HEIGHT - HALF_PAD_HEIGHT ):
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line( [PAD_WIDTH / 2 ,  paddle1_pos + HALF_PAD_HEIGHT] ,
                      [PAD_WIDTH / 2 ,  paddle1_pos - HALF_PAD_HEIGHT] ,
                      PAD_WIDTH, "white" )
    canvas.draw_line( [WIDTH - ( PAD_WIDTH / 2 ) ,  paddle2_pos + HALF_PAD_HEIGHT] ,
                      [WIDTH - ( PAD_WIDTH / 2 ) ,  paddle2_pos - HALF_PAD_HEIGHT] ,
                      PAD_WIDTH, "white" )
    
    # draw scores
    canvas.draw_text(str(score1), [200, 100], 48, "white")
    canvas.draw_text(str(score2), [400, 100], 48, "white")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 5
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 5
        
                                    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("teal")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 150)


# start frame
new_game()
frame.start()
