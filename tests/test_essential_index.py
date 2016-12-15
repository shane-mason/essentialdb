__author__ = 'scmason'
import unittest
from essentialdb import EssentialIndex

data = {
    'a': {'f1': 'v1', 'f2': 'v2'},
    'b': {'f1': 'v1a', 'f2': 'v2'},
    'c': {'f1': 'v1b', 'f2': 'v2'},
}

class TestEssentialIndex(unittest.TestCase):

    def test_create_index_unique(self):
        index = EssentialIndex()
        index_dict = index.create_index(data, 'f1')
        self.assertEqual(len(index_dict), 3)


    def test_create_index_multiple(self):
        index = EssentialIndex()
        index_dict = index.create_index(data, 'f2')
        self.assertEqual(len(index_dict), 1)

    def test_find_unique(self):
        index = EssentialIndex()
        index.create_index(data, 'f1')
        items = index.find(data, 'v1a')
        self.assertEqual(len(items), 1)

    def test_find_multiple(self):
        index = EssentialIndex()
        index.create_index(data, 'f2')
        items = index.find(data, 'v2')
        self.assertEqual(len(items), 3)

    def test_find_none(self):
        index = EssentialIndex()
        index.create_index(data, 'f2')
        items = index.find(data, 'v444')
        self.assertEqual(len(items), 0)
