# CODE TO ADD
#   a116_buggy_image.py
import turtle as trtl
# instead of a descriptive name of the turtle such as painter,
# a less useful variable name x is used
painter = trtl.Turtle()
painter.pensize(40)

#Make spider body
painter.circle(20)

painter.pensize(5)

legs = 8
length_of_legs = 70
leg_angle = 180 / legs

n = 0

for i in range(legs):
  painter.goto(0,20)
  if i > 3:
      side = -1
  else:
      side = 1
  offset = legs/2%2
  if offset == 0:
      offset = (legs/4+0.5)*leg_angle
  print(offset)
  painter.setheading((leg_angle*(i%4)+offset)*side+90)
  painter.forward(length_of_legs)

painter.hideturtle()
wn = trtl.Screen()
wn.mainloop()