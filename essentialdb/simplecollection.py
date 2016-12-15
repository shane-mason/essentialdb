__author__ = 'scmason'
import datetime
import random
import pickle
from essentialdb import SimpleDocument, QueryFilter
from essentialdb import QueryFilter


class SimpleCollection:
    """
    SimpleCollection implements a simple collection store with rudimentary disk
    persistence and all the logic required to query the store. This class can be
    extended to add or alter database functionality.
    """

    def __init__(self):
        self.documents = SimpleDocument()

    def insert_one(self, document):
        self.documents[document["_id"]] = SimpleDocument(document)
        return document["_id"]

    def find_one(self, query=None, filter=None):
        if query is None and filter is None:
            if self.documents:
                return self.documents[random.choice(list(self.documents.keys()))]
        else:
            results = self._query(query, filter)

            if len(results) > 0:
                return results[0]
        return []

    def _query(self, query, filter_function=None, limit=None):
        query_filter = QueryFilter(query)
        results = query_filter.execute_filter(self.documents, filter_function)
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
                del self.documents[item['_id']]
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

    def createIndex(self, index_document, options=None):
        for key in index_document:
            pass

    def _load(self, filepath):
        # TODO: Test if file exists
        try:
            with open(filepath, "rb") as fp:
                db = pickle.load(fp)
                self.documents = db["documents"]
        except:
            self.documents = {}
