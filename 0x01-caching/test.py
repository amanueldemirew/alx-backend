#!/usr/bin/env python3
"""
Test Module
"""
List = __import__('3-lru_cache').List
Node = __import__('3-lru_cache').Node
import unittest


class test_list(unittest.TestCase):
    """
    Test the list class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        new = List()
        self.assertEqual(new.head, None)
        self.assertEqual(new.tail, None)

    def test_insert_front(self):
        new = List()
        new.insert_front((3, 4))

        self.assertIsInstance(new.front(), Node)
        self.assertIsInstance(new.back(), Node)

        front_data = new.front().data
        self.assertEqual(front_data[0], 3)
        self.assertEqual(front_data[1], 4)

        back_data = new.back().data
        self.assertEqual(back_data[0], 3)
        self.assertEqual(back_data[1], 4)

    def test_insert_back(self):
        new = List()

        new.insert_end((3, 4))

        self.assertIsInstance(new.front(), Node)
        self.assertIsInstance(new.back(), Node)

        front_data = new.front().data
        self.assertEqual(front_data[0], 3)
        self.assertEqual(front_data[1], 4)

        back_data = new.back().data
        self.assertEqual(back_data[0], 3)
        self.assertEqual(back_data[1], 4)

    def test_pop_front(self):
        items = [(3, 5), (4, 6), (8, 9), ("hello", "world")]

        new = List()

        for item in items:
            new.insert_end(item)

        for i in range(len(items)):
            front_data = new.front().data
            self.assertEqual(front_data[0], items[i][0])
            self.assertEqual(front_data[1], items[i][1])
            new.pop_front()

    def test_pop_back(self):
        items = [(3, 5), (4, 6), (8, 9), ("hello", "world")]

        new = List()

        for item in items:
            new.insert_front(item)

        for i in range(len(items)):
            back_data = new.back().data
            self.assertEqual(back_data[0], items[i][0])
            self.assertEqual(back_data[1], items[i][1])
            new.pop_back()

    def test_erase_front(self):
        items = [(3, 5), (4, 6), (8, 9), ("hello", "world")]

        new = List()

        for item in items:
            new.insert_end(item)

        for i in range(len(items)):
            node = new.front()
            front_data = node.data
            self.assertEqual(front_data[0], items[i][0])
            self.assertEqual(front_data[1], items[i][1])
            new.erase(node)

    def test_erase_back(self):
        items = [(3, 5), (4, 6), (8, 9), ("hello", "world")]

        new = List()

        for item in items:
            new.insert_front(item)

        for i in range(len(items)):
            node = new.back()
            back_data = node.data
            self.assertEqual(back_data[0], items[i][0])
            self.assertEqual(back_data[1], items[i][1])
            new.erase(node)

    def test_erase_middle(self):
        left = [(3, 5), (4, 6), (8, 9)]
        right = [(45, 34), (45, 23), (45, 12)]
        middle = (456, 677)

        new = List()

        for l in left:
            new.insert_end(l)

        new.insert_end(middle)

        m_node = new.back()

        for r in right:
            new.insert_end(r)

        new.erase(m_node)
        for i in range(len(left) + len(right)):
            node = new.front()
            data = node.data if node else None
            self.assertNotEqual(data, middle)
            new.pop_front()
