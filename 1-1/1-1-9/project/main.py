import turtle
from PIL import Image

import numpy as np
import os

t = turtle.Turtle()

image_paths = "tiles"
png_files = [f for f in os.listdir(image_paths) if f.lower().endswith('.gif')]
for img in png_files:
    turtle.addshape(image_paths + "/" + img)

def draw_tile(x, y, tileID):
    global t
    global images
    t.up()
    t.goto(x, y)
    t.shape(png_files[tileID])

draw_tile(0, 0, 0)