import turtle
from turtle import Screen
import numpy as np

class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def add(self, x=None, y=None, z=None, pos=None):
        temp = Position(self.x, self.y, self.z)
        if pos is None:
            temp.x += x
            temp.y += y
            temp.z += z
        else:
            temp.x += pos.x
            temp.y += pos.y
            temp.z += pos.z
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
        temp = Position(position.x-origin.x, position.y-origin.y, position.z-origin.z)

        x = temp.x
        z = temp.z

        temp.x = x * np.cos(np.deg2rad(rotation.y)) - z * np.sin(np.deg2rad(rotation.y))
        temp.z = x * np.sin(np.deg2rad(rotation.y)) + z * np.cos(np.deg2rad(rotation.y))

        x = temp.x
        y = temp.y

        temp.x = x * np.cos(np.deg2rad(rotation.z)) - y * np.sin(np.deg2rad(rotation.z))
        temp.y = x * np.sin(np.deg2rad(rotation.z)) + y * np.cos(np.deg2rad(rotation.z))

        y = temp.y
        z = temp.z

        temp.y = y * np.cos(np.deg2rad(rotation.x)) - z * np.sin(np.deg2rad(rotation.x))
        temp.z = y * np.sin(np.deg2rad(rotation.x)) + z * np.cos(np.deg2rad(rotation.x))

        temp.x += origin.x
        temp.y += origin.y
        temp.z += origin.z

        return temp
    def add(self, rotation):
        temp = Rotation(self.x, self.y, self.z)
        temp.x += rotation.x
        temp.y += rotation.y
        temp.z += rotation.z
        return temp

class camera():
    def __init__(self, position=Position(), rotation=Rotation()):
        self.position = Position(position.x, position.y, position.z)
        self.rotation = Rotation(rotation.x, rotation.y, rotation.z)
    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z

