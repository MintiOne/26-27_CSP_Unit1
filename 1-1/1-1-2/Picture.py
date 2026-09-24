import turtle
from turtle import Screen
import numpy as np
import copy

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
    def inverse(self):
        temp = Rotation(self.x, self.y, self.z)
        temp.x = 180-temp.x
        temp.y = 180-temp.y
        temp.z = 180-temp.z
        return temp

class camera():
    def __init__(self, position=Position(), rotation=Rotation()):
        self.position = Position(position.x, position.y, position.z)
        self.rotation = Rotation(rotation.x, rotation.y, rotation.z)
    def move(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
    def local_move(self, x, y, z):
        self.position = Rotation.rotate(self.position.add(x, y, z), self.position, self.rotation.inverse())

class Point():
    def __init__(self, position=Position()):
        if position is Position():
            self.position = position
        else:
            self.position = Position()
        self.processed_position = Position()
        self.proj_x = 0
        self.proj_y = 0
    def calc_pos(self, cam):
        self.processed_position = Position(self.position.x, self.position.y, self.position.z)
        self.processed_position = Rotation.rotate(self.position, cam.position, cam.rotation)
        self.processed_position.x -= cam.position.x
        self.processed_position.y -= cam.position.y
        self.processed_position.z -= cam.position.z
    def project(self):
        global fc
        if self.processed_position.z == 0:
            self.proj_x = 0
            self.proj_y = 0
        else:
            self.proj_x = (self.processed_position.x / self.processed_position.z) * fc
            self.proj_y = (self.processed_position.y / self.processed_position.z) * fc
        return self.proj_x, self.proj_y
    def draw(self):
        global t
        t.penup()
        t.goto(self.proj_x, self.proj_y)
        t.pendown()
        t.penup()

class triangle():
    def __init__(self, point1, point2, point3, size=1, color="black", fill_color="red"):
        if point1 is Position:
            self.point1 = point1
        else:
            self.point1 = Point(point1)

        if point2 is Position:
            self.point2 = point2
        else:
            self.point2 = Point(point2)

        if point3 is Position:
            self.point3 = point3
        else:
            self.point3 = Point(point3)
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

class Line:
    def __init__(self, point1, point2):
        self.abs_point1 = point1
        self.abs_point2 = point2
        self.point1 = Point(Position(point1.position.x, point1.position.y, point1.position.z))
        self.point2 = Point(Position(point2.position.x, point2.position.y, point2.position.z))
    def calc_pos(self, cam):
        self.abs_point1.calc_pos(cam)
        self.abs_point2.calc_pos(cam)
        self.point1 = copy.copy(self.abs_point1)
        self.point2 = copy.copy(self.abs_point2)

    def fix_clipping(self):
        global fov
        #xy clipping:
        slope = np.tan(np.deg2rad(fov/2))
        if self.point1.processed_position.z < (slope*self.point1.processed_position.x):
            slope1 = (self.point1.processed_position.z - self.point2.processed_position.z) / (self.point1.processed_position.x - self.point2.processed_position.x)
            intercept = self.point1.processed_position.z - (self.point1.processed_position.x * slope1)
            self.point1.processed_position.x = (-intercept)/(slope1-slope)
            self.point1.processed_position.z = intercept + (slope1*self.point1.processed_position.x)

        if self.point2.processed_position.z < (slope*self.point2.processed_position.x):
            slope1 = (self.point1.processed_position.z - self.point2.processed_position.z) / (self.point1.processed_position.x - self.point2.processed_position.x)
            intercept = self.point2.processed_position.z - (self.point2.processed_position.x * slope1)
            self.point2.processed_position.x = (-intercept)/(slope1-slope)
            self.point2.processed_position.z = intercept + (slope1*self.point2.processed_position.x)

        slope = np.tan(np.deg2rad(-fov / 2))

        if self.point1.processed_position.z < (slope * self.point1.processed_position.x):
            slope1 = (self.point1.processed_position.z - self.point2.processed_position.z) / (
                        self.point1.processed_position.x - self.point2.processed_position.x)
            intercept = self.point1.processed_position.z - (self.point1.processed_position.x * slope1)
            self.point1.processed_position.x = (-intercept) / (slope1 - slope)
            self.point1.processed_position.z = intercept + (slope1 * self.point1.processed_position.x)

        if self.point2.processed_position.z < (slope * self.point2.processed_position.x):
            slope1 = (self.point1.processed_position.z - self.point2.processed_position.z) / (
                        self.point1.processed_position.x - self.point2.processed_position.x)
            intercept = self.point2.processed_position.z - (self.point2.processed_position.x * slope1)
            self.point2.processed_position.x = (-intercept) / (slope1 - slope)
            self.point2.processed_position.z = intercept + (slope1 * self.point2.processed_position.x)

    def project(self):
        self.point1.project()
        self.point2.project()

    def draw(self):
        self.project()
        global t
        t.penup()
        t.goto(self.point1.proj_x, self.point1.proj_y)
        t.pendown()
        t.goto(self.point2.proj_x, self.point2.proj_y)
        t.penup()


class Plane:
    def __init__(self, position, rotation, width, height, style={"color": (0,0,0), "fill": None, "size":5}):
        self.position = Position(position.x, position.y, position.z)
        self.rotation = Rotation(rotation.x, rotation.y, rotation.z)
        self.style = style
        self.width = width
        self.height = height
        self.points = []
        self.lines = []
        for i in range(4):
            self.points.append(Point())
        for i in range(4):
            i2 = (i+1) % len(self.points)
            self.lines.append(Line(self.points[i], self.points[i2]))
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
        for line in self.lines:
            line.calc_pos(cam)
            line.fix_clipping()
        if self.style["fill"] is not None:
            t.fillcolor(self.style["fill"])
            t.pensize(0)
            t.begin_fill()
            for i in range(len(self.lines)):
                self.lines[i].project()
                if i == 0:
                    t.penup()
                t.goto(self.lines[i].point1.proj_x, self.lines[i].point1.proj_y)
                t.pendown()
                t.goto(self.lines[i].point2.proj_x, self.lines[i].point2.proj_y)
            t.goto(self.lines[0].point1.proj_x, self.lines[0].point1.proj_y)
            t.end_fill()
            t.penup()
        for line in self.lines:
            t.color(self.style["color"])
            t.pensize(self.style["size"])
            line.draw()

class cube():
    def __init__(self, position=Position(), rotation=Rotation(), width = 1, height = 1, depth = 1):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height
        self.depth = depth
        self.planes = []
        self.planes.append(Plane(self.position.add(0, 0, depth*0.5), self.rotation.add(Rotation(0,0,0)), self.width, self.height, style={"color": (0,0,0), "fill": (255,255,0), "size":5}))
        self.planes.append(Plane(self.position.add(0, 0, depth*-0.5), self.rotation.add(Rotation(0, 0, 0)), self.width, self.height, style={"color": (0,0,0), "fill": (255, 0,0), "size":5}))
        self.planes.append(Plane(self.position.add(width*-0.5, 0, 0), self.rotation.add(Rotation(0, 90, 0)), self.width, self.height, style={"color": (0,0,0), "fill": (255,0,255), "size":5}))
        self.planes.append(Plane(self.position.add(width*0.5, 0, 0), self.rotation.add(Rotation(0, 90, 0)), self.width,self.height, style={"color": (0,0,0), "fill": (0,255,0), "size":5}))
        self.planes.append(Plane(self.position.add(0, height*0.5, 0), self.rotation.add(Rotation(90, 0, 0)), self.width,self.height, style={"color": (0,0,0), "fill": (255,100,255), "size":5}))
        self.planes.append(Plane(self.position.add(0, height*-0.5, 0), self.rotation.add(Rotation(90, 0, 0)), self.width, self.height, style={"color": (0,0,0), "fill": (55,255,100), "size":5}))
    def draw(self, cam):
        for i in range(len(self.planes)):
            self.planes[i].draw(cam)

def get_mouse_pos(event):
    global mouse_x, mouse_y
    mouse_x = event.x - screen.window_width() / 2
    mouse_y = screen.window_height() / 2 - event.y

def cam_mouse_move(mouse_x, mouse_y, cam, sensitivity = 40):
    cam.rotation.y = mouse_x * sensitivity / 100
    #add code here for rotation based on current orientation

t = turtle.Pen()
turtle.colormode(255)
screen = Screen()
screen.setup(width=2000, height=1300)
canvas = screen.getcanvas()
canvas.bind('<Motion>', get_mouse_pos)
turtle.Screen().bgcolor("white")
turtle.tracer(0)

print(screen.window_width())

fov = 45
fc = screen.window_width()/(2*np.tan(fov/2))

mouse_x, mouse_y = 0,0

cam = camera(Position(0, 0, -30), Rotation(0,0,0))

cube1 = cube(position=Position(0,0,0), rotation=Rotation(0,0,0), width=20, height=20, depth=20)
#plane1 = Plane(Position(0,0,0),Rotation(0,90,0),8,8)

t.speed(0)

turtle.reset()
while True:
    screen.listen()
    screen.onkeypress(lambda: cam.local_move(0,0, 1), "w")
    screen.onkeypress(lambda: cam.local_move(0, 0, -1), "s")
    screen.onkeypress(lambda: cam.local_move(-1, 0, 0), "a")
    screen.onkeypress(lambda: cam.local_move(1, 0, 0), "d")
    cam_mouse_move(mouse_x, mouse_y, cam)
    t.reset()
    cube1.draw(cam)
    turtle.update()