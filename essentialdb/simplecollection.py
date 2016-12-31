__author__ = 'scmason'
import datetime
import random
import pickle
from essentialdb import SimpleDocument
from essentialdb import QueryFilter
from essentialdb import EssentialIndex


class SimpleCollection:
    """
    SimpleCollection implements a simple collection store with rudimentary disk
    persistence and all the logic required to query the store. This class can be
    extended to add or alter database functionality.
    """

    def __init__(self):
        self.documents = SimpleDocument()
        self.indexes = {}

    def insert_one(self, document):
        self.documents[document["_id"]] = SimpleDocument(document)
        for field in self.indexes:
            self.indexes[field].update_index(self.documents[document["_id"]])

        return document["_id"]

    def find_one(self, query=None, filter=None):
        if query is None and filter is None:
            if self.documents:
                return self.documents[random.choice(list(self.documents.keys()))]
        else:
            results = self._query(query, filter)

            if len(results) > 0:
                return results[0]
        return None

    def _query(self, query, filter_function=None, limit=None):
        query_filter = QueryFilter(query)
        results = query_filter.execute_filter(self.documents, filter_function, self.indexes)
        return results

    def find(self, query=None, filter=None):
        return self._query(query, filter)

    def update(self, query, update):
        to_update = self._query(query)
        for document in to_update:
            for key in update:
                document[key] = update[key]
            for field in self.indexes:
                self.indexes[field].update_index(document)
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
            for document in to_delete:
                del self.documents[document['_id']]
                for field in self.indexes:
                    self.indexes[field].remove_from_index(document)
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
                "indexes": self.indexes,
                "documents": self.documents
            }
            pickle.dump(output, fp)

    def createIndex(self, index_document, options=None):
        for key in index_document:
            if index_document[key] == "hashed":
                index = EssentialIndex(key)
                index.create_index(self.documents)
                self.indexes[key] = index

    def dropIndexes(self):
        self.indexes.clear()

    def _load(self, filepath):
        # TODO: Test if file exists
        try:
            with open(filepath, "rb") as fp:
                db = pickle.load(fp)
                self.documents = db["documents"]
        except:
            self.documents = {}
