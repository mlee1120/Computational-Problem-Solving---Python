"""
file: balance.py
description: CSCI 603 hw8 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
"""

import sys
import math
import turtle

'''
I made the list of beams global for convenience. 
Otherwise, it would have to be passed among several functions.
'''
beams = []


class Beam:
    # instance variables of class Beam
    __slots__ = "name", "position", "weights", "empty_pan_index", "scale_factor"

    # static variable of class Beam (for drawing: represents the length of a edge of the balance puzzle)
    edge_length = 50

    def __init__(self, name):
        """
        Constructor sets up a new Beam object along with its name, position (stores the position of this this Beam
        object if it is hanging on another), weights (a list of Weight objects or Beam objects hanging on it),
        empty_pan_index (if there is a single Weight object having weight of -1, stores the position of it and deals
        with it after this Beam has finished being set up), and scale_factor (pixels per tick along the beam, which
        will be calculated after all beams have been set up by calling .calculate() function).
        :param name: the name of this Beam object
                     Although it is not used, it might be useful when we add more functions to Beam
        """

        '''
        Transforms B to B0, which is helpful for index-based data structure -> beams (list)
        for example: Line 80
        Although the root bean (B or B0) would never be used, I did this just to unify all beams names.
        '''
        if not name.isdecimal() and len(name) == 1:
            name += "0"
        self.name = name
        # the root Beam's position will always be None, other Beams' positions will be changed later
        self.position = None
        self.weights = []
        self.empty_pan_index = None
        self.scale_factor = 0

    def add_weight(self, position, weight):
        """
        This function adds a Weight object or a Beam object to the list of Weights of Beams from this Bean object,
        meaning the object is hanging on this Beam object.
        :param position: relative position of the Weight object or the Beam object to the center of this Beam object
        :param weight:   weight of the Weight object or Beam object's name
        """

        '''
        If weight is not decimal or "-1", meaning it is in form of "B?", adds the corresponding 
        Beam object to the list of objects hanging on this Beam object. Otherwise, creates a new 
        Weight object and add it to the list.
        '''
        if weight.isdecimal() or weight == "-1":
            self.weights.append(Weight(position, weight))
            # stores the position of the Weight object having weight of -1
            if weight == "-1":
                if self.empty_pan_index is not None:
                    print("Each beam can contain at most one weight as -1. Please revise the file.")
                    sys.exit(0)
                self.empty_pan_index = len(self.weights) - 1
        else:
            # checks if all hanging beams' names are valid
            if weight[0].upper() != "B":
                print("Beams' names should start with \"B\". Please revise the file.")
                sys.exit(0)
            if int(weight[1]) < 1 or int(weight[1]) > len(beams):
                print("There is something wrong with the file. Please revise the file.")
                sys.exit(0)
            self.weights.append(beams[int(weight[1]) - 1])
            beams[int(weight[1]) - 1].position = int(position)

    def get_position(self):
        """
        This functions returns the relative position to the center of the Beam object this Beam object is hanging on.
        :return: the relative position
        """
        return self.position

    def get_weight(self):
        """
        This function calculates and returns the total weight of this Beam object. It calls .get_weight() function
        from Weight to get the weight of a single Weight or calls itself recursively if the hanging object is Beam.
        :return: the total weight of this Beam object
        """
        result = 0
        for w in self.weights:
            result += w.get_weight()
        return result

    def is_balanced(self):
        """
        This function calculates to total torque of this Beam object with its center as
        the support point and returns if it is balanced or not.
        :return: if this Beam object is balanced
        """
        total = 0
        for w in self.weights:
            total += w.get_position() * w.get_weight()
        return total == 0

    def calculate(self):
        """
        This function will be called if "empty_pan_index" of this Beam object is not None, and it will calculate the
        Weight's weight at that position (empty_pan_index) by supposing this Beam object balanced (total torque = 0).
        """
        total = 0
        # calculates the total torque caused by all other Weights and Beams hanging on this Beam object
        for i in range(len(self.weights)):
            if i != self.empty_pan_index:
                total += self.weights[i].get_position() * self.weights[i].get_weight()
        self.weights[self.empty_pan_index].weight = int((-total) / self.weights[self.empty_pan_index].get_position())

    def draw(self, first):
        """
        This function draws this Beam object and all its sub-Beam objects recursively in a turtle window.
        :param first: whether or not this Beam object is the first beam to be drawn
        :pre:  turtle facing east at the center of the window, pen down (default conditions)
        :post: turtle facing south, turtle at the position where the balance puzzle
               will be proximately drawn at the center of the window, pen down
        """
        if first:
            self.window_set()
        current_position = 0
        turtle.pendown()
        # draws every Weights or Beams hanging on this Beam in sequence
        for w in self.weights:
            turtle.left(90)
            turtle.forward((w.get_position() - current_position) * self.scale_factor)
            turtle.right(90)
            current_position = w.get_position()
            turtle.forward(self.edge_length)
            if isinstance(w, Beam):
                # recursion
                w.draw(False)
            else:
                turtle.penup()
                turtle.forward(15)
                turtle.write(w.weight, False, "center")
                turtle.back(15)
                turtle.pendown()
            turtle.back(self.edge_length)
        turtle.left(90)
        turtle.forward((0 - current_position) * self.scale_factor)
        turtle.right(90)

    def window_set(self):
        """
        This function sets up the turtle window and turtle's position before drawing the balance puzzle.
        :pre:  turtle facing east at the center of the window, pen down (default conditions)
        :post: turtle facing south, turtle at the position where the balance puzzle
               will be proximately drawn at the center of the window, pen up
        """

        '''
        actual height of the balance puzzle if it has a balanced binary structure, in which every 
        beam has at most two other beams hanging on it and the structure is balanced (not torque balance).
        '''
        estimated_height = int(round(math.log(len(beams), 2))) + 1
        # sets the window size
        turtle.screensize(self.edge_length * (estimated_height + 1), self.edge_length * (estimated_height + 1))
        turtle.penup()
        # Sets the turtle position so that the balance puzzle would be proximately drawn at the center of window.
        turtle.setposition(0, self.edge_length * estimated_height / 2)
        turtle.right(90)


