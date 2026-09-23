import turtle
from turtle import Screen
import numpy as np

class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def add(self, x=None, y=None, z=None, pos=None):
        temp = self
        breakpoint()
        if pos is None:
            temp.x += x
            temp.y += y
            temp.z += z
        else:
            temp.x += pos.x
            temp.y += pos.y
            temp.z += pos.z
        breakpoint()
        return temp

def dist(position1, position2):
    dist = np.cbrt((position1.x - position2.x)**2 + (position1.y - position2.y)**2+(position1.z - position2.z)**2)
    xy = np.sqrt((position1.x - position2.x) ** 2 + (position1.y - position2.y) ** 2)
    xz = np.sqrt((position1.x - position2.x) ** 2 + (position1.z - position2.z) ** 2)
    yz = np.sqrt((position1.z - position2.z) ** 2 + (position1.y - position2.y) ** 2)
    return dist, xy, xz, yz


class Rotation():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    @staticmethod
    def rotate(position, origin, rotation):
        temp, xy, xz, yz = dist(position, origin)

        temp = position

        temp.x = origin.x + np.cos(np.deg2rad(rotation.z) + np.atan2(temp.y - origin.y, temp.x - origin.x)) * xy
        temp.y = origin.y + np.sin(np.deg2rad(rotation.z) + np.atan2(temp.y - origin.y, temp.x - origin.x)) * xy

        temp.x = origin.x + np.cos(np.deg2rad(rotation.y) + np.atan2(temp.z - origin.z, temp.x - origin.x)) * xz
        temp.z = origin.z + np.sin(np.deg2rad(rotation.y) + np.atan2(temp.z - origin.z, temp.x - origin.x)) * xz

        temp.y = origin.y + np.sin(np.deg2rad(rotation.x) + np.atan2(temp.y - origin.y, temp.z - origin.z)) * yz
        temp.z = origin.z + np.cos(np.deg2rad(rotation.x) + np.atan2(temp.y - origin.y, temp.z - origin.z)) * yz

        return temp
    def add(self, rotation):
        temp = Rotation(self.x, self.y, self.z)
        temp.x += rotation.x
        temp.y += rotation.y
        temp.z += rotation.z
        return temp

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
    def calc_pos(self, cam, fc=30):
        temp_x = (self.position.x - cam.position.x)
        temp_y = (self.position.y - cam.position.y)
        temp_z = (self.position.z - cam.position.z)
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

class Plane:
    def __init__(self, position, rotation, width, height):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height
        self.points = []
        for i in range(4):
            self.points.append(point())
        breakpoint()
    def draw(self, cam):
        self.points[0].position = Position(self.position.x - self.width, self.position.y - self.height, self.position.z)
        self.points[1].position = Position(self.position.x + self.width, self.position.y - self.height, self.position.z)
        self.points[2].position = Position(self.position.x + self.width, self.position.y + self.height, self.position.z)
        self.points[3].position = Position(self.position.x - self.width, self.position.y + self.height, self.position.z)
        #self.points[0].position = Rotation.rotate(self.points[0].position, self.position, self.rotation)
        #self.points[1].position = Rotation.rotate(self.points[1].position, self.position, self.rotation)
        #self.points[2].position = Rotation.rotate(self.points[2].position, self.position, self.rotation)
        #self.points[3].position = Rotation.rotate(self.points[3].position, self.position, self.rotation)
        global t
        t.penup()
        for i in range(4):
            self.points[i].calc_pos(cam)
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
        self.planes = []
        self.plane1 = Plane(self.position.add(0, 0, depth), self.rotation.add(Rotation(0,0,0)), self.width, self.height)
        self.plane2 = Plane(self.position.add(0,width, 0), self.rotation.add(Rotation(0,0,0)), self.width, self.height)
        breakpoint()
    def draw(self, cam):
        self.plane1.draw(cam)
        self.plane2.draw(cam)



t = turtle.Pen()
screen = Screen()
turtle.Screen().bgcolor("white")

cam = camera(Position(0, 0, 30))

cube1 = cube(position=Position(0,0,10), rotation=Rotation(0,0,0), width=30, height=30, depth=30)

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
    cube1.draw(cam)