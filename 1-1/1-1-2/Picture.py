import turtle
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
        self.proj_x = (temp_x_2 / self.position.z) * fc
        self.proj_y = (temp_y_2 / self.position.z) * fc
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
turtle.Screen().bgcolor("white")

cam = camera(Position(0, 0, 1))

p1 = point(Position(-5,-5,0.01))
p2 = point(Position(-5,5,0.01))
p3 = point(Position(5,5,0.01))
p4 = point(Position(5,-5,0.01))
tri = triangle(p1, p2, p3, size=2, fill_color="white")
tri2 = triangle(p1, p4, p3, size=2, fill_color="white")
tri.draw(cam)
tri2.draw(cam)

turtle.Screen().mainloop()