"""
file: dnalist.py
description: CSCI 603 hw6 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
"""

from collections.abc import Iterable, Iterator


class LinkedNode:
    # instance variables of class LinkedNode
    __slots__ = "value", "link"

    def __init__(self, value, link=None):
        """
        Constructor sets up a new LinkedNode with a value and a link pointing to an existing one or None.
        :param value: the value to be stored in the new node
        :param link: another LinkedNode or None to be pointed to by the new node
        """
        self.value = value
        self.link = link


class DNAList(Iterable):
    # instance variables of class DNAList
    __slots__ = 'front', 'back'

    def __init__(self, gene=''):
        """
        Constructor sets up a new DNAList.
        :param gene: an optional argument for which a default (empty string) value is provided
        """
        self.front = None
        self.back = None
        # checks if the parameter is valid
        if isinstance(gene, str):
            for i in gene:
                i = i.upper()
                # checks if the parameter contains only 'A', 'C', 'G', or 'T'
                if i == 'A' or i == 'C' or i == 'G' or i == 'T':
                    self.append(i)
                # creates an empty DNAList because there are invalid characters
                else:
                    print("Invalid arguments for DNAList(gene).")
                    print("gene should be a string containing only 'A', 'C', 'G', or 'T'.")
                    print("Creating an empty DNAList instead.")
                    self.front = None
                    self.back = None
                    break
        else:
            print("Invalid argument for DNAList(gene).")
            print("gene a string (type 'str').")
            print("Creating an empty DNAList instead.")

    def __eq__(self, other):
        """
        This function compares if two DNAList have the same elements.
        :param other: another DNAList different from this DNAList
        :return: if two DNALists have the same elements
        """
        result = False
        if self.size() == other.size():
            result = True
            node_1 = self.front
            node_2 = other.front
            # compares two DNALists node value by node value (element by element)
            while node_1 is not None:
                if node_1.value != node_2.value:
                    result = False
                    break
                node_1 = node_1.link
                node_2 = node_2.link
        return result

    def __str__(self):
        """
        This function simply returns a string with the contents of the nodes all together, such as GCACTT.
        :return: a string with the contents of the nodes all together
        """
        a_string = ""
        node = self.front
        while node is not None:
            a_string += node.value
            node = node.link
        return a_string

    def append(self, item):
        """
        This function takes in a single character 'item' and extends the list with a node that represents this
        character.
        :param item: a single character
        """
        # checks if the parameter is valid
        if not isinstance(item, str):
            print('Invalid arguments for DNAList.append(item).')
            print('item should be a string (type str).')
            print('No action was executed on the DNAList. Please try entering some valid arguments.')
        else:
            item = item.upper()
            # checks if the parameter is 'A', 'C', 'G', or 'T'
            if item == 'A' or item == 'C' or item == 'G' or item == 'T':
                new_node = LinkedNode(item)
                if self.front is None:
                    self.front = new_node
                else:
                    self.back.link = new_node
                self.back = new_node
            else:
                print('Invalid arguments for DNAList.append(item).')
                print("item should be a single character 'A', 'C', 'G', or 'T'.")
                print('No action was executed on the DNAList. Please try entering some valid arguments.')

    def join(self, other):
        """
        This function takes in another DNAList 'other' and adds it to the end of this DNAList.
        :param other: another DNAList
        """
        if self.back is None:
            self.front = other.front
        else:
            self.back.link = other.front
        self.back = other.back

    def splice(self, ind, other):
        """
        This function takes in an integer 'ind' representing an index into this DNAList, and another DNAList 'other'.
        It should then insert 'other' into this DNAList immediately after the ind’th character of this DNAList.
        :param ind: an index into this DNAList
        :param other: another DNAList
        """
        # if this DNAList is empty, don't do anything
        if self.empty():
            print('The original DNAList is empty. Splice can not be executed.')
        # checks if the parameters are valid
        elif not isinstance(ind, int) or ind < -self.size() or ind >= self.size() or not isinstance(other, DNAList):
            print('Invalid arguments for DNAList.splice(ind, other). Instructions are shown as below:')
            print('1. ind should be an integer.')
            print('2. ind should be greater than ' + str(-self.size()) + ' and less ' + str(self.size()) + '.')
            print('3. other should be a DNAList')
            print('No action was executed on the DNAList. Please try entering some valid arguments.')
        # if other is empty, don't do anything, either
        elif other.empty():
            print('The DNAList you provided is empty. Splice was not executed on the original DNAList')
        else:
            if ind < 0:
                ind = self.size() + ind
            node = self.front
            for _ in range(ind):
                node = node.link
            other.back.link = node.link
            node.link = other.front

    def snip(self, i1, i2):
        """
        This function removes a portion of the gene (list) as specified by the integers i1 and i2. Specifically,
        counting from the beginning of the list as 0, the list should no longer contain all nodes from the node
        at position i1 (inclusive) up to but not including position i2.
        :param i1: the starting node position to be removed (inclusive)
        :param i2: the ending node position to be removed (exclusive)
        """
        # checks if the parameters are valid
        if not isinstance(i1, int) or not isinstance(i2, int) or i1 < 0 or i1 >= i2 or i2 >= self.size():
            print('Invalid arguments for DNAList.snip(i1, i2). Instructions are shown as below:')
            print('1. i1 and i2 should be integers.')
            print('2. i1 should be equal and greater than 0 and less i2.')
            print('3. i2 should be less than ' + str(self.size()) + '.')
            print('No action was executed on the DNAList. Please try entering some valid arguments.')
        else:
            node_start = None
            node_end = self.front
            for c in range(i2):
                if c == i1 - 1:
                    node_start = node_end
                node_end = node_end.link
            # snip begins at the first node
            if node_start is None:
                self.front = node_end
            else:
                node_start.link = node_end

    def replace(self, repstr, other):
        """
        This function finds the string 'repstr' as a subsequence of this DNAList and replace it with DNAList 'other'.
        All target subsequences in the DNAList will be replaced.
        :param repstr: a string to be found in this DNAList
        :param other: a DNAList to replace the subsequence
        """
        # checks if the parameters are valid
        if not isinstance(repstr, str) or not isinstance(other, DNAList):
            print('Invalid arguments for DNAList.replace(repstr, other). Instructions are shown as below:')
            print('1. repstr should be a string (type str).')
            print('2. other should be a DNAList.')
            print('No action was executed on the original DNAList. Please try entering some valid arguments.')
        else:
            repstr = repstr.upper()
            node = self.front
            # node_start stores the node which starts replacing (exclusive)
            node_start = None
            # node_end stores the node which ends replacing (exclusive)
            node_end = None
            # variable decides whether to replace or not
            re = False
            # traverses this DNAList to find target sequence
            while node is not None:
                if node.value == repstr[0]:
                    # temporary node for traversing while comparing
                    node_temp = node.link
                    node_end = node.link
                    # compares sequences to see if it matches the target sequence
                    for counter in range(len(repstr) - 1):
                        if node_temp.value != repstr[counter + 1]:
                            re = False
                            break
                        else:
                            node_temp = node_temp.link
                            node_end = node_temp
                            re = True
                    if len(repstr) == 1:
                        re = True
                # starts replacing if re == True
                if re:
                    re = False
                    if other.empty():
                        if node_start is None:
                            self.front = node_end
                        else:
                            node_start.link = node_end
                        node = node_end
                    else:
                        other_copy = other.copy()
                        if node_start is None:
                            self.front = other_copy.front
                        else:
                            node_start.link = other_copy.front
                        other_copy.back.link = node_end
                        node_start = other_copy.back
                        node = node_end
                # keeps on traversing and looks for the all target sequences in the DNAList
                else:
                    node_start = node
                    node = node.link

    def copy(self):
        """
        This function returns a new DNAList with the same contents as the DNAList called upon.
        :return: a new DNAList with the same contents as the DNAList called upon.
        """
        new_list = DNAList()
        node = self.front
        while node is not None:
            new_list.append(node.value)
            node = node.link
        return new_list

    def size(self):
        """
        This function calls its helper function to calculate the size of a DNAList and returns the value.
        :return the number of data elements in this DNAList
        """
        return self._size_to_end(self.front)

    # "_" implies helper functions or private functions
    def _size_to_end(self, node):
        """
        This function helps calculating the number of data elements in a DNAList recursively.
        :param node: a node used to scan every node in a DNAList
        :return: the number of data elements in a DNAList
        """
        if node is None:
            return 0
        else:
            # remember self. !!!
            return 1 + self._size_to_end(node.link)

    def empty(self):
        """
        This function tells its caller function if this DNAList is empty or not.
        :return: the result if this DNAList is empty or not
        """
        return self.back is None

    '''
    def __iter__(self):
        cursor = self.front
        while cursor is not None:
            yield cursor.value
            cursor = cursor.link
    '''

    def __iter__(self):
        return DNAList.Iter(self.front)

    class Iter(Iterator):
        __slots__ = "cursor"

        def __init__(self, front):
            self.cursor = front

        def __next__(self):
            if self.cursor is None:
                raise StopIteration()
            temp = self.cursor
            self.cursor = self.cursor.link
            return temp.value


"""
main conditional guard
The following condition checks whether we are running as a script.
If the file is being imported, don't run the test code.
"""
if __name__ == '__main__':
    pass
