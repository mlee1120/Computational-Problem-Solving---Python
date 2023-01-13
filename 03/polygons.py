"""
file: polygons.py
description: CSCI 603 hw3 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
author: Joseph Gawlowicz jg2348@RIT.EDU/joseph.gawlowicz@live.com
"""

import sys
import math
import random
import turtle

# .../polygons.py 3~8 [fill|unfill]

if 3 > int(sys.argv[1]) or int(sys.argv[1]) > 8 or len(sys.argv) != 3:
    print("$ python3 polygons.py #_sides [fill|unfill]")
    assert (3 <= int(sys.argv[1]) <= 8)
    assert (sys.argv[2])
for i in range(len(sys.argv)):
    print(sys.argv[i], end=" ")

# "constants" for random angles that the turtle rotates before and after recursive calls
ANGLE = random.randint(10, 350), random.randint(10, 350), random.randint(10, 350), random.randint(10, 350), \
        random.randint(10, 350)

# "constants" for the available colors
ALL_COLOR = "red", "orange", "yellow", "green", "blue", "purple", "black", "pink", "cyan", "aquamarine", "magenta", \
            "green yellow", "firebrick", "bisque"

# "constants" for the colors used on regular polygons
COLOR = ALL_COLOR[random.randint(0, 13)], ALL_COLOR[random.randint(0, 13)], ALL_COLOR[random.randint(0, 13)], ALL_COLOR[
    random.randint(0, 13)], ALL_COLOR[random.randint(0, 13)]

# window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 750

# pen sizes to use for filled and unfilled polygons
FILL_PEN_WIDTH = 1
UNFILL_PEN_WIDTH = 3

# length of 1 side of the first polygon
SIDE_LENGTH = 130

# FILL - determinator of filling polygons or not
if sys.argv[2] == "fill":
    FILL = True
else:
    FILL = False


def start():
    """
    Calls preset() to set window & turtle and calls draw_polygons_rec to draw polygons.
    :pre: turtle at the center, turtle facing east, pen down
    :post: First drawn regular polygon at the center, turtle facing east, pen up
    """
    preset()
    print("\nSum: " + str(int(draw_polygons_rec(SIDE_LENGTH, int(sys.argv[1])))))
    turtle.penup()
    turtle.update()
    turtle.mainloop()


def preset():
    """
    set window and turtle
    :pre: turtle at the center, turtle facing east, pen down
    :post: First regular polygon to be drawn at the center, turtle facing east, pen down
    """
    turtle.title("CSCI603 ml3406 jg2348 hw3 polygons.py - Beauty of Randomness")
    turtle.screensize(WINDOW_WIDTH, WINDOW_HEIGHT)
    #turtle.bgcolor("black")
    # skip drawing animation
    turtle.tracer(0, 0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(-(WINDOW_WIDTH / 2) + 10, -(WINDOW_HEIGHT / 2) + 10)
    turtle.write("Sides: " + sys.argv[1] + ", Fill:" + str(FILL), True, "center")
    # set turtle to the position that the first polygon to be drawn will be at the center
    turtle.setposition((-SIDE_LENGTH / 2),
                       (-SIDE_LENGTH / 2) * math.tan(((180 - 360 / int(sys.argv[1])) / 2) * 2 * math.pi / 360))
    turtle.pendown()
    if FILL:
        turtle.pensize(FILL_PEN_WIDTH)
    else:
        turtle.pensize(UNFILL_PEN_WIDTH)


def draw_polygons_rec(length, sides):
    """
    Draw polygons recursively (length becomes half as sides decreases 1).
    The result is different evert time because we apply random int when initializing ANGLE and COLOR
    sys.argv[2] determines to fill the polygons or not
    :param length: length of 1 side of a polygon
    :param sides: number of sides of a polygon
    :return: summation - summation of all lengths of all polygons
    """
    summation = 0
    # if fill, draws one polygon first for filling the polygon and executes the recursive steps later
    if FILL:
        turtle.begin_fill()
        for _ in range(sides):
            turtle.pencolor(COLOR[sides - 4])
            turtle.fillcolor(COLOR[sides - 4])
            turtle.forward(length)
            turtle.left(360 / sides)
        turtle.end_fill()
    for _ in range(sides):
        turtle.pencolor(COLOR[sides - 4])
        turtle.forward(length)
        summation += length
        turtle.left(360 / sides)
        if sides > 3:
            turtle.right(ANGLE[sides - 4])
            summation += draw_polygons_rec(length / 2, sides - 1)
            turtle.left(ANGLE[sides - 4])
    return summation


# main conditional guard
# script execution/run
# the following condition checks whether we are
# running as a script, in which case run the test code.
# if the file is being imported, don't run the test code.
if __name__ == "__main__":
    start()