class Weight:
    # instance variables of class Weight
    __slots__ = "position", "weight"

    def __init__(self, position, weight):
        """
        Constructor sets up a new Weight objects along with its position and weight.
        :param position: relative position of this Weight object to the center of
                         the beam, on which this Weight object is hanging
        :param weight:   weight of this Weight object
        """
        self.position = int(position)
        self.weight = int(weight)

    def get_position(self):
        """
        This function return the relative position of this Weight object.
        :return: the relative position of this Weight object
        """
        return self.position

    def get_weight(self):
        """
        This function returns the weight of this Weight object.
        :return:  the weight of this Weight object
        """
        return self.weight


def read(filename):
    """
    This function reads in the information of a balance puzzle from a text file line by line and stores
    the information in a list of beams, each having a list of Weights and Beams.
    I assume all file provide a list of beams in the order of:
    Leaf beams (beams without hanging beam) first -> parent beams of leaf beams -> ... -> the root beam (the last)
    :param filename: the file path name of the text file storing the information of a balance puzzle
    """
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                data = line.split(" ")
                # checks if the number of data is correct in every line
                if len(data) % 2 != 1:
                    print("Bad configuration file. Please check and revise the file.")
                    sys.exit(0)
                # checks if all beams' names start with "B"
                if data[0][0].upper() != "B":
                    print("Beams' names should start with \"B\". Please revise the file.")
                    sys.exit(0)
                # creates a new Beam object
                beam = Beam(data[0].upper())
                # add the new Beam object to the list of beams
                beams.append(beam)
                # adds all weights to the beam
                for i in range(1, len(data) - 1, 2):
                    beam.add_weight(data[i], data[i + 1])
                # deals with the empty pan (if exists) once a beam is set up
                if beam.empty_pan_index is not None:
                    beam.calculate()
    except FileNotFoundError as error:
        print(error, file=sys.stderr)
        sys.exit(-1)


