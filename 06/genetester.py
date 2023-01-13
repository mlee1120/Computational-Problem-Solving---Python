"""
file: genetester.py
description: CSCI 603 hw6 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
"""

import unittest


class TestInitOfLinkedNode(unittest.TestCase):
    def test___init__(self):
        """
        This function tests __init__ from LinkedNode.
        """
        from hw6.dnalist import LinkedNode
        a = LinkedNode(1)
        # tests value
        self.assertEqual(a.value, 1)
        # tests link
        self.assertEqual(a.link, None)
        b = LinkedNode(2, a)
        # tests value
        self.assertEqual(b.value, 2)
        # tests link and value
        self.assertEqual(b.link.value, 1)


class TestInit(unittest.TestCase):
    def test___init__(self):
        """
        This function tests __init__ from DNAList.
        """
        from hw6.dnalist import DNAList

        # The constructor works with valid argument
        self.assertTrue(isinstance(DNAList(), DNAList))

        # The constructor works with valid argument
        self.assertTrue(isinstance(DNAList("ACGT"), DNAList))

        # The constructor works with invalid argument
        self.assertTrue(isinstance(DNAList("KK"), DNAList))

        # The constructor works with invalid argument
        self.assertTrue(isinstance(DNAList(123), DNAList))


class TestEq(unittest.TestCase):
    def test___eq__(self):
        """
        This function tests __eq__ from DNAList.
        """
        from hw6.dnalist import DNAList

        # empty DNALists are equal
        self.assertEqual(DNAList(), DNAList())

        a = DNAList('ACG')
        b = DNAList('ACG')
        # two DNALists with the same elements and order are equal
        self.assertTrue(a == b)

        c = DNAList('GAC')
        # two DNALists with the same elements but different order are not equal
        self.assertFalse(a == c)


class TestStr(unittest.TestCase):
    def test___str__(self):
        """
        This function tests __str__ from DNAList.
        """
        from hw6.dnalist import DNAList

        # checks if __str__ returns expected result
        self.assertEqual(DNAList('ACGT').__str__(), 'ACGT')


class TestAppend(unittest.TestCase):
    def test_append(self):
        """
        This function tests append from DNAList.
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        a.append('A')
        # an empty DNAList appends a single character
        self.assertEqual(a, DNAList('A'))

        b = DNAList()
        b.append('a')
        # ignores case
        self.assertEqual(b, DNAList('A'))

        c = DNAList()
        c.append('A')
        c.append('C')
        # an empty DNAList appends a single character and then another
        self.assertEqual(c, DNAList('AC'))

        d = DNAList()
        d.append('K')
        d.append(123)
        # an empty DNAList appends invalid objects is still an empty DNAList
        self.assertEqual(d, DNAList())


class TestJoin(unittest.TestCase):
    def test_join(self):
        """
        This function tests join from DNAList.
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        b = DNAList()
        a.join(b)
        # a DNAList remains the same while joined with an empty DNAList
        self.assertEqual(a, DNAList())

        c = DNAList('ACG')
        d = DNAList('T')
        c.join(d)
        # join functions well
        self.assertEqual(c, DNAList('ACGT'))


class TestSplice(unittest.TestCase):
    def test_splice(self):
        """
        This function tests splice from DNAList.
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        a.splice(0, DNAList('AC'))
        # an empty DNAList can not be spliced
        self.assertEqual(a, DNAList())

        b = DNAList('ACG')
        b.splice(0, DNAList('T'))
        # splice works at every position in a DNAList
        self.assertEqual(b, DNAList('ATCG'))

        c = DNAList('ACG')
        c.splice(2, DNAList('T'))
        # splice works at every position in a DNAList
        self.assertEqual(c, DNAList('ACGT'))

        d = DNAList('ACG')
        d.splice(-1, DNAList('T'))
        # splice works at every position in a DNAList (len(DNAList)-1)
        self.assertEqual(d, DNAList('ACGT'))

        e = DNAList('ACG')
        e.splice(-3, DNAList('T'))
        # splice works at every position in a DNAList (len(DNAList)-3)
        self.assertEqual(e, DNAList('ATCG'))

        f = DNAList('ACG')
        f.splice(0, DNAList())
        # a DNAList remains the same if spliced with an empty DNAList
        self.assertEqual(f, DNAList('ACG'))

        g = DNAList('ACG')
        g.splice('a', DNAList('T'))
        g.splice(0, 12)
        # a DNAList remains the same if the arguments are invalid
        self.assertEqual(g, DNAList('ACG'))


class TestSnip(unittest.TestCase):
    def test_snip(self):
        """
        This function tests snip from DNAList.
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        a.snip(0, 0)
        a.snip(0, 1)
        a.snip('s', 1)
        a.snip(0, 's')
        # a DNAList remains the same if the arguments are invalid
        self.assertEqual(a, DNAList())

        b = DNAList('AC')
        b.snip(0, 1)
        # snip works at every position in a DNAList
        self.assertEqual(b, DNAList('C'))

        c = DNAList('ACGT')
        c.snip(1, 3)
        # snip works at every position in a DNAList
        self.assertEqual(c, DNAList('AT'))


class TestReplace(unittest.TestCase):
    def test_replace(self):
        """
        This function tests replace from DNAList.
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        b = DNAList('T')
        a.replace('A', b)
        # an empty DNAList will not be replaced because there is no target sequence in it
        self.assertEqual(a, DNAList())

        c = DNAList('ACG')
        c.replace('A', b)
        # replace works with a single character
        self.assertEqual(c, DNAList('TCG'))

        d = DNAList('ACGTACGT')
        d.replace('C', b)
        # all target sequences will be replaced
        self.assertEqual(d, DNAList('ATGTATGT'))

        e = DNAList('ACGACG')
        f = DNAList('TCA')
        e.replace('AC', f)
        # replace works with two or more characters
        self.assertEqual(e, DNAList('TCAGTCAG'))

        g = DNAList('ACGT')
        g.replace('AC', 123)
        g.replace('AC', 'TA')
        g.replace(132, b)
        # a DNAList remains the same if the arguments are invalid
        self.assertEqual(g, DNAList('ACGT'))


class TestCopy(unittest.TestCase):
    def test_copy(self):
        """
        This function tests copy from DNAList.
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        b = a.copy()
        # checks if the original DNAList and the copied one are equal
        self.assertTrue(a == b)

        b.append('A')
        # checks if there are two DNALists which are equal or there are just two variable pointing to the same objects
        self.assertFalse(a == b)


class TestSizeAndSizeToEnd(unittest.TestCase):
    def test_sizeAnd_size_to_end(self):
        """
        This function tests size and _size_to_end from DNAList
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        # an empty DNAList should have a size of 0
        self.assertTrue(a.size() == 0)

        b = DNAList('ACG')
        # the size of a DNAList is the number of nodes in the DNAList
        self.assertTrue(b.size() == 3)


class TestEmpty(unittest.TestCase):
    def test_empty(self):
        """
        This function tests empty from DNAList.
        :return:
        """
        from hw6.dnalist import DNAList

        a = DNAList()
        # returns True if the DNAList is empty
        self.assertTrue(a.empty())

        b = DNAList('ACG')
        # returns False if the DNAList is not empty
        self.assertFalse(b.empty())


"""
main conditional guard
The following condition checks whether we are running as a script.
If the file is being imported, don't run the test code.
"""
if __name__ == '__main__':
    unittest.main()
