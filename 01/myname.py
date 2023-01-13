"""
file: myname.py
description: CSCI603 hw1
language: python3
author: Michael Lee  ml3406@RIT.EDU
"""

import turtle
from turtle import *


def preset(size, gap):
    """ Set the turtle's window according to the user's preferences.
    """
    screensize((8 * (size + gap) + 50), 250, "black")
    title("CSCI603 ml3406 hw1 myname.py")
    # Hide the turtle at the beginning before starting drawing.
    hideturtle()
    pensize(2)
    color("white")
    penup()
    backward((8 * (size + gap)) / 2)


def drawM(length, c):
    """ Draw a word M in the current direction.
        c determines whether the word M should be red or not.
        Call draw_line(length) if a line draw is required.
    """
    if c:
        color("red")
    left(90)
    pendown()
    draw_line(length)
    right(150)
    draw_line(length)
    left(120)
    draw_line(length)
    right(150)
    draw_line(length)
    penup()
    left(90)


def drawI(length, c):
    """ Draw a word I in the current direction.
        c determines whether the word I should be orange or not.
        Call draw_line(length) if a line draw is required.
    """
    if c:
        color("orange")
    pendown()
    draw_line(length / 2)
    left(90)
    draw_line(length)
    left(90)
    draw_line(length / 2)
    left(180)
    draw_line(length)
    left(180)
    draw_line(length / 2)
    left(90)
    draw_line(length)
    left(90)
    draw_line(length / 2)
    penup()


def drawK(length, c):
    """ Draw a word K in the current direction.
        c determines whether the word K should be yellow or not.
        Call draw_line(length) if a line draw is required.
    """
    if c:
        color("yellow")
    left(90)
    pendown()
    draw_line(length)
    right(180)
    draw_line(length / 2)
    left(120)
    draw_line(length)
    right(180)
    draw_line(length)
    left(120)
    draw_line(length)
    right(180)
    draw_line(length)
    left(120)
    draw_line(length / 2)
    penup()
    left(90)
    forward(length)


def drawO(length, c):
    """ Draw a word O in the current direction.
        c determines whether the word O should be green or not.
        Call draw_line(length) if a line draw is required.
    """
    if c:
        color("green")
    draw_line(length / 2)
    pendown()
    circle(length / 2)
    penup()
    forward(length / 2)


def drawL(length, c):
    """ Draw a word L in the current direction.
        c determines whether the word L should be blue or not.
        Call draw_line(length) if a line draw is required.
    """
    if c:
        color("blue")
    left(90)
    pendown()
    draw_line(length)
    right(180)
    draw_line(length)
    left(90)
    draw_line(length)
    penup()


def drawE(length, c):
    """ Draw a word E in the current direction.
        c determines whether the word E should be purple or not.
        Call draw_line(length) if a line draw is required.
    """
    if c:
        color("purple")
    left(90)
    pendown()
    draw_line(length)
    right(90)
    draw_line(length)
    right(180)
    draw_line(length)
    left(90)
    draw_line(length / 2)
    left(90)
    draw_line(2 * length / 3)
    right(180)
    draw_line(2 * length / 3)
    left(90)
    draw_line(length / 2)
    left(90)
    draw_line(length)
    penup()


def space(length):
    """ Leave a space in the current direction.
    """
    forward(length)


def drawgap(gap):
    """ Leave a gap in the current direction.
    """
    forward(gap)


def draw_line(length):
    """ Draw a line in the current direction.
    """
    forward(length)


def main():
    """
    main() function first asks the user to enter something for preferences,
    and then it calls set(size, gap) to set the window.
    After that, it calls several functions to accomplish drawing my family name.
    """

    size = int(input("Please enter an integer for the size of the words (100 is preferred): "))
    gap = int(input("Please enter an integer for the size of the gap (10 is preferred):"))
    # c determines if colorful words are applied or not according to user's answer.
    c = False
    determine = int(input("Do you wish to have colorful words? Enter 1 for yes or 0 for no: "))
    if determine == 1:
        c = True
    preset(size, gap)
    # Show the turtle when starting to draw.
    showturtle()
    drawM(size, c)
    drawgap(gap)
    drawI(size, c)
    drawgap(gap)
    drawK(size, c)
    drawgap(gap)
    drawO(size, c)
    drawgap(gap)
    space(size)
    drawgap(gap)
    drawL(size, c)
    drawgap(gap)
    drawE(size, c)
    drawgap(gap)
    drawE(size, c)
    # Hide the turtle when finishing drawing.
    hideturtle()
    input('Close the graphic window when done.')
    # mainloop() prevents the turtle's window to close.
    mainloop()


# # script execution/run
# the following condition checks whether we are
# running as a script, in which case run the test code.
# if the file is being imported, don't run the test code.
if __name__ == '__main__':
    main()
