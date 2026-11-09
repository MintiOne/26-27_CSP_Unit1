import turtle
from PIL import Image

import numpy as np
import os

import world
import brushes

t = turtle.Turtle()
screen = turtle.Screen()

tilesizex = 32
tilesizey = 32

screenX = 0
screenY = 0
mouse_x = 0
mouse_y = 0

turtle.tracer(0)

image_paths = "tiles"
png_files = [f for f in os.listdir(image_paths) if f.lower().endswith('.gif')]
for png_file in png_files:
    temp = Image.open(image_paths + "/" + png_file).convert('RGBA')
    temp = temp.resize((tilesizex,tilesizey))
    temp.save(image_paths + "/resize/" + png_file)
for img in png_files:
    screen.register_shape(image_paths + "/resize/" + img)

screen.screensize(32, 32)

def get_mouse_input(event):
    global screen
    global mouse_x, mouse_y
    mouse_x = event.x - screen.window_width() / 2
    mouse_y = screen.window_height() / 2 - event.y

canvas = turtle.getcanvas()
canvas.bind('<Motion>', get_mouse_input)

def draw_tile(x, y, path):
    global t
    global images
    global png_files
    global screenX
    global screenY
    t.up()
    t.goto(x-screenX, y-screenY)
    t.shape(path)
    t.stamp()
def draw_screen():
    global screen
    for x in range(len(world.tiles)):
        for y in range(len(world.tiles[x])):
            draw_tile(x*tilesizex, y*tilesizey, world.tiles[x][y])

def tile(name):
    global image_paths
    return image_paths + "/resize/" + name

def draw(brush):
    global screenX
    global screenY
    global mouse_x
    global mouse_y
    world.tiles[round((mouse_x+screenX)/tilesizex)][round((mouse_y+screenY)/tilesizey)] = tile(brush)

for y in range(16):
    world.tiles.append([])
    for x in range(16):
        world.tiles[y].append(tile("48_960.gif"))

def move_camera(x, y):
    global screenX
    global screenY
    screenX += x
    screenY += y

while True:
    screen.reset()
    screen.listen()
    screen.onkeypress(lambda: brushes.Land.cycle, "e")
    screen.onkeypress(lambda: draw(brushes.Land.brush), "1")
    screen.onkeypress(lambda: move_camera(0,10), "w")
    screen.onkeypress(lambda: move_camera(0,-10), "s")
    screen.onkeypress(lambda: move_camera(-10,0), "a")
    screen.onkeypress(lambda: move_camera(10,0), "d")
    draw_screen()
    screen.update()