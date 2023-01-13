"""
file: holicow.py
description: CSCI 603 hw9 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
"""

import sys
import math


class Vertex:
    """
    An individual vertex in a graph.
    """
    # instance variables of class Vertex
    __slots__ = 'isPaintball', 'id', 'posX', 'posY', 'radius', 'connectedTo'

    def __init__(self, paintball_or_not, name, x, y, r=0):
        """
        Constructor sets up a new Vertex with isPaintball telling if the Vertex is a paintball or a cow, an id storing
        the name of this Vertex (paintball/cow), the (x, y) positions of this Vertex, the splatter radius of this Vertex
        (paintball > 0; cow = 0), and a dictionary of its neighbor vertices with keys as the neighbor vertices and
        values as the number of cows this vertex (if paintball) painted if triggered.
        :param paintball_or_not: if this Vertex is a paintball or not (a cow instead)
        :param name: the name of the cow/the color of the paintball
        :param x: the x position of this Vertex
        :param y: the y position of this Vertex
        :param r: the splatter radius of this vertex (paintball > 0; cow = 0)
        """
        self.isPaintball = paintball_or_not
        self.id = name
        self.posX = x
        self.posY = y
        self.radius = r
        self.connectedTo = {}  # or dict()

    def add_neighbor(self, nbr, weight=0):
        """
        This function add a neighbor Vertex to this Vertex. (add a directed edge/relationship)
        :param nbr: the neighbor Vertex
        :param weight: the weight of this edge
        """
        self.connectedTo[nbr] = weight

    def __str__(self):
        """
        Return a string representation of the vertex and its direct neighbors:
            vertex-id connectedTo [neighbor-1-id, neighbor-2-id, ...]
        :return: The string
        """
        return str(self.id) + ' connectedTo: ' + str([str(x.id) for x in self.connectedTo])

    def __eq__(self, other):
        """
        This function compares if two Vertices are identical.
        :param other: another Vertex different from this one
        :return: if two Vertices are identical
        """
        if not isinstance(other, Vertex):
            return False
        else:
            return self.id == other.id and self.posX == other.posX and \
                   self.posY == other.posY and self.radius == other.radius

    def __hash__(self):
        """
        This function returns the hash code of this Vertex.
        (Override __hash__ everytime __eq__ is overridden.)
        :return: the hash code
        """
        return hash(self.id) + hash(self.posX) + hash(self.posY) + hash(self.radius)

    def get_connections(self):
        """
        This functions returns all neighbor Vertices of this Vertex.
        :return: all neighbor Vertices of this Vertex
        """
        return self.connectedTo.keys()


class Graph:
    """
    An individual graph.
    """
    # instance variables of class Graph
    __slots__ = 'vertexDict'

    def __init__(self):
        """
        Constructor set up a new Graph having a dictionary with keys as all vertices and values as the numbers of
        painted cows by the vertex (if it is a cow => 0; if it is a paintball => 0, but will be calculated later)
        """
        self.vertexDict = dict()

    def add_vertex(self, vertex, number_of_descendant_cows=0):
        """
        This function adds a Vertex to this Graph
        :param vertex: the Vertex to be added
        :param number_of_descendant_cows: the number of painted cows by the Vertex
        """
        # checks if the Vertex is already in this Graph
        if vertex not in self.vertexDict:
            self.vertexDict[vertex] = number_of_descendant_cows

    def build_edges(self):
        """
        This function builds all edges of this Graph according to the given information
        """
        # traverses all Vertices in the Graph
        for vertex in self.vertexDict.keys():
            # if the vertex is a paintball
            if vertex.isPaintball:
                # checks if there is an edge(relationship) between this paintball and another Vertex
                for neighbor in self.vertexDict.keys():
                    '''
                    checks if there is a relationship by comparing the distance between two vertices with 
                    the splatter radius of the paintball. 
                    distances are calculated by Pythagorean theorem
                    '''
                    if neighbor != vertex and vertex.radius >= math.sqrt(
                            (vertex.posX - neighbor.posX) ** 2 + (vertex.posY - neighbor.posY) ** 2):
                        vertex.add_neighbor(neighbor)

    def __iter__(self):
        """
        This function returns an iterator over the vertices in the graph, which allows the user to do:
            for vertex in graph:
                ...
        :return: the iterator
        """
        return iter(self.vertexDict.keys())


