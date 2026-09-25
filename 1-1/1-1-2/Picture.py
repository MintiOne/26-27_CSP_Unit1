import turtle
from turtle import Screen
import numpy as np
import copy
from PIL import Image, ImageTk

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

    def matrix(self):
        x = np.deg2rad(self.x)
        y = np.deg2rad(self.y)
        z = np.deg2rad(self.z)

        cx, sx = np.cos(x), np.sin(x)
        cy, sy = np.cos(y), np.sin(y)
        cz, sz = np.cos(z), np.sin(z)

        Rx = np.array([
            [1, 0, 0],
            [0, cx, -sx],
            [0, sx, cx]
        ])

        Rz = np.array([
            [cz, -sz, 0],
            [sz, cz, 0],
            [0, 0, 1]
        ])

        Ry = np.array([
            [cy, 0, sy],
            [0, 1, 0],
            [-sy, 0, cy]
        ])

        return Rx @ Rz @ Ry

    def add(self, rotation):
        # Convert both rotations to matrices
        a = self.matrix()
        b = rotation.matrix()

        m = a @ b

        z = np.arcsin(np.clip(-m[0, 1], -1.0, 1.0))

        cz = np.cos(z)

        if abs(cz) > 1e-6:
            y = np.arctan2(m[0, 2], m[0, 0])
            x = np.arctan2(m[2, 1], m[1, 1])
        else:
            y = 0
            x = np.arctan2(-m[1, 2], m[1, 1])

        return Rotation(
            np.rad2deg(x),
            np.rad2deg(y),
            np.rad2deg(z)
        )
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
        self.position = Rotation.rotate(self.position.add(x, y, z), self.position, self.rotation)

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
        self.processed_position = Rotation.rotate(self.position, cam.position, cam.rotation.inverse())
        self.processed_position.x -= cam.position.x
        self.processed_position.y -= cam.position.y
        self.processed_position.z -= cam.position.z
    def project(self):
        global fc
        if self.processed_position.z == 0:
            print("yea")
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

def intersect_fov(p1, p2, slope):
    p1 = p1.processed_position
    p2 = p2.processed_position
    dx = p2.x-p1.x
    dz = p2.z-p1.z
    t = (slope*p1.z-p1.x)/(dx-slope*dz)
    if t > 1 or t < 0:
        print("error!")
    return p1.x+t*dx, p1.z+t*dz

