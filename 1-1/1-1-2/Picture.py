import turtle
import numpy as np

class Position():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Rotation():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class camera():
    def __init__(self):
        self.position = Position()
        self.rotation = Rotation()

class point():
    def __init__(self):
        self.position = Position()
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

t = turtle.Pen()
turtle.Screen().bgcolor("white")

p = point()
p.position = Position(2, 3, 1)
cam = camera()
p.calc_pos(cam)
t.goto(p.proj_x, p.proj_y)

turtle.Screen().mainloop()