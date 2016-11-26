from essentialdb import EssentialDB, SimpleCollection
import unittest
import time
__author__ = 'scmason'

class Timer:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start


def import_data(count):
    import glob
    import json
    ls = glob.glob("tests/mock-data/*.json")
    data = []

    for i in range(count):
        with open(ls[i], 'r', encoding="utf8") as fp:
            as_str = fp.read()
            as_ls = json.loads(as_str)
            data += as_ls

    return data

def run_test(function, iterations, args):
    elapsed = 0.0
    for i in range(iterations):
        with Timer() as t:
            if len(args) == 0:
                function()
            elif len(args) == 1:
                function(args[0])
            else:
                function(args[0], args[1])
        elapsed += t.secs

    return elapsed/iterations

PERFORMANCE_DB_FILE = "performance_test_db"
TEST_ITERATIONS = 10
averages = {}

class TestEssentialDBPerformance(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestEssentialDBPerformance, self).__init__(*args, **kwargs)
        self.collection = EssentialDB(filepath=PERFORMANCE_DB_FILE)

    def test_1_insert(self):
        data = import_data(10)
        with Timer() as t:
            self.collection.insert_many(data)
        averages["insert"] = t.secs
        self.assertLess(t.secs, 0.14)

    def test_2_find_one(self):
        average = run_test(self.collection.find_one, TEST_ITERATIONS, [{"gid": "1850ca08-f88c-4155-b89f-b5513a1383aa"}])
        averages['find_one'] = average
        self.assertLess(average, 0.012)

    def test_3_find_many(self):
        average = run_test(self.collection.find, TEST_ITERATIONS, [{"gender": "Female"}])
        averages['find_many'] = average
        self.assertLess(average, 0.015)

    def test_4_complex_and(self):
        average = run_test(self.collection.find, TEST_ITERATIONS, [{"first_name":"Anne","gender": "Female"}])
        averages['complex_and'] = average
        self.assertLess(average, 0.015)

    def test_5_complex_or(self):
        average = run_test(self.collection.find, TEST_ITERATIONS, [{"$or":[{"last_name":"Nguyen"}, {"first_name": "Jack"}]}])
        averages['complex_or'] = average
        self.assertLess(average, 0.016)

    def test_6_update_one(self):
        q = [{"gid": "04f60316-beea-4f6e-8a1d-3a02b3e972b4"}, {'first_name' : "Awesome"}]
        average = run_test(self.collection.update, TEST_ITERATIONS, q)
        averages['update_one'] = average
        self.assertLess(average, 0.015)

    def test_7_update_many(self):
        q = [{"gender": "Female"},{'first_name' : "Girl"}]
        average = run_test(self.collection.update, TEST_ITERATIONS, q)
        averages['update_many'] = average
        self.assertLess(average, 0.015)

    def test_8_sync(self):
        import os
        average = run_test(self.collection.sync, TEST_ITERATIONS, [])
        size = os.path.getsize(PERFORMANCE_DB_FILE)
        averages['sync'] = average
        averages['size'] = size
        self.assertLess(average, 0.06)


    def test_9_remove(self):
        average = run_test(self.collection.remove, 1, [])
        averages['remove'] = average
        self.assertLess(average, 0.015)

    @classmethod
    def tearDownClass(self):
        import os

        size = os.path.getsize(PERFORMANCE_DB_FILE)
        averages['size'] = size

        collection = EssentialDB(filepath=PERFORMANCE_DB_FILE)
        collection.remove()
        collection.sync()
        os.remove(PERFORMANCE_DB_FILE)
        #now we should save stats...
        print(averages)
