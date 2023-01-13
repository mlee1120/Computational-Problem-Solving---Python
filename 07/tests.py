""" 
file: tests.py
description: Verify the LinkedHashTable class implementation
language: python3
author: Michael Lee ml3406@RIT.EDU
"""

__author__ = "Michael Lee"

from linkedhashtable import LinkedHashTable


def print_set(a_set):
    for word in a_set:  # uses the iter method
        print(word, end=" ")
    print()


def test0():
    """
    This is the provided test case.
    """
    print("The provided test case:")
    table = LinkedHashTable(100)
    table.add("to")
    table.add("do")
    table.add("is")
    table.add("to")
    table.add("be")
    print_set(table)
    print("'to' in table?", table.contains("to"))
    table.remove("to")
    print("'to' in table?", table.contains("to"))
    print_set(table)
    print("Test case 0 passed!")


def test1():
    """
    This test case tests basic functions of constructor and all methods from LinkedHashTable and ChainNode
    """
    print("\nTest Case 1:")
    # invalid arguments while declaring a LinkedHashTable
    table = LinkedHashTable("Hello")
    table = LinkedHashTable(11.5)
    table = LinkedHashTable(10, 5)
    # checks initial values of all parameters
    assert table.size == 0
    assert table.buckets == 10
    assert len(table.table) == 10
    for i in range(len(table.table)):
        assert table.table[i] is None
    assert table.LOAD_LIMIT == 0.75
    assert table.front is None
    assert table.back is None
    # invalid arguments for contains()
    print("Is 100 in the table? Result:", table.contains(100))
    print("Is None in the table? Result:", table.contains(None))
    # checks contains() for non-existing key
    print("Is 'dog' in the table? Result:", table.contains("dog"))
    # checks add()
    table.add("dog")
    assert table.size == 1
    assert table.front.key == table.back.key == "dog"
    assert table.front.prevInsertion == table.front.nextInsertion == table.front.chain is None
    # checks contains() for existing key
    print("Is 'dog' in the table? Result:", table.contains("dog"))
    # adds existing key
    table.add("dog")
    assert table.size == 1
    assert table.front.key == table.back.key == "dog"
    # checks iterator
    print_set(table)
    table.add("cat")
    assert table.size == 2
    assert table.front.key == "dog"
    assert table.back.key == "cat"
    print("Is 'cat' in the table? Result:", table.contains("cat"))
    # this program is case sensitive
    print("Is 'Cat' in the table? Result:", table.contains("Cat"))
    print_set(table)
    # removes non-existing key
    table.remove("fish")
    assert table.size == 2
    # removes existing keys
    table.remove("cat")
    assert table.size == 1
    print("Is 'cat' in the table? Result:", table.contains("cat"))
    print("Is 'dog' in the table? Result:", table.contains("dog"))
    print_set(table)
    table.remove("dog")
    assert table.size == 0
    print("Is 'dog' in the table? Result:", table.contains("dog"))
    print("\nTest case 1 passed!")


