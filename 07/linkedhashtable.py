"""
file: linkedhashtable.py
description: CSCI 603 hw7 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
"""

from hw7.set import SetType
from collections.abc import Iterable


class ChainNode:
    # instance variables of class ChainNode
    __slots__ = "key", "chain", "prevInsertion", "nextInsertion"

    def __init__(self, obj=None, prev=None, link=None, chain=None):
        """
        Constructor sets up a new ChainNode with a key (storing keys in this homework), a pointer 'chain' pointing to
        the next node in a location in the table (or None if there is no next node), a pointer 'prevInsertion' pointing
        to the node added to the LinkedHshTable right before this node (or None if this node is the first node added to
        the table), and also a pointer 'nextInsertion' pointing to the node added to the table right after this node
        (or to None if this node is so far the last node added into the table).
        :param obj: the key to be stored in this new node
        :param prev: another ChainNode added to the table right before this node
        :param link: another ChainNode added to the table right after this node
        :param chain: another ChainNode added to the table after this node and having a collision with this node
        """
        self.key = obj
        self.chain = chain
        self.prevInsertion = prev
        self.nextInsertion = link


class LinkedHashTable(SetType, Iterable):
    # instance variables of class LinkedHashTable
    __slots__ = "table", "buckets", "LOAD_LIMIT", "front", "back"

    def __init__(self, initial_num_buckets=100, load_limit=0.75):
        """
        Constructor sets up a new LinkedHashTable with a size of 0 (implying that no key is stored in the table at
        the beginning), including an empty table (list) with a size (buckets), a front pointer which will points to
        the first-added key, a back pointer which will points to the last-added key, and LOAD_LIMIT.
        :param initial_num_buckets: the initial size of the table
        :param load_limit: tells the program when to rehash or reducing the size of the table
        """
        super().__init__()
        # deals with invalid arguments (creating a LinkedHashTable with default values)
        if not isinstance(initial_num_buckets, int):
            print("The number of buckets should be an integer.")
            initial_num_buckets = 10
        elif initial_num_buckets < 10:
            print("The minimum number of buckets is 10.")
            initial_num_buckets = 10
        if not isinstance(load_limit, float) or load_limit <= 0 or load_limit >= 1:
            print("Load limit should be a float number between 0 to 1.")
            load_limit = 0.75
        print("Creating a table with " + str(initial_num_buckets) + " buckets and load limit of " + str(
            load_limit) + " ...", end="\n\n")
        self.buckets = initial_num_buckets
        self.LOAD_LIMIT = load_limit
        self.front = None
        self.back = None
        self.table = list()
        for _ in range(self.buckets):
            self.table.append(None)

    def contains(self, obj):
        """
        This program checks if a key exists in the table.
        :param obj: the key to be checked
        :return: True if the key exists in the table or False if not
        """
        result = False
        if isinstance(obj, str):
            # computes the location in the table
            index = self.hash_function(obj) % self.buckets
            # temporary pointer used to traverse a location in the table
            node_temp = self.table[index]
            if node_temp is not None:
                # traversing
                while node_temp is not None and node_temp.key != obj:
                    node_temp = node_temp.chain
                result = node_temp is not None and node_temp.key == obj
        return result

    def add(self, obj):
        """
        This function adds a key (ChainNode) tp the table.
        :param obj: the key to be added to the table
        """
        # checks if the argument is valid
        if not isinstance(obj, str):
            print("Invalid argument: the key should be a string.")
        else:
            # if the key is not in the table
            if not self.contains(obj):
                # rehashing if load factor exceeds te load limit
                if self.size / self.buckets >= self.LOAD_LIMIT:
                    # temporary pointer for keeping track of all added ChainNodes
                    temp_node = self.front
                    self.size = 0
                    self.buckets *= 2
                    self.table = list()
                    for _ in range(self.buckets):
                        self.table.append(None)
                    # adding all keys back to the resized table
                    while temp_node is not None:
                        self.add(temp_node.key)
                        temp_node = temp_node.nextInsertion

                # computes the location in the table
                index = self.hash_function(obj) % self.buckets
                # creates a new ChainNode storing the key
                node = ChainNode(obj)

                # first key added to the table
                if self.size == 0:
                    self.front = node
                    self.table[index] = node

                # not first key added to the table
                else:
                    node.prevInsertion = self.back
                    self.back.nextInsertion = node

                    # first key added to one location in the table
                    if self.table[index] is None:
                        self.table[index] = node

                    # collision -> chaining
                    else:
                        node_temp = self.table[index]
                        # traverse to the last ChainNode in the location
                        while node_temp.chain is not None:
                            node_temp = node_temp.chain
                        node_temp.chain = node
                self.back = node
                self.size += 1

            # if the key is already in the table
            else:
                print("Key '" + str(obj) + "' is already in the table.")

    def remove(self, obj):
        """
        This function removes a key (ChainNode) from the table without messing up the order of insertion of other keys.
        :param obj: the key to be removed from the table
        """
        # if the key is in the table
        if self.contains(obj):
            # reduces the table size if load factor falls behind the lower load limit
            if self.size / self.buckets <= 1 - self.LOAD_LIMIT:
                # temporary pointer for keeping track of all inserted ChainNode
                temp_node = self.front
                self.size = 0
                self.buckets //= 2
                # the minimum table size is 10 according to the provided documentation
                if self.buckets < 10:
                    self.buckets = 10
                self.table = list()
                for _ in range(self.buckets):
                    self.table.append(None)
                while temp_node is not None:
                    self.add(temp_node.key)
                    temp_node = temp_node.nextInsertion
            # computes the location in the table
            index = self.hash_function(obj) % self.buckets

            # if the target ChainNode is the only ChainNode in the table
            if self.size == 1:
                self.front = None
                self.back = None
                self.table[index] = None
            else:
                # the target ChainNode to be removed
                target_node = self.table[index]
                # the ChainNode added to the same location right before the target ChainNode
                before_target_node = None
                # traverse the chain at the corresponding location to find the target ChainNode
                while target_node.key != obj:
                    before_target_node = target_node
                    target_node = target_node.chain

                # the following if-elif-else statements deal with adding order to the table

                # if the target ChainNode is the first ChainNode added to the table
                if self.front == target_node:
                    self.front = self.front.nextInsertion
                    self.front.prevInsertion = None
                # if the target ChainNode is the last ChainNode added to the table
                elif self.back == target_node:
                    self.back = self.back.prevInsertion
                    self.back.nextInsertion = None
                # other situations
                else:
                    target_node.prevInsertion.nextInsertion = target_node.nextInsertion
                    target_node.nextInsertion.prevInsertion = target_node.prevInsertion

                # the following if-else statements deal with adding order to a location in the table

                # if the target ChainNode is the first ChainNode added to a certain location
                if before_target_node is None:
                    self.table[index] = self.table[index].chain
                # other situations
                else:
                    before_target_node.chain = target_node.chain
            self.size -= 1
        # if the key is not in the table
        else:
            print("Key '" + str(obj) + "' does not exist in the table.")

    def __iter__(self):
        """
        iterator for LinkedHashTable
        """
        node = self.front
        # traverses through all ChainNodes and yields their key values in the order of insertion to the table
        while node is not None:
            yield node.key
            node = node.nextInsertion

    def hash_function(self, obj):
        """
        This function receives a string object, calculates its hash code, and returns the hash code of the object.
        :param obj: the key (a string) to be added to the table
        :return: the hash code of obj
        """
        result = 0
        for index in range(len(obj)):
            result += ord(obj[index]) * pow(31, index)
        return result


'''
main conditional guard
The following condition checks whether we are running as a script.
If the file is being imported, don't run the test code.
'''
if __name__ == '__main__':
    pass