def scale():
    """
    This function calculates scale factors for every Beam Object in the list of beams.
    """

    # Traverses through every beams for calculating their scale factors.
    for b in beams:
        # a list to store all possible scale factors for a beam temporarily
        temp = []
        # calculates a scale factor for every two adjacent objects hanging on a Beam
        for i in range(0, len(b.weights) - 1, 1):
            # basic gap size between two adjacent Weights
            result = 20.0

            # if both objects are Beams
            if isinstance(b.weights[i], Beam) and isinstance(b.weights[i + 1], Beam):

                # if both Beams are empty, requires only the basic gap
                if len(b.weights[i].weights) == 0 and len(b.weights[i + 1].weights) == 0:
                    pass

                # if the left Beam is empty, requires basic gap + the right (sub-)Beams leftmost objects total distance
                elif len(b.weights[i].weights) == 0:
                    # calls recursive helper function to calculate the total leftmost objects distance
                    result = 20.0 + _scale(b.weights[i + 1], 0)

                # if the right Beam is empty, requires the left (sub-)Beams rightmost objects total distance + basic gap
                elif len(b.weights[i + 1].weights) == 0:
                    # calls recursive helper function to calculate the total rightmost objects distance
                    result = _scale(b.weights[i], -1) + 20.0

                # both Beams are not empty
                else:
                    '''
                    requires total rightmost objects distance from the left Beams and all its rightmost sub-Beams + 
                    basic gap +  total leftmost objects distance from the right Beams and all its leftmost sub-Beams.
                    '''
                    result = _scale(b.weights[i], -1) + 20.0 + _scale(b.weights[i + 1], 0)

            # if the left object is a Beam
            elif isinstance(b.weights[i], Beam):
                if len(b.weights[i].weights) == 0:
                    pass
                else:
                    result = _scale(b.weights[i], -1) + 20.0

            # if the right object is a Beam
            elif isinstance(b.weights[i + 1], Beam):
                if len(b.weights[i + 1].weights) == 0:
                    pass
                else:
                    result = 20.0 + _scale(b.weights[i + 1], 0)

            # both objects are not Beams (they are both Weights)
            else:
                pass

            # add all possible scale factors to the list
            temp.append(result / (b.weights[i + 1].get_position() - b.weights[i].get_position()))
        # chooses the largest possible scale factor as the Beam object's scale factor for not causing overlap
        b.scale_factor = max(temp)


def _scale(beam, index):
    """
    The recursive helper functions which helps calculate possible scale factors.
    :param beam:  the beam whose leftmost or rightmost distance to be calculated
    :param index: 0 (leftmost) or -1(rightmost)
    :return: the total distance
    """
    if isinstance(beam.weights[index], Beam):
        return abs(beam.weights[index].get_position()) * beam.scale_factor + _scale(beam.weights[index], index)
    else:
        return abs(beam.weights[index].get_position()) * beam.scale_factor


def check_balance():
    """
    This function checks and prints out if the balance puzzle is balanced by traversing
    through the list of beams and sees if they are all balanced or not.
    """
    result = True
    for b in beams:
        if not b.is_balanced():
            # If a single beam in the puzzle is not balanced, the puzzle is not balanced.
            result = False
            break
    if result:
        print("The puzzle is balanced!")
    else:
        print("The puzzle is unbalanced!")


'''
main conditional guard
The following condition checks whether we are running as a script.
If the file is being imported, don't run the test code.
'''
if __name__ == '__main__':
    # checks if users provide the file path name of the file to be read
    if len(sys.argv) == 1:
        print("Usage: balance.py filename")
        print("Please add the filename of the file to be read to program arguments (Edit configuration -> Parameters)")
        sys.exit(0)
    read(sys.argv[1])
    if len(beams) == 0:
        print("There might be something wrong in your file (e.g. it is an empty file). Please check it.")
        sys.exit(0)
    scale()
    # draws the balance puzzle from its root by calling root beam's draw function
    beams[-1].draw(True)
    check_balance()
    turtle.mainloop()
