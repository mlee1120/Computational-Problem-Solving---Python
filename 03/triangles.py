"""
file: triangles.py
description: CSCI 603 hw3 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
author: Joseph Gawlowicz jg2348@RIT.EDU/joseph.gawlowicz@live.com
"""

import turtle


def start():
    """
    Sets window & turtle and calls draw_triangles_rec(length, depth)
    :pre: turtle down, lower left, facing east
    :post: turtle up, lower left, facing east
    :return: None
    """
    turtle.title("CSCI603 ml3406 jg2348 hw3 triangles.py")
    turtle.screensize(800, 750)
    turtle.tracer(0, 0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setposition(-100, -40)
    turtle.pendown()
    print("For depth=6 and length=200, the sum is " + str(draw_triangles_rec(200, 6)))
    turtle.penup()
    turtle.update()
    turtle.mainloop()


def draw_triangles_1(length):
    """
    Draws a red triangle.
    :param: length - length of 1 side of the triangle
    :pre: turtle down, lower left, facing east
    :post: turtle down, lower left, facing east
    :return: None
    """
    turtle.pencolor('red')
    turtle.forward(length)
    turtle.left(120)
    turtle.forward(length)
    turtle.left(120)
    turtle.forward(length)
    turtle.left(120)
    # a for loop as below can reduce code lines
    # for _ in range(3):
    #     turtle.forward(length)
    #     turtle.left(120)


def draw_triangles_2(length):
    for _ in range(3):
        turtle.pencolor('green')
        turtle.forward(length)
        draw_triangles_1(length / 2)
        turtle.left(120)


def draw_triangles_rec(length, depth):
    """
    Draw triangles recursively (length becomes half as depth decreases 1)
    :param length: length of 1 side of a triangle
    :param depth: controls the number of time of recursion
    :return: summation of all lengths of all triangles
    """
    color = "pink", "red", "green", "blue", "orange", "purple"
    summation = 0
    if depth == 0:
        return summation
    if depth > 0:
        for _ in range(3):
            turtle.pencolor(color[depth % len(color)])
            turtle.forward(length)
            summation += length
            summation += draw_triangles_rec(length / 2, depth - 1)
            turtle.left(120)
    return summation


# main conditional guard
# script execution/run
# the following condition checks whether we are
# running as a script, in which case run the test code.
# if the file is being imported, don't run the test code.
if __name__ == '__main__':
    start()
