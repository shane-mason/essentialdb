__author__ = 'scmason'

import datetime

import random
import pickle
from essentialdb import Keys


class SimpleCollection:
    """
    SimpleCollection implements a simple collection store with rudimentary disk
    persistence. 

    """


    def __init__(self):
        self.documents = {}
        self.queue = None
        self.writer = None

    #        self.setup(cPickle_writer)

    def setup(self, writer_function, filepath="bb.out"):
        self.filepath = filepath

    #        self.queue = Queue()
    #        self.writer = Process(target=writer_function, args=(self.queue,filepath) )
    #        self.writer.start()

    def insert_one(self, document):
        self.documents[document["_id"]] = document
        return document["_id"]

    def insert_many(self, documents):
        pass

    def find_one(self, query=None, filter=None):
        if query is None and filter is None:
            if self.documents:
                return self.documents[random.choice(list(self.documents.keys()))]
        else:
            results = self._query(query, filter)

            if len(results) > 0:
                return results[0]
        return None

    def _query(self, query, filter=None, limit=None):
        """

        """


        def _test_comparison(field, query, doc):

            try:
                # then is is something like  { "$eq": 12 }
                operator = list(query.keys())[0]
                compareto = query[operator]
                return Keys.comparisons[operator](doc[field], compareto)
            except:
                return False


        def _test_or(query_list, doc):
            for q in query_list:
                for field in q:
                    if isinstance(q[field], dict) and   _test_comparison(field, q[field], doc):
                        return True
                    elif field in doc and q[field] == doc[field]:
                        return True
            return False

        def _test_nor(query_list, doc):
            for q in query_list:
                for field in q:
                    if isinstance(q[field], dict) and  _test_comparison(field, q[field], doc):
                        return False
                    elif field in doc and q[field] == doc[field]:
                        return False
            return True

        def _test_and(query_list, doc):
            for q in query_list:
                for field in q:
                    if isinstance(q[field], dict):
                        if not _test_comparison(field, q[field], doc):
                            return False
                    elif field not in doc or q[field] != doc[field]:
                        return False
            return True


        results = []
        # first, is it by id?
        if Keys.id in query:
            if query[Keys.id] in self.documents:
                matches = True
                if filter:
                    matches = filter(self.documents[query[Keys.id]])
                if matches:
                    results.append(self.documents[query[Keys.id]])
        else:
            for _id in self.documents:
                matches = True
                for key in query:
                    if key == Keys._or:
                        matches = _test_or(query[key], self.documents[_id])
                    elif key == Keys._nor:
                        matches = _test_nor(query[key], self.documents[_id])
                    elif key == Keys._and:
                        matches = _test_and(query[key], self.documents[_id])
                    elif isinstance(query[key], dict):
                        #something like {"field': {'$eq': 'something'}}
                        matches = _test_comparison(key, query[key], self.documents[_id])
                    elif key not in self.documents[_id] or query[key] != self.documents[_id][key]:
                        matches = False

                    if not matches:
                        break

                if matches:
                    if filter:
                        matches = filter(self.documents[_id])
                    if matches:
                        results.append(self.documents[_id])


        return results

    def find(self, query=None, filter=None):
        return self._query(query, filter)

    def update(self, query, update):
        to_update = self._query(query)
        for item in to_update:
            for key in update:
                item[key] = update[key]
        return len(to_update)

    def count(self):
        return len(self.documents)

    def remove(self, query=None):
        count = 0
        if query is None:
            count = self.count()
            self.documents = {}
        else:
            to_delete = self._query(query)
            count = len(to_delete)
            for item in to_delete:
                del self.documents[item]
        return count

    def set(self, key, value):
        self.documents[key] = value

    def get(self, key):
        if key in self.documents:
            return self.documents[key]
        return None

    def sync(self, filepath):

        with open(filepath, "wb") as fp:
            output = {
                "meta": {
                    "timestamp": datetime.datetime.now()
                },
                "indexes": None,
                "documents": self.documents
            }
            pickle.dump(output, fp)

    def _load(self, filepath):
        # TODO: Test if file exists
        try:
            with open(filepath, "rb") as fp:
                db = pickle.load(fp)
                self.documents = db["documents"]
        except:
            self.documents = {}
