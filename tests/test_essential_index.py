__author__ = 'scmason'
import unittest
from essentialdb import EssentialIndex, EssentialDB
from .document_generator import DocumentGenerator


class TestEssentialIndex(unittest.TestCase):
    def _gen_data(self):
        return dict({
            'a': {'f1': 'v1', 'f2': 'v2', 'f3': 100, '_id': "a"},
            'b': {'f1': 'v1a', 'f2': 'v2', 'f3': 10, '_id': "b"},
            'c': {'f1': 'v1b', 'f2': 'v2', 'f3': 1000, '_id': "c"},
        })

    def test_create_index_unique(self):
        data = self._gen_data()
        index = EssentialIndex('f1')
        index_dict = index.create_index(data)
        self.assertEqual(len(index_dict), 3)

    def test_create_index_multiple(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index_dict = index.create_index(data)
        self.assertEqual(len(index_dict), 1)

    def test_find_unique(self):
        data = self._gen_data()
        index = EssentialIndex('f1')
        index.create_index(data)
        items = index.find(data, 'v1a')
        self.assertEqual(len(items), 1)

    def test_find_multiple(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index.create_index(data)
        items = index.find(data, 'v2')
        self.assertEqual(len(items), 3)

    def test_find_none(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index.create_index(data)
        items = index.find(data, 'v444')
        self.assertEqual(len(items), 0)

    def test_update_new(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index.create_index(data)
        data['new'] = {'f1': 'v1a', 'f2': 'newval', 'f3': 10, "_id": "new"}
        index.update_index(data['new'])
        items = index.find(data, 'newval')
        self.assertEqual(len(items), 1)

    def test_update_existing(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index.create_index(data)
        data['b'] = {'f1': 'v1a', 'f2': 'updatedval', 'f3': 10, "_id": "b"}
        index.update_index(data['b'])
        items = index.find(data, 'updatedval')
        self.assertEqual(len(items), 1)

    def test_remove_existing(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index.create_index(data)
        items = index.find(data, 'v2')
        self.assertEqual(len(items), 3)
        removed = index.remove_from_index(data['b'])
        self.assertTrue(removed)
        items = index.find(data, 'v2')
        self.assertEqual(len(items), 2)

    def test_remove_non_existing(self):
        data = self._gen_data()
        index = EssentialIndex('f2')
        index.create_index(data)
        removed = index.remove_from_index({'_id': 'doesnt exist'})
        self.assertFalse(removed)
        removed = index.remove_from_index({'no id': 'doesnt exist'})
        self.assertFalse(removed)

