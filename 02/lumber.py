"""
file: lumber.py
description: CSCI 603 hw2 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
author: Joseph Gawlowicz jg2348@RIT.EDU/joseph.gawlowicz@live.com
"""

import turtle
import hw2.yard
import random
import math

"""
:param a: LumberYard type from yard.py
"""

a = hw2.yard.LumberYard()


def start():
    """
    start() calls window_set() at the beginning to settle our yard.
    turtle.onscreenclick(a function with two arguments(x, y), default = 1 left click, False to replace a former binding)
    :pre: turtle at the center, turtle facing east, pen down
    :post: turtle facing east, pen up
    """
    window_set()
    turtle.onscreenclick(doclick, 1, False)
    turtle.mainloop()


def window_set():
    """
    window_set() settles every thing before Starting growing trees
    :param: screensize - screen width and height
    :param dline_x_po: x-postion of the starting point of the dividing line
    :param dline_y_pos: y-postion of the dividing line
    :param: word_x_pos - x-position of the left button
    :param: word_y_pos - y-position of both buttons
    :param: screensize - screen width and height
    :post: turtle facing east, pen up
    """
    print("Please don't click too fast.")
    print("Total length: ", end="")
    turtle.penup()
    turtle.hideturtle()
    turtle.speed(0)
    screensize = 800
    dline_x_pos = -1000
    dline_y_pos = -200
    word_x_pos = -250
    word_y_pos = -300
    turtle.screensize(screensize, screensize)
    turtle.setpos(dline_x_pos, dline_y_pos)
    turtle.pendown()
    turtle.forward(-2 * (dline_x_pos))
    turtle.penup()
    turtle.setpos(word_x_pos, word_y_pos)
    turtle.write("Harvest and sort", True, "center")
    turtle.setpos(-word_x_pos, word_y_pos)
    turtle.write("Harvest unsorted", True, "center")


def doclick(x, y):
    """
    React to user's clicks, whose positions depends the next step (grow trees or harvest)
    1. above the dividing line: grow a tree
    Every tree has random trunk height between 50 ~ 250, and all tree heights are recorded in a.
    (except that the top of the trunk should never be less than 50 pixels from the top of the window.)
    2. under the dividing line: harvest (right: unsorted; left: sorted)
    right button: list not sorted
    left button: list sorted (highest to shortest)
    turtle.exitonclick will override any other click responses previously specified.
    list.sort(reverse=True) (order in big to small)
    :param x: x-position of the current click
    :param y: y-position of the current click
    """
    if -200 <= y <= 350:
        turtle.setposition(x, y)
        trunk_height = random.randint(50, 250)
        if (y + trunk_height) > 350:
            trunk_height = int(350 - y)
        draw_trunk(trunk_height)
        a.addLog(trunk_height)
    elif y < -200:
        turtle.setposition(0, -200)
        turtle.color("salmon4")
        if x >= 0:
            turtle.clear()
            place_lumber(a.allLogs())
        else:
            turtle.clear()
            b = a.allLogs()
            b.sort(reverse=True)
            place_lumber(b)
        turtle.exitonclick()


def draw_trunk(trunk_height):
    """
    draw a tree trunk with a random height sent from doclick(x, y)
    :param trunk_height: trunk height of the tree which is about to be grown
    :pre: turtle at the position where is clicked, facing east, pen up
    :post: turtle at the top of the trunk, facing east, pen down
    """
    turtle.color("salmon4")
    turtle.left(90)
    turtle.pendown()
    turtle.forward(trunk_height)
    turtle.right(90)
    turtle.color("black")
    draw_leaves(random.randint(1, 3))


def draw_leaves(tree_type):
    """
    depend what type of trees to draw
    :param tree_type: type of the tree which is about to be grown
    :pre: turtle at the top of the trunk, facing east, pen down
    :post: turtle at the top of the trunk, facing east, pen up
    """
    tree_size = 50
    if tree_type == 1:
        draw_maple(tree_size)
        turtle.penup()
    elif tree_type == 2:
        draw_pine(tree_size)
        turtle.penup()
    else:
        draw_starfruit(2 * tree_size)
        turtle.penup()


def draw_maple(size):
    """
    draw a maple tree
    :pre: turtle at the top of the trunk, facing east, pen down
    :post: turtle at the top of the trunk, facing east, pen down
    """
    turtle.color("red")
    turtle.circle(size)
    turtle.color("black")


def draw_pine(size):
    """
    draw a pine tree
    :pre: turtle at the top of the trunk, facing east, pen down
    :post: turtle at the top of the trunk, facing east, pen down
    """
    turtle.color("green")
    turtle.forward(size)
    turtle.left(135)
    turtle.forward(size * math.sqrt(2))
    turtle.left(90)
    turtle.forward(size * math.sqrt(2))
    turtle.left(135)
    turtle.forward(size)
    turtle.color("black")


def draw_starfruit(size):
    """
    draw a starfruit tree
    :pre: turtle at the top of the trunk, facing east, pen down
    :post: turtle at the top of the trunk, facing east, pen down
    """
    turtle.color("yellow3")
    turtle.left(72)
    for _ in range(5):
        turtle.forward(size)
        turtle.left(144)
    turtle.right(72)
    turtle.color("black")


def place_lumber(b):
    """
    Draw all tree trunks in a pile and print the total trunk length.
    :param b: receive a unsorted or sorted list storing all trunk heights
    :pre: turtle at(0, y), where y >= dline_y_pos(-200), facing east, pen up
    :post: turtle at(0, y), where y >= dline_y_pos(-200), facing east, pen up
    """
    total_length = 0
    for i in range(len(b)):
        turtle.pendown()
        turtle.forward(b[i] / 2)
        turtle.left(90)
        turtle.forward(10)
        turtle.left(90)
        turtle.forward(b[i])
        turtle.left(90)
        turtle.forward(10)
        turtle.left(90)
        turtle.forward(b[i] / 2)
        turtle.penup()
        turtle.left(90)
        turtle.forward(10)
        turtle.right(90)
        total_length += b[i]
    print(total_length)


# main conditional guard
# script execution/run
# the following condition checks whether we are
# running as a script, in which case run the test code.
# if the file is being imported, don't run the test code.
if __name__ == '__main__':
    start()
