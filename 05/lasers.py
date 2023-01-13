"""
file: lasers.py
description: CSCI 603 hw5 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
author: Joseph Gawlowicz jg2348@RIT.EDU/joseph.gawlowicz@live.com
"""

import sys
from MergeSort import msort
import os


def start():
    """
    Prompts for a ﬁle name, reads in the grid data, prompts for the number of lasers to place,
    and displays all lasers' scores, positions, and orientations.
    """
    # the 2D list storing the grid data
    grid = readfile(ask_file_name())
    # the list storing every possible laser positions, orientations and values
    pov = position_orientation_value(grid)
    # sort the elements in pov based on their values (scores) by Merge Sorting (Min First Max Last)
    pov = msort(pov)
    # number of lasers to place
    nol = ask_number_of_lasers(len(grid))
    # a list to store positions, orientations and values of lasers to be placed
    laser = []
    for c1 in range(nol):
        if len(laser) == 0:
            # removes the laser with max value and adds it to list laser
            laser.append(pov.pop())
        # checks if the last laser in pov centers on the same square as the lasers in laser. If yes, remove the laser
        # without adding it to laser and check next laser in pov
        else:
            d1 = True
            while d1:
                d2 = True
                for c2 in range(len(laser)):
                    if pov[-1][:pov[-1].index(")")] == laser[c2][:laser[c2].index(")")]:
                        d2 = False
                if d2:
                    laser.append(pov.pop())
                    d1 = False
                else:
                    pov.pop()
    # displays all lasers' scores, positions, and orientations
    for c3 in range(len(laser)):
        print("Laser #" + str(c3 + 1) + " scores " + laser[c3][laser[c3].index(" ") + 1:] + ", Position: " +
              laser[c3][:laser[c3].index(")") + 1] + " facing " +
              laser[c3][laser[c3].index(")") + 1:laser[c3].index(" ")])
    # don't close the window after executing the program
    os.system("pause")


def ask_file_name():
    """
    Prompts for a ﬁle path name with extension.

    :return: the file path name
    """
    filename = input("Please enter the file name of the grid data with extension (e.g. $/.../grid.txt): ")
    return filename


def readfile(filename):
    """
    Opens the file with the grid data, reads the data, and stores the data in a 2D list

    :param filename: file path name of the file with the grid data
    :return: the 2D list storing the grid data
    """
    try:
        grid = []
        with open(filename) as f:
            for line in f:
                line = line.strip()
                data = line.split(" ")
                grid.append(data)
        return grid
    except FileNotFoundError as error:
        print(error, file=sys.stderr)


def position_orientation_value(grid):
    """
    Stores every possible laser placements with values in a list.
    e.g. (2,2)south 18 (form of an element in the list)

    :param grid: the 2D list storing the grid data
    :return: the list storing every possible laser positions, orientations and values
    """
    pov = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            # first row
            if i == 0:
                # ignore the first and the last element, and the rest of the elements only face south
                if 0 < j < len(grid) - 1:
                    pov.append(
                        "(" + str(i) + "," + str(j) + ")south " + str(
                            int(grid[i][j - 1]) + int(grid[i + 1][j]) + int(grid[i][j + 1])))
            # last row
            elif i == len(grid) - 1:
                # ignore the first and the last element, and the rest of the elements only face north
                if 0 < j < len(grid) - 1:
                    pov.append(
                        "(" + str(i) + "," + str(j) + ")north " + str(
                            int(grid[i][j - 1]) + int(grid[i - 1][j]) + int(grid[i][j + 1])))
            # other rows
            else:
                # elements in the first column only face east
                if j == 0:
                    pov.append(
                        "(" + str(i) + "," + str(j) + ")east " + str(
                            int(grid[i - 1][j]) + int(grid[i][j + 1]) + int(grid[i + 1][j])))
                # elements in the last column only face west
                elif j == len(grid) - 1:
                    pov.append(
                        "(" + str(i) + "," + str(j) + ")west " + str(
                            int(grid[i + 1][j]) + int(grid[i][j - 1]) + int(grid[i - 1][j])))
                # other columns
                else:
                    # lasers facing north, east, south, and west sequentially
                    for k in range(4):
                        if k == 0:
                            pov.append("(" + str(i) + "," + str(j) + ")north " + str(
                                int(grid[i][j - 1]) + int(grid[i - 1][j]) + int(grid[i][j + 1])))
                        elif k == 1:
                            pov.append("(" + str(
                                i) + "," + str(j) + ")east " + str(
                                int(grid[i - 1][j]) + int(grid[i][j + 1]) + int(grid[i + 1][j])))
                        elif k == 2:
                            pov.append("(" + str(
                                i) + "," + str(j) + ")south " + str(
                                int(grid[i][j + 1]) + int(grid[i + 1][j]) + int(grid[i][j - 1])))
                        else:
                            pov.append("(" + str(
                                i) + "," + str(j) + ")west " + str(
                                int(grid[i + 1][j]) + int(grid[i][j - 1]) + int(grid[i - 1][j])))
    return pov


def ask_number_of_lasers(n):
    """
    Prompts for the number of lasers to place.
    If an invalid value is input, prompt again.

    :param n: length of the grid data matrix, which is used to calculate the max number of lasers
    :return: the number of lasers to place
    """
    d = True
    nol = 0
    while d:
        nol = input("Please enter an integer number of lasers between 1 to " + str(n * n - 4) + ": ")
        if nol.isdecimal():
            if 0 < int(nol) <= n * n - 4:
                nol = int(nol)
                d = False
    return nol


# main conditional guard
# script execution/run
# the following condition checks whether we are
# running as a script, in which case run the test code.
# if the file is being imported, don't run the test code.
if __name__ == '__main__':
    start()
