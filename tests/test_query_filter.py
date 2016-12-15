import unittest
from essentialdb import QueryFilter


class TestQueryFilter(unittest.TestCase):
    def test_equality_expression(self):
        q = {'a': 'b'}
        qf = QueryFilter(q)
        self.assertEqual(len(qf.expressions), 1)
        self.assertEqual(qf.expressions[0].field, 'a')
        self.assertEqual(qf.expressions[0].value, 'b')

    def test_equality_expressions(self):
        q = {'a': 'b', 'c': 'd', 'e': 'f'}
        qf = QueryFilter(q)
        self.assertEqual(len(qf.expressions), 3)

    def test_comparison_operators(self):
        q = {'a': {'$eq': 'b'}}
        qf = QueryFilter(q)
        self.assertEqual(len(qf.expressions), 1)

    def test_logical_operators(self):
        q = {"$or": [{'a': 'b'}, {'c': 'd'}, {'e': 'f'}]}
        qf = QueryFilter(q)
        self.assertEqual(len(qf.expressions), 1)

    def test_complex(self):
        q = {"$or": [{'a': {'$eq': 'b'}}, {'c': 'd'}, {'e': 'f'}], 'e': 'f'}
        qf = QueryFilter(q)
        self.assertEqual(len(qf.expressions), 2)
