import turtle
from turtle import Screen
import numpy as np

class Position():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Rotation():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class camera():
    def __init__(self, position=Position(), rotation=Rotation()):
        self.position = Position()
        self.rotation = Rotation()
    def move(self, x, y):
        self.position.x += x
        self.position.y += y

class point():
    def __init__(self, position):
        self.position = position
        self.proj_x = 0
        self.proj_y = 0
    def calc_pos(self, cam, fc=5):
        temp_x = (self.position.x - cam.position.x)
        temp_y = (self.position.y - cam.position.y)
        temp_z = (self.position.z - cam.position.z)
        temp_dist = np.sqrt((temp_x ** 2) + (temp_y ** 2))
        temp_angle = np.arctan2(temp_y, temp_x)
        temp_x_2 = np.cos(cam.rotation.z+temp_angle)*temp_dist
        temp_y_2 = np.sin(cam.rotation.z + temp_angle) * temp_dist
        if temp_z != 0:
            print(temp_z)
            self.proj_x = (temp_x / temp_z) * fc
            self.proj_y = (temp_y / temp_z) * fc
        else:
            self.proj_x = 0
            self.proj_y = 0
        return self.proj_x, self.proj_y
    def draw(self):
        global t
        t.penup()
        t.goto(self.proj_x, self.proj_y)
        t.pendown()
        t.penup()

class line():
    def __init__(self, point1, point2, size=1, color="black"):
        self.point1 = point1
        self.point2 = point2
        self.size = size
        self.color = color
    def draw(self, cam):
        global t
        self.point1.calc_pos(cam)
        self.point2.calc_pos(cam)
        t.penup()
        t.color(self.color)
        t.pensize(self.size)
        t.goto(self.point1.proj_x, self.point1.proj_y)
        t.pendown()
        t.goto(self.point2.proj_x, self.point2.proj_y)
        t.penup()

class triangle():
    def __init__(self, point1, point2, point3, size=1, color="black", fill_color="red"):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.size = size
        self.color = color
        self.fill_color = fill_color
    def draw(self, cam):
        print(cam.position.x)
        self.point1.calc_pos(cam)
        self.point2.calc_pos(cam)
        self.point3.calc_pos(cam)
        t.penup()
        t.color(self.color)
        t.pensize(self.size)
        t.fillcolor(self.fill_color)
        t.begin_fill()
        t.goto(self.point1.proj_x, self.point1.proj_y)
        t.pendown()
        t.goto(self.point2.proj_x, self.point2.proj_y)
        t.goto(self.point3.proj_x, self.point3.proj_y)
        t.goto(self.point1.proj_x, self.point1.proj_y)
        t.penup()
        t.end_fill()

t = turtle.Pen()
screen = Screen()
turtle.Screen().bgcolor("white")

cam = camera(Position(0, 0, 0))

p1 = point(Position(10,10,1))
p2 = point(Position(10,20,1))
p3 = point(Position(20,20,1))
p4 = point(Position(20,10,1))
p5 = point(Position(10,10,11))
p6 = point(Position(10,20,11))
p7 = point(Position(20,20,11))
p8 = point(Position(20,10,11))
tri = triangle(p1, p2, p3, size=10, fill_color="white")
tri2 = triangle(p1, p4, p3, size=10, fill_color="white")
tri3 = triangle(p1, p4, p5, size=10, fill_color="white")
tri4 = triangle(p1, p4, p8, size=10, fill_color="white")
tri5 = triangle(p1, p2, p5, size=10, fill_color="white")
tri6 = triangle(p1, p2, p6, size=10, fill_color="white")

t.speed(0)

turtle.reset()
while True:
    screen.listen()
    screen.onkeypress(lambda: cam.move(1,0), "Right")
    t.reset()
    screen.update()
    tri.draw(cam)
    tri2.draw(cam)
    tri3.draw(cam)
    tri4.draw(cam)
    tri5.draw(cam)
    tri6.draw(cam)