from essentialdb import EssentialDB, SimpleCollection
import random
import string
import unittest

__author__ = 'scmason'

SYNC_DB_FILE = "sync_test_db"

class TestEssentialDB(unittest.TestCase):

    def setUp(self):
        self.collection = EssentialDB()
        self.docs = _gen_docs(10)

    def test_set_get(self):
        self.collection.set("my-test-number", 1)
        self.collection.set("my-test-string", "Hello")

        num = self.collection.get("my-test-number")
        text = self.collection.get("my-test-string")

        self.assertEqual(num, 1)
        self.assertEqual(text, "Hello")

    def test_insert_and_find_one(self):
        self.collection.insert_one(self.docs[0])
        response = self.collection.find_one()
        self.assertEqual(response["field 1"], self.docs[0]["field 1"])
        self.assertEqual(self.collection.count(), 1)

    def test_insert_many(self):
        self.collection.insert_many(self.docs)
        self.assertEqual(self.collection.count(), 10)

    def test_find_one_of_many_by_id(self):
        self.collection.insert_many(self.docs)
        response = self.collection.find_one({"_id": self.docs[0]["_id"]})
        self.assertEqual(response["_id"], self.docs[0]["_id"])

    def test_find_one_complex_query(self):
        self.collection.insert_many(self.docs)
        response = self.collection.find_one({"field 0": self.docs[5]["field 0"], "field 1": self.docs[5]["field 1"]})
        self.assertEqual(response["_id"], self.docs[5]["_id"])

    def test_find_one_complex_dot_query(self):
        self.collection.insert_many(self.docs)
        response = self.collection.find_one({"nested.n0": self.docs[5]["nested"]["n0"], "nested.n1": self.docs[5]["nested"]["n1"]})
        self.assertEqual(response["_id"], self.docs[5]["_id"])

    def test_find_one_filter(self):
        def filter(doc):
            if doc["field 0"] == "Hello":
                return True
            return False

        self.docs[5]["field 0"] = "Hello"
        self.collection.insert_many(self.docs)
        response = self.collection.find(filter=filter)
        self.assertEqual(response[0]["_id"], self.docs[5]["_id"])


    def test_find_or(self):
        self.collection.insert_many(self.docs)
        q = {"$or": [{"field 0": self.docs[5]["field 0"]}, {"field 1": self.docs[6]["field 1"]}]}
        response = self.collection.find(q)
        self.assertEqual(len(response), 2)


    def test_find_nor(self):
        self.collection.insert_many(self.docs)
        q = {"$nor": [{"field 1": self.docs[0]["field 1"]}, {"field 1": self.docs[1]["field 1"]}]}
        response = self.collection.find(q)
        self.assertEqual(len(response), 8)

    def test_find_and(self):
        self.collection.insert_many(self.docs)
        q = {"field 1": self.docs[0]["field 1"], "field 2": self.docs[0]["field 2"]}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_find_or_complex(self):
        self.docs[0]["number"] = 0
        self.docs[1]["number"] = 5
        self.docs[2]["number"] = 20
        self.docs[3]["number"] = 25

        self.collection.insert_many(self.docs)
        q = {"$or": [{"number": {"$eq": 5}}, {"number": {"$eq": 20}}]}
        response = self.collection.find(q)
        self.assertEqual(len(response), 2)

    def test_find_nor_complex(self):
        self.docs[0]["number"] = 0
        self.docs[1]["number"] = 5

        self.collection.insert_many(self.docs)
        q = {"$nor": [{"number": {"$eq": 10}}, {"number": {"$eq": 0}}]}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_find_and_complex(self):
        self.docs[0]["number"] = 0
        self.docs[0]["field 0"] = "Hello"
        self.docs[5]["number"] = 2
        self.docs[5]["field 0"] = "Hello"
        self.docs[7]["number"] = 4
        self.docs[7]["field 0"] = "Bye"

        self.collection.insert_many(self.docs)
        q = {"$and": [{"number": {"$lt": 2}}, {"field 0": {"$eq": "Hello"}}]}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)


    def test_update_one(self):
        self.collection.insert_many(self.docs)
        self.collection.update({"field 0": self.docs[5]["field 0"], "field 1": self.docs[5]["field 1"]}, {"field 2": "Hello"})
        find = self.collection.find_one({"field 2": "Hello"})
        self.assertEqual(find["_id"], self.docs[5]["_id"])

    def test_remove_one(self):
        self.collection.insert_many(self.docs)
        self.collection.remove({'fields 0': self.docs[5]["field 0"]})
        results = self.collection.find_one({'fields 0': self.docs[5]["field 0"]})
        self.assertEqual(results, [])

    def test_remove_many(self):
        self.docs[6]["number"] = 1
        self.docs[7]["number"] = 1
        self.collection.insert_many(self.docs)
        q = {"number": {"$ne": 1}}
        count = self.collection.remove(q)
        self.assertEqual(count, 8)



    def test_remove_all(self):
        self.collection.insert_many(self.docs)
        self.collection.remove()
        results = self.collection.count()
        self.assertEqual(results, 0)

    def test_eq(self):
        self.collection.insert_many(self.docs)
        q = {"field 1": {"$eq": self.docs[3]["field 1"]}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_gt(self):
        self.docs[6]["number"] = 11
        self.collection.insert_many(self.docs)
        q = {"number": {"$gt": 10}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_gte(self):
        self.docs[6]["number"] = 11
        self.collection.insert_many(self.docs)
        q = {"number": {"$gte": 11}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_lt(self):
        self.docs[6]["number"] = 9
        self.collection.insert_many(self.docs)
        q = {"number": {"$lt": 10}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_lte(self):
        self.docs[6]["number"] = 9
        self.collection.insert_many(self.docs)
        q = {"number": {"$lte": 9}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_ne(self):
        self.docs[6]["number"] = 9
        self.collection.insert_many(self.docs)
        q = {"number": {"$ne": 10}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 1)

    def test_in(self):
        self.docs[6]["number"] = 6
        self.docs[7]["number"] = 7
        self.collection.insert_many(self.docs)
        q = {"number": {"$in": [6, 7]}}
        response = self.collection.find(q)
        self.assertEqual(len(response), 2)

    def test_nin(self):
        self.docs[6]["number"] = 6
        self.docs[7]["number"] = 7
        self.collection.insert_many(self.docs)
        q = {"number": {"$nin": [6, 7]}}
        response = self.collection.find(q)
        self.assertEqual(len(response), len(self.docs)-2)


    def test_nin(self):
        self.docs[6]["number"] = 6
        self.docs[7]["number"] = 7
        self.collection.insert_many(self.docs)
        q = {"number": {"$nin": [6, 7]}}
        response = self.collection.find(q)
        self.assertEqual(len(response), len(self.docs)-2)

    def xtest_create_index(self):
        self.collection.createIndex({"field 1": 1})
        q = {"field 1": {"$eq": self.docs[5]["field 1"]}}
        response = self.collection.find(q)
        #self.assertEqual(len(response), 1)

    def test_sync_load(self):
        with EssentialDB(collection=SimpleCollection(), filepath=SYNC_DB_FILE) as db:
            docs = _gen_docs(10)
            db.insert_many(docs)

        with EssentialDB(collection=SimpleCollection(), filepath=SYNC_DB_FILE) as db2:
            find = db2.find_one({"_id": docs[5]["_id"]})
            self.assertEqual(find["_id"], docs[5]["_id"])

    @classmethod
    def tearDownClass(cls):
        import os
        os.remove(SYNC_DB_FILE)


def _gen_docs(count=1):
    docs = []

    def _gen_text():
        return ''.join(random.choice(string.ascii_letters) for k in range(random.randint(3, 8)))

    for i in range(count):
        doc = {
            "field 0": _gen_text(),
            "field 1": _gen_text(),
            "field 2": _gen_text(),
            "number": 10,
            "nested": {
                "n0": _gen_text(),
                "n1": _gen_text(),
                "n2": 10
            }
        }

        docs.append(doc)
    return docs


if __name__ == '__main__':
    unittest.main()