class Line:
    def __init__(self, point1, point2):
        self.abs_point1 = point1
        self.abs_point2 = point2
        self.point1 = Point(Position(point1.position.x, point1.position.y, point1.position.z))
        self.point2 = Point(Position(point2.position.x, point2.position.y, point2.position.z))
        self.point1_clipped = Point(Position(point1.position.x, point1.position.y, point1.position.z))
        self.point2_clipped = Point(Position(point2.position.x, point2.position.y, point2.position.z))
    def calc_pos(self, cam):
        self.abs_point1.calc_pos(cam)
        self.abs_point2.calc_pos(cam)
        self.point1 = copy.deepcopy(self.abs_point1)
        self.point2 = copy.deepcopy(self.abs_point2)
        self.point1_clipped = copy.deepcopy(self.abs_point1.processed_position)
        self.point2_clipped = copy.deepcopy(self.abs_point2.processed_position)
    def fix_clipping(self):
        global fov
        #Left Right Clipping
        slope = np.tan(np.deg2rad(fov/2))
        self.abs_point1.calc_pos(cam)
        self.abs_point2.calc_pos(cam)
        self.point1_clipped = copy.deepcopy(self.abs_point1.processed_position)
        self.point2_clipped = copy.deepcopy(self.abs_point2.processed_position)

        d1 = self.point1_clipped.x - slope * self.point1_clipped.z
        d2 = self.point2_clipped.x - slope * self.point2_clipped.z

        #Right Side

        if d1 > 0 and d2 > 0:
            #both outside
            return False
        elif d1 > 0:
            t = -d1 / (d2 - d1)
            self.point1_clipped.x = self.point1_clipped.x + t * (self.point2_clipped.x - self.point1_clipped.x)
            self.point1_clipped.z = self.point1_clipped.z + t * (self.point2_clipped.z - self.point1_clipped.z)
            self.point1_clipped.y = self.point1_clipped.y + t * (self.point2_clipped.y - self.point1_clipped.y)
        elif d2 > 0:
            t = -d1 / (d2 - d1)
            self.point1_clipped.x = self.point1_clipped.x + t * (self.point2_clipped.x - self.point1_clipped.x)
            self.point1_clipped.z = self.point1_clipped.z + t * (self.point2_clipped.z - self.point1_clipped.z)
            self.point1_clipped.y = self.point1_clipped.y + t * (self.point2_clipped.y - self.point1_clipped.y)

        self.point1.processed_position = self.point1_clipped
        self.point2.processed_position = self.point2_clipped
        self.point1_clipped = copy.deepcopy(self.point1.processed_position)
        self.point2_clipped = copy.deepcopy(self.point2.processed_position)

        d1 = self.point1_clipped.x + slope * self.point1_clipped.z
        d2 = self.point2_clipped.x + slope * self.point2_clipped.z

        if d1 < 0 and d2 < 0:
            print("yea")
            # both outside
            return False
        elif d1 < 0:
            t = -d1 / (d2 - d1)
            self.point1_clipped.x = self.point1_clipped.x + t * (self.point2_clipped.x - self.point1_clipped.x)
            self.point1_clipped.z = self.point1_clipped.z + t * (self.point2_clipped.z - self.point1_clipped.z)
            self.point1_clipped.y = self.point1_clipped.y + t * (self.point2_clipped.y - self.point1_clipped.y)
        elif d2 < 0:
            t = -d1 / (d2 - d1)
            self.point1_clipped.x = self.point1_clipped.x + t * (self.point2_clipped.x - self.point1_clipped.x)
            self.point1_clipped.z = self.point1_clipped.z + t * (self.point2_clipped.z - self.point1_clipped.z)
            self.point1_clipped.y = self.point1_clipped.y + t * (self.point2_clipped.y - self.point1_clipped.y)

        self.point1.processed_position = self.point1_clipped
        self.point2.processed_position = self.point2_clipped
        self.point1_clipped = copy.deepcopy(self.point1.processed_position)
        self.point2_clipped = copy.deepcopy(self.point2.processed_position)

        return True

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
        global models
        models.append(self)
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
        temp = []
        t.penup()
        for line in self.lines:
            line.calc_pos(cam)
            temp.append(line.fix_clipping())
        if self.style["fill"] is not None and any(temp):
            t.fillcolor(self.style["fill"])
            t.pensize(5)
            t.begin_fill()

            first = True

            for i in range(len(self.lines)):
                if temp[i]:
                    self.lines[i].project()

                    if first:
                        t.penup()
                        t.goto(self.lines[i].point1.proj_x, self.lines[i].point1.proj_y)
                        t.pendown()
                        first = False
                    else:
                        t.goto(self.lines[i].point1.proj_x, self.lines[i].point1.proj_y)
                    t.goto(self.lines[i].point2.proj_x, self.lines[i].point2.proj_y)

            for i in range(len(self.lines)):
                if temp[i] is True:
                    t.goto(self.lines[i].point1.proj_x, self.lines[i].point1.proj_y)
                    break
            t.end_fill()
            t.penup()
        i = 0
        for line in self.lines:
            if temp[i] is True:
                t.color(self.style["color"])
                t.pensize(self.style["size"])
                line.draw()
            i+=1

class cube():
    def __init__(self, position=Position(), rotation=Rotation(), width = 1, height = 1, depth = 1):
        self.position = position
        self.rotation = rotation
        self.width = width
        self.height = height
        self.depth = depth
        self.planes = []
        self.planes.append(Plane(Rotation.rotate(self.position.add(0, 0, depth*0.5), self.position, self.rotation), self.rotation.add(Rotation(0,0,0)), self.width, self.height, style={"color": (0,0,0), "fill": (255,255,0), "size":5}))
        self.planes.append(Plane(Rotation.rotate(self.position.add(0, 0, depth*-0.5), self.position, self.rotation), self.rotation.add(Rotation(0, 0, 0)), self.width, self.height, style={"color": (0,0,0), "fill": (255, 0,0), "size":5}))
        self.planes.append(Plane(Rotation.rotate(self.position.add(width*-0.5, 0, 0), self.position, self.rotation), self.rotation.add(Rotation(0, 90, 0)), self.depth, self.height, style={"color": (0,0,0), "fill": (255,0,255), "size":5}))
        self.planes.append(Plane(Rotation.rotate(self.position.add(width*0.5, 0, 0), self.position, self.rotation), self.rotation.add(Rotation(0, 90, 0)), self.depth,self.height, style={"color": (0,0,0), "fill": (0,255,0), "size":5}))
        self.planes.append(Plane(Rotation.rotate(self.position.add(0, height*0.5, 0), self.position, self.rotation), self.rotation.add(Rotation(90, 0, 0)), self.width,self.depth, style={"color": (0,0,0), "fill": (255,150,255), "size":5}))
        self.planes.append(Plane(Rotation.rotate(self.position.add(0, height *-0.5, 0), self.position, self.rotation), self.rotation.add(Rotation(90, 0, 0)), self.width, self.depth, style={"color": (0,0,0), "fill": (55,70,100), "size":5}))

    def draw(self, cam):
        for i in range(len(self.planes)):
            self.planes[i].draw(cam)

