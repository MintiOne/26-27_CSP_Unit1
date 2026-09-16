import turtle
from turtle import Screen
import numpy as np

class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def add(self, x=None, y=None, z=None, pos=None):
        if pos is None:
            self.x += x
            self.y += y
            self.z += z
        else:
            self.x += pos.x
            self.y += pos.y
            self.z += pos.z
        return self


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
    def __init__(self, position=Position()):
        if position is Position():
            self.position = position
        else:
            self.position = Position()
        self.proj_x = 0
        self.proj_y = 0
    def calc_pos(self, cam, fc=60):
        temp_x = (self.position.x - cam.position.x)
        temp_y = (self.position.y - cam.position.y)
        temp_z = (self.position.z - cam.position.z)
        temp_dist = np.sqrt((temp_x ** 2) + (temp_y ** 2))
        #temp_angle = np.arctan2(temp_y, temp_x)
        #temp_x_2 = np.cos(cam.rotation.z+temp_angle)*temp_dist
        #temp_y_2 = np.sin(cam.rotation.z + temp_angle) * temp_dist
        if temp_z == 0:
            self.proj_x = 0
            self.proj_y = 0
        else:
            self.proj_x = (temp_x / temp_z) * fc
            self.proj_y = (temp_y / temp_z) * fc
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
        if point1 is Position:
            self.point1 = point1
        else:
            self.point1 = point(point1)

        if point2 is Position:
            self.point2 = point2
        else:
            self.point2 = point(point2)

        if point3 is Position:
            self.point3 = point3
        else:
            self.point3 = point(point3)
        self.size = size
        self.color = color
        self.fill_color = fill_color
    def draw(self, cam):
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

class plane:
    def __init__(self, position, rotation, width, height):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height
        self.points = []
        for i in range(4):
            self.points.append(point())
    def draw(self, cam):
        global t
        for i in range(4):
            self.points[i].calc_pos()
            t.goto(self.points[i].proj_x, self.points[i].proj_y)
            t.pendown()
        t.goto(self.points[0].proj_x, self.points[0].proj_y)
        t.penup()

class cube():
    def __init__(self, position=Position(), rotation=Rotation(), width = 1, height = 1, depth = 1):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height
        self.depth = depth
        triangles = []
        triangles.append(triangle(Position(self.position.x - width), Position(self.position.y - height), Position(self.position.z - depth)))



t = turtle.Pen()
screen = Screen()
turtle.Screen().bgcolor("white")

cam = camera(Position(0, 0, 30))

p1 = point(Position(-1,-1,1))
p2 = point(Position(1,-1,1))
p3 = point(Position(1,1,1))
p4 = point(Position(-1,1,1))
p5 = point(Position(-1,-1,2))
p6 = point(Position(1,-1,2))
p7 = point(Position(1,1,2))
p8 = point(Position(-1,1,2))
tri = triangle(p1, p2, p3, size=10, fill_color="white")
tri2 = triangle(p1, p4, p3, size=10, fill_color="white")
tri3 = triangle(p5, p6, p7, size=10, fill_color="white")
tri4 = triangle(p5, p8, p7, size=10, fill_color="white")
tri5 = triangle(p2, p3, p6, size=10, fill_color="white")
tri6 = triangle(p6, p3, p7, size=10, fill_color="white")
tri7 = triangle(p4, p3, p7, size=10, fill_color="white")
tri8 = triangle(p8, p3, p7, size=10, fill_color="white")

t.speed(0)

turtle.reset()
while True:
    screen.listen()
    screen.onkeypress(lambda: cam.move(1,0), "Right")
    screen.onkeypress(lambda: cam.move(-1, 0), "Left")
    screen.onkeypress(lambda: cam.move(0, 1), "Up")
    screen.onkeypress(lambda: cam.move(0, -1), "Down")
    t.reset()
    screen.update()
    tri.draw(cam)
    tri2.draw(cam)
    tri3.draw(cam)
    tri4.draw(cam)
    tri5.draw(cam)
    tri6.draw(cam)
    tri7.draw(cam)
    tri8.draw(cam)