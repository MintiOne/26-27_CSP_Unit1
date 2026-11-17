# a121_catch_a_turtle.py
#-----import statements-----
import turtle
import random as rand

#-----game configuration----
spot_color = 'red'
spot_size = 10
spot_shape = 'circle'

score = 0
font_setup = ("Arial", 20, "normal")

timer = 30

#-----initialize turtle-----
t = turtle.Turtle()
score_writer = turtle.Turtle()
timer_writer = turtle.Turtle()

wn = turtle.Screen()
t.shape(spot_shape)
t.shapesize(spot_size, spot_size)
t.color(spot_color)
t.penup()

screen_x = wn.window_width() // 2
screen_y = wn.window_height() // 2

score_writer.penup()
score_writer.goto(screen_x * -0.85, screen_y * 0.75)

timer_writer.penup()
timer_writer.goto(screen_x * 0.85, screen_y * 0.75)

#-----game functions--------

def spot_clicked(x, y):
    change_position()
def change_position():
    t.goto(rand.randint(-screen_x, screen_x), rand.randint(-screen_y, screen_y))
    update_score()
def update_score():
    global score
    score += 1

    score_writer.clear()
    score_writer.goto(screen_x * -0.85, screen_y * 0.75)
    score_writer.write(score, font=font_setup)

def countdown():
    global timer_writer
    global timer
    timer_writer.clear()
    if timer <= 0:
        timer_writer.write("Times Up!", font=font_setup)
    else:
        timer -= 1
        timer_writer.write(str(timer), font=font_setup)
        timer_writer.getscreen().ontimer(countdown, 1000)

#-----events----------------
t.onclick(spot_clicked)
wn.ontimer(countdown, 1000)
wn.mainloop()
t.penup()

wn.mainloop()