def cow():
    """
    This function executes all the tasks asked by Lab 9 Implementation Section.
    """
    graph = build_graph(sys.argv[1])
    display_field(graph)
    trigger_all(graph)
    display_optimal(graph)


def build_graph(filename):
    """
    This function read information from a text file and build a graph according to the information.
    :param filename: the file path name of the text file to be rea
    :return: the built graph
    """
    result = Graph()
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                data = line.split(" ")
                if data[0] == "cow":
                    result.add_vertex(Vertex(False, data[1], int(data[2]), int(data[3])))
                else:
                    result.add_vertex(Vertex(True, data[1], int(data[2]), int(data[3]), int(data[4])))
    # if the file name is provided, but does not exist
    except FileNotFoundError:
        print("File Not Found: {" + filename + "}")
        sys.exit(-1)
    result.build_edges()
    return result


def display_field(graph):
    """
    This function displays a graph as an adjacency list where each vertex indicates what
    neighboring vertices it is connected to.
    :param graph: a graph to be displayed
    """
    print("Field of Dreams")
    print("---------------")
    for vertex in graph:
        print(vertex)


def trigger_all(graph):
    """
    This function simulates triggering every paintball and shows the results.
    :param graph: a graph to be simulated triggering all paint balls
    """
    print("\nBeginning simulation...")
    for vertex in graph:
        if vertex.isPaintball:
            print("Triggering " + vertex.id + " paint ball...")
            graph.vertexDict[vertex] = depth_first_trigger(vertex)


def depth_first_trigger(start):
    """
    This function applies Depth First Search method to traverse all vertices in a graph for simulation.
    :param start: the starting vertex in the graph
    :return: the number of painted cows by a paintball
    """
    visited = set()
    visited.add(start)
    return __depth_first_trigger(start, visited)


def __depth_first_trigger(current, visited):
    """
    This is a helper function for executing DFS.
    :param current: the current Vertex (during traversing)
    :param visited: a set of visited Vertices to prevent repeated visit
    :return: the number of painted cows (not final number)
    """
    total = 0
    for neighbor in current.get_connections():
        if neighbor not in visited:
            if neighbor.isPaintball:
                # only paint balls are add to visited because cow can be visited (painted) twice or more times
                visited.add(neighbor)
                print("\t" + neighbor.id + " paint ball is triggered by " + current.id + " paint ball")
                total += __depth_first_trigger(neighbor, visited)
            else:
                print("\t" + neighbor.id + " is painted " + current.id + "!")
                total += 1
    return total


def display_optimal(graph):
    """
    This function finds the paintball which paints the cows with most colors and displays the results.
    :param graph: the graph to be traversed
    """
    print("\nResults:")
    best_choice = None
    best_total = 0
    for vertex in graph:
        if graph.vertexDict[vertex] >= best_total:
            best_total = graph.vertexDict[vertex]
            best_choice = vertex
    print("Triggering the " + best_choice.id + " paint ball is the best choice with " + str(
        best_total) + " total paint on cows:")
    if best_total == 0:
        print("No cows were painted by any starting paint ball!")
    else:
        visited = set()
        visited.add(best_choice)
        generate_results(best_choice, visited)
        for vertex in graph:
            if not vertex.isPaintball:
                print("\t" + vertex.id + "'s colors: {", end="")
                i = 0
                for paint in vertex.get_connections():
                    if i == len(vertex.get_connections()) - 1:
                        print("'" + paint.id + "'", end="")
                    else:
                        print("'" + paint.id + "', ", end="")
                    i += 1
                print("}")


def generate_results(current, visited):
    """
    This function helps showing the results of every cow's painted colors
    by triggering the optimal paintball (only traverses the best path).
    :param visited: set of visited Vertices to prevent repeated visit
    :param current: the current Vertex (during traversing)
    """
    for vertex in current.get_connections():
        if vertex not in visited:
            if vertex.isPaintball:
                # only paint balls are add to visited because cow can be visited (painted) twice or more times
                visited.add(vertex)
                generate_results(vertex, visited)
            else:
                vertex.add_neighbor(current)


'''
main conditional guard
The following condition checks whether we are running as a script.
If the file is being imported, don't run the test code.
'''
if __name__ == '__main__':
    # checks arguments
    if len(sys.argv) != 2:
        print("Usage: python3 holicow.py {filename}")
        sys.exit(-1)
    cow()
