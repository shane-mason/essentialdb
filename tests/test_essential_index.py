__author__ = 'scmason'
import unittest
from essentialdb import EssentialIndex, EssentialDB
from .document_generator import DocumentGenerator

data = {
    'a': {'f1': 'v1', 'f2': 'v2', 'f3': 100},
    'b': {'f1': 'v1a', 'f2': 'v2', 'f3': 10},
    'c': {'f1': 'v1b', 'f2': 'v2', 'f3': 1000},
}

class TestEssentialIndex(unittest.TestCase):

    def test_create_index_unique(self):
        index = EssentialIndex('f1')
        index_dict = index.create_index(data)
        print(index_dict)
        self.assertEqual(len(index_dict), 3)


    def test_create_index_multiple(self):
        index = EssentialIndex('f2')
        index_dict = index.create_index(data)
        self.assertEqual(len(index_dict), 1)

    def test_find_unique(self):
        index = EssentialIndex('f1')
        index.create_index(data)
        items = index.find(data, 'v1a')
        self.assertEqual(len(items), 1)

    def test_find_multiple(self):
        index = EssentialIndex( 'f2')
        index.create_index(data)
        items = index.find(data, 'v2')
        self.assertEqual(len(items), 3)

    def test_find_none(self):
        index = EssentialIndex( 'f2')
        index.create_index(data)
        items = index.find(data, 'v444')
        self.assertEqual(len(items), 0)

class TestEssentialIndexSpeed(unittest.TestCase):

    def XXsetUp(self):

        generator = DocumentGenerator()

        self.collection = EssentialDB("indextest.db")
        self.docs = []

        self.users = []

        for i in range(1000):
            self.users.append(generator.gen_email())


        #print(self.users)
        #'frerthhehme@reutme.co.uk', 'tinlor@ndve.org', 'gomst.iinrwa@parawmea.net', 'elaesote@hmoheohe.com', 'alhe@niciat.tv', 'mtihitk@heeatneomdcnrero.org', 'haitnemavo@ofonwe.eanecech.jp', 'pldonlelued@chedoren.fr', 'isma@wue995.com'
        template = {
            '_id': 'index',
            "gid": 'gid',
            "severity": ['minor', 'major', 'critical', 'blocker'],
            "title": 'sentence',
            "posts": 'small_int',
            "description": 'paragraph',
            "user": self.users
        }

        generator.set_template(template)
        self.docs = generator.gen_docs(50000)
        self.collection.insert_many(self.docs)
        self.collection.sync()

    @classmethod
    def setUpClass(cls):
        cls.collection = EssentialDB("indextest.db")
        cls.collection.createIndex({'severity': 'hashed'})
        cls.collection.createIndex({'user': 'hashed'})

    def test_find_many(self):
        q = {'severity': 'major'}
        results = self.collection.find(q)
        print(len(results))

    def test_find_several(self):
        q = {'user': 'tinlor@ndve.org'}
        results = self.collection.find(q)
        print(results[5])
        print(len(results))

    def test_find_one(self):
        q = {'_id': 25000}
        results = self.collection.find(q)
        print(len(results))