class Image_plane():
    def __init__(self, image_file, size_x, size_y):
        global screen
        self.origin = Point()
        self.image_file = image_file
        self.size_x = size_x
        self.size_y = size_y
        self.cache_key = f"{self.image_file}_{int(self.size_x)}x{int(self.size_y)}"
        image_file = Image.open(self.image_file)
        image_file = image_file.convert("RGBA")
        resized_image = image_file.resize((max(1, int(self.size_x)), max(1, int(self.size_y))))
        self.tk_img = ImageTk.PhotoImage(resized_image)
    def draw(self, cam):
        global t
        global image_cache
        global screen
        self.origin.calc_pos(cam)
        self.origin.project()

        screen._shapes[self.cache_key] = turtle.Shape("image", self.tk_img)

        t.penup()
        t.goto(self.origin.proj_x, self.origin.proj_y)
        t.shape(self.cache_key)



def get_mouse_pos(event):
    global mouse_x, mouse_y
    mouse_x = event.x - screen.window_width() / 2
    mouse_y = screen.window_height() / 2 - event.y

def cam_mouse_move(mouse_x, mouse_y, cam, sensitivity = 40):
    global prev_mouse_x
    global prev_mouse_y
    dx = mouse_x - prev_mouse_x
    dy = mouse_y - prev_mouse_y
    cam.rotation.y += -dx * sensitivity / 250
    cam.rotation.x += -dy * sensitivity / 200
    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y
    #add code here for rotation based on current orientation

t = turtle.Pen()
turtle.colormode(255)
screen = Screen()
screen.setup(width=2000, height=1300)
canvas = screen.getcanvas()
canvas.bind('<Motion>', get_mouse_pos)
turtle.Screen().bgcolor("white")
turtle.tracer(0)

fov = 45
fc = screen.window_width()/(2*np.tan(np.deg2rad(fov/2)))

mouse_x, mouse_y = 0,0
prev_mouse_x, prev_mouse_y = 0,0

cam = camera(Position(0, 0, -100), Rotation(0,0,0))


image_cache = {}

models = []
values = []

cube1 = cube(position=Position(30,0,0), rotation=Rotation(0,0,0), width=3, height=40, depth=100)
cube2 = cube(position=Position(-30,0,0), rotation=Rotation(0,0,0), width=3, height=40, depth=100)

earth = Image_plane("images/earth.gif", 100, 100)
earth.origin.position = Position(0,0,30)

t.speed(0)

turtle.reset()
while True:
    screen.listen()
    screen.onkeypress(lambda: cam.local_move(0,0, 1), "w")
    screen.onkeypress(lambda: cam.local_move(0, 0, -1), "s")
    screen.onkeypress(lambda: cam.local_move(-1, 0, 0), "a")
    screen.onkeypress(lambda: cam.local_move(1, 0, 0), "d")
    screen.onkeypress(lambda: cam.local_move(0, -1, 0), "q")
    screen.onkeypress(lambda: cam.local_move(0, 1, 0), "e")
    cam_mouse_move(mouse_x, mouse_y, cam)
    #maybe make it sort the list as it appends?
    values = []
    for i in range(len(models)):
        values.append(dist(Rotation.rotate(models[i].position, cam.position, cam.rotation), cam.position))
    models = [model for _, model in sorted(zip(values, models), key=lambda pair: pair[0], reverse=True)]
    for model in models:
        model.draw(cam)
    earth.draw(cam)
    turtle.update()
    t.reset()