def test2():
    """
    This test case checks if all pointers point to the right objects in all cases and also forces rehashing and
    reducing table size.
    """
    print("\nTest Case 2:")
    table = LinkedHashTable(10)
    # first insertion into the table ("duck" is at location 3)
    table.add("duck")
    assert table.front == table.back == table.table[table.hash_function("duck") % 10]
    assert table.front.key == "duck"
    assert table.front.prevInsertion == table.front.nextInsertion == table.front.chain is None
    # second insertion into the table ("mouse" is also at location 3 => collision)
    table.add("mouse")
    assert table.hash_function("duck") % 10 == table.hash_function("mouse") % 10
    assert table.front == table.table[table.hash_function("duck") % 10]
    assert table.front.key == "duck"
    assert table.back.key == "mouse"
    assert table.front.nextInsertion == table.front.chain == table.back
    assert table.back.prevInsertion == table.front
    assert table.front.prevInsertion == table.back.nextInsertion == table.back.chain is None
    # reset table
    table = LinkedHashTable(10)
    table.add("duck")
    # second insertion into the table ("lion" is at location 4 => no collision)
    table.add("lion")
    assert table.hash_function("duck") % 10 != table.hash_function("lion") % 10
    assert table.front == table.table[table.hash_function("duck") % 10]
    assert table.back == table.table[table.hash_function("lion") % 10]
    assert table.front.key == "duck"
    assert table.back.key == "lion"
    assert table.front.nextInsertion == table.back
    assert table.back.prevInsertion == table.front
    assert table.front.prevInsertion == table.back.nextInsertion == table.front.chain == table.back.chain is None
    # forces rehashing
    table.add("monkey")
    table.add("cow")
    table.add("sheep")
    table.add("horse")
    table.add("dog")
    table.add("chicken")
    # after chicken is added, load factor becomes 0.8, which is greater than or equal to LOAD_LIMIT
    print(table.size / table.buckets)
    print("The table size is now", table.buckets)
    print_set(table)
    # rehashing
    table.add("bee")
    print("After rehashing, the table size becomes", table.buckets)
    print_set(table)
    table.add("a")
    table.add("b")
    table.add("c")
    table.add("d")
    table.add("e")
    table.add("f")
    print(table.size / table.buckets)
    # second rehashing
    table.add("g")
    print("After second rehashing, the table size becomes", table.buckets)
    print_set(table)
    # forces reducing table size
    table.remove("a")
    table.remove("b")
    table.remove("c")
    table.remove("d")
    table.remove("e")
    # after "g" is removed, load factor becomes 0.25, which is less than or equal to (1 - LOAD_LIMIT)
    table.remove("f")
    print(table.size / table.buckets)
    # first reduction
    table.remove("g")
    print("After reducing table size, the table size becomes", table.buckets)
    print_set(table)
    table.remove("sheep")
    table.remove("dog")
    table.remove("monkey")
    # after duck is removed, load factor becomes 0.25, which is less than or equal to (1 - LOAD_LIMIT)
    table.remove("duck")
    print(table.size / table.buckets)
    # second reduction
    table.remove("chicken")
    print("After second reduction, the table size becomes", table.buckets)
    print_set(table)

    # removes the only key in the table
    table = LinkedHashTable(10)
    table.add("duck")
    table.remove("duck")
    assert table.table[table.hash_function("duck") % 10] == table.front == table.back is None

    # removes the first added but not the only key in the table (with collision)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("mouse")
    table.remove("duck")
    assert table.front == table.back == table.table[table.hash_function("mouse") % 10]
    assert table.front.key == "mouse"
    assert table.front.prevInsertion == table.front.nextInsertion == table.front.chain is None

    # removes the first added but not the only key in the table (without collision)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("lion")
    table.remove("duck")
    assert table.front == table.back == table.table[table.hash_function("lion") % 10]
    assert table.front.key == "lion"
    assert table.front.prevInsertion == table.front.nextInsertion == table.front.chain is None

    # removes the last added but not the only key in the table (with collision)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("mouse")
    table.remove("mouse")
    assert table.front == table.back == table.table[table.hash_function("duck") % 10]
    assert table.front.key == "duck"
    assert table.front.prevInsertion == table.front.nextInsertion == table.front.chain is None

    # removes the last added but not the only key in the table (without collision)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("lion")
    table.remove("lion")
    assert table.front == table.back == table.table[table.hash_function("duck") % 10]
    assert table.front.key == "duck"
    assert table.front.prevInsertion == table.front.nextInsertion == table.front.chain is None

    # removes the first added key in a chain (locations of "duck", "mouse", and "sheep" are the same)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("lion")
    table.add("mouse")
    table.add("sheep")
    table.remove("duck")
    assert table.front == table.table[table.hash_function("lion") % 10]
    assert table.back.key == "sheep"
    assert table.table[table.hash_function("duck") % 10].key == "mouse"
    assert table.back == table.table[table.hash_function("duck") % 10].chain
    assert table.table[table.hash_function("lion") % 10].prevInsertion is None

    # removes the last added key in a chain (locations of "duck", "mouse", and "sheep" are the same)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("mouse")
    table.add("lion")
    table.add("sheep")
    table.remove("sheep")
    assert table.front == table.table[table.hash_function("duck") % 10]
    assert table.back == table.table[table.hash_function("lion") % 10]
    assert table.back.nextInsertion is None

    # removes other keys (locations of "duck", "mouse", "butterfly", and "sheep" are all the same)
    table = LinkedHashTable(10)
    table.add("duck")
    table.add("mouse")
    table.add("butterfly")
    table.add("sheep")
    table.remove("mouse")
    assert table.front.key == "duck"
    assert table.back.key == "sheep"
    assert table.front.chain.key == table.front.nextInsertion.key == "butterfly"
    assert table.back.prevInsertion.prevInsertion == table.front
    print("Test case 2 passed!")


def test3():
    """
    This test case just generally tries all functions of LinkedHashTable.
    """
    print("\nTest Case 3:")
    table = LinkedHashTable(10)
    table.add("a")
    print("Although the load factor is now " + str(table.size / table.buckets) + ", which is less than ", end="")
    print("(1-MAX_LOAD), the minimum table size is 10, so the program will not reduce the table size.")
    table.remove("a")
    print("The table size is still", table.buckets, "after removing key 'a'")
    table.add("b")
    table.add("z")
    table.add("k")
    table.add("L")
    table.add("I")
    table.add("I")
    table.add("m")
    table.add("n")
    table.add("o")
    print("Table size:", table.buckets)
    print_set(table)
    # rehashing
    table.add("d")
    print("Table size:", table.buckets)
    print_set(table)
    table.remove("XD")
    table.remove("k")
    table.remove("b")
    table.remove("m")
    table.remove("k")
    table.remove("L")
    print("Table size:", table.buckets)
    print_set(table)
    # reduces table size
    table.remove("I")
    print("Table size:", table.buckets)
    print_set(table)

    print("\nTest case 3 passed!")


if __name__ == '__main__':
    test0()
    test1()
    test2()
    test3()