class point():
    def __init__(self, position=Position()):
        if position is Position():
            self.position = position
        else:
            self.position = Position()
        self.proj_x = 0
        self.proj_y = 0
    def calc_pos(self, cam, fc=310):
        temp = Position(self.position.x, self.position.y, self.position.z)
        temp = Rotation.rotate(self.position, cam.position, cam.rotation)
        temp.x -= cam.position.x
        temp.y -= cam.position.y
        temp.z -= cam.position.z
        if temp.z == 0:
            self.proj_x = 0
            self.proj_y = 0
        else:
            self.proj_x = (temp.x / temp.z) * fc
            self.proj_y = (temp.y / temp.z) * fc
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
        self.position = Position(position.x, position.y, position.z)
        self.rotation = Rotation(rotation.x, rotation.y, rotation.z)
        self.width = width
        self.height = height
        self.points = []
        for i in range(4):
            self.points.append(point())
    def draw(self, cam):
        global screen
        self.points[0].position = Position(self.position.x - self.width/2, self.position.y - self.height/2, self.position.z)
        self.points[1].position = Position(self.position.x + self.width/2, self.position.y - self.height/2, self.position.z)
        self.points[2].position = Position(self.position.x + self.width/2, self.position.y + self.height/2, self.position.z)
        self.points[3].position = Position(self.position.x - self.width/2, self.position.y + self.height/2, self.position.z)
        self.points[0].position = Rotation.rotate(self.points[0].position, self.position, self.rotation)
        self.points[1].position = Rotation.rotate(self.points[1].position, self.position, self.rotation)
        self.points[2].position = Rotation.rotate(self.points[2].position, self.position, self.rotation)
        self.points[3].position = Rotation.rotate(self.points[3].position, self.position, self.rotation)
        global t
        t.penup()
        for i in range(4):
            i2 = (i+1) % len(self.points)
            self.points[i].calc_pos(cam)
            self.points[i2].calc_pos(cam)
            #clipping fixes
            if np.abs(self.points[i].proj_x) >= screen.window_width()/2:
                temp_slope = (self.points[i].proj_y - self.points[i2].proj_y)/(self.points[i].proj_x - self.points[i2].proj_x)
                temp_inter = self.points[i].proj_y - (temp_slope * self.points[i].proj_x)
                if self.points[i].proj_x > 0:
                    self.points[i].proj_x = screen.window_width()/2
                if self.points[i].proj_x < 0:
                    self.points[i].proj_x = -screen.window_width()/2
                self.points[i].proj_y = self.points[i].proj_x * temp_slope + temp_inter
            if np.abs(self.points[i].proj_y) >= screen.window_height()/2:
                temp_slope = (self.points[i].proj_x - self.points[i2].proj_x)/(self.points[i].proj_y - self.points[i2].proj_y)
                temp_inter = self.points[i].proj_x - (temp_slope * self.points[i].proj_y)
                if self.points[i].proj_y > 0:
                    self.points[i].proj_y = screen.window_height()/2
                if self.points[i].proj_y < 0:
                    self.points[i].proj_y = -screen.window_height()/2
                self.points[i].proj_x = self.points[i].proj_y * temp_slope + temp_inter
            if np.abs(self.points[i2].proj_x) >= screen.window_width()/2:
                temp_slope = (self.points[i].proj_y - self.points[i2].proj_y)/(self.points[i].proj_x - self.points[i2].proj_x)
                temp_inter = self.points[i2].proj_y - (temp_slope * self.points[i2].proj_x)
                if self.points[i2].proj_x > 0:
                    self.points[i2].proj_x = screen.window_width()/2
                if self.points[i2].proj_x < 0:
                    self.points[i2].proj_x = -screen.window_width()/2
                self.points[i2].proj_y = (self.points[i2].proj_x * temp_slope) + temp_inter
            if np.abs(self.points[i2].proj_y) >= screen.window_height()/2:
                temp_slope = (self.points[i].proj_x - self.points[i2].proj_x)/(self.points[i].proj_y - self.points[i2].proj_y)
                temp_inter = self.points[i2].proj_x - (temp_slope * self.points[i2].proj_y)
                if self.points[i2].proj_y > 0:
                    self.points[i2].proj_y = screen.window_height()/2
                if self.points[i2].proj_y < 0:
                    self.points[i2].proj_y = -screen.window_height()/2
                self.points[i2].proj_x = self.points[i2].proj_y * temp_slope + temp_inter
            t.penup()
            t.goto(self.points[i].proj_x, self.points[i].proj_y)
            t.pendown()
            t.goto(self.points[i2].proj_x, self.points[i2].proj_y)
            t.penup()

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
        self.planes.append(Plane(self.position.add(0, 0, depth*0.5), self.rotation.add(Rotation(0,0,0)), self.width, self.height))
        self.planes.append(Plane(self.position.add(0, 0, depth*-0.5), self.rotation.add(Rotation(0, 0, 0)), self.width, self.height))
        self.planes.append(Plane(self.position.add(width*-0.5, 0, 0), self.rotation.add(Rotation(0, 90, 0)), self.width, self.height))
        self.planes.append(Plane(self.position.add(width*0.5, 0, 0), self.rotation.add(Rotation(0, 90, 0)), self.width,self.height))
        self.planes.append(Plane(self.position.add(0, height*0.5, 0), self.rotation.add(Rotation(90, 0, 0)), self.width,self.height))
        self.planes.append(Plane(self.position.add(0, height*-0.5, 0), self.rotation.add(Rotation(90, 0, 0)), self.width, self.height))
    def draw(self, cam):
        for i in range(len(self.planes)):
            self.planes[i].draw(cam)

def get_mouse_pos(event):
    global mouse_x, mouse_y
    mouse_x = event.x - screen.window_width() / 2
    mouse_y = screen.window_height() / 2 - event.y
    print(mouse_x, mouse_y)

def cam_mouse_move(mouse_x, mouse_y, cam, sensitivity = 40):
    cam.rotation.y = mouse_x * sensitivity / 100
    #add code here for rotation based on current orientation

t = turtle.Pen()
screen = Screen()
screen.setup(width=1000, height=1000)
canvas = screen.getcanvas()
canvas.bind('<Motion>', get_mouse_pos)
turtle.Screen().bgcolor("white")
turtle.tracer(0)

mouse_x, mouse_y = 0,0

cam = camera(Position(0, 0, 30), Rotation(0,0,0))

cube1 = cube(position=Position(0,0,0), rotation=Rotation(0,0,0), width=15, height=20, depth=32)
#plane1 = Plane(Position(0,0,0),Rotation(0,90,0),8,8)

t.speed(0)

turtle.reset()
while True:
    screen.listen()
    screen.onkeypress(lambda: cam.move(-1,0, 0), "Right")
    screen.onkeypress(lambda: cam.move(1, 0, 0), "Left")
    screen.onkeypress(lambda: cam.move(0, -1, 0), "Up")
    screen.onkeypress(lambda: cam.move(0, 1, 0), "Down")
    cam_mouse_move(mouse_x, mouse_y, cam)
    t.reset()
    cube1.draw(cam)
    turtle.update()