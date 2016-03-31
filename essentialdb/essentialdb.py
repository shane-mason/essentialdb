"""
.. module:: essentialdb
   :platform: Unix, Windows
   :synopsis: Embedded python document database

.. moduleauthor:: Shane C Mason <shane.c.mason@gmail.com>

"""

from essentialdb import SimpleCollection, Keys

import uuid


class EssentialDB:
    """
    EssentialDB class is the front end interface to the EssentialDB database. A BreezeBlock instance is equivalent to
    a collection.

    To initiate with the 'module level' universal collection and no disk persistence, use:

        from essentialdb import EssentialDB

        blocks = EssentialDB()

    When using the universal collection, all other BreezeBlock instances will recieve the same store.

    To initiate with separate collections, initiate like so:

        books = EssentialDB(collection=SimpleCollection())
        authors = EssentialDB(collection=SimpleCollection())

    For deferred disk persistence, use filepath:

        books = EssentialDB(collection=SimpleCollection(), filepath="mydatabase.db")


    """
    def __init__(self, collection=SimpleCollection(), filepath=None, autosync=False):
        self.collection = collection
        self.filepath=filepath
        if filepath is not None:
            self.collection._load(filepath)

        self.autosync = autosync

    def __del__(self):
        #TODO: Test if dirty before forcing sync
        #self.sync()
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.sync()

    def insert_one(self, document, _id=None):
        """
        Inserts one document into the collection. If the document already
        contains an _id, or one is specified in the key word arguments, it will
        be used as the documents primary identifier on insert.  If a document
        with the same identifier already exists, this operation will overwrite
        the existing document. If '_id' is not specified, a globally unique
        identifier will be generated and inserted.

        Args:
            document (dict) The document to insert.

        Kwargs:
            _id (str): If specified, _id will be used as for the primary document
            identifier. If a document with the same identifier exists, this
            operation will overwrite the existing document.

        Returns:
            The unique identifier for the inserted document

        Example:

            author = {'first': 'Langston', 'last': 'Hughes', 'born': 1902}
            EssentialDB().insert_one(author)

        """
        if _id is not None:
            document[Keys.id] = _id
        elif Keys.id not in document:
            document[Keys.id] = str(uuid.uuid4())

        results = self.collection.insert_one(document)
        self._cleanup()
        return results

    def _cleanup(self):
        """
        Internal function, used to finalize any outstanding tasks after inserts
        and other operations that alter the state of the database.
        """
        if self.autosync:
            self.sync()
        pass

    def set(self, key, value):
        """
        Sets key in the current collection to be equal to the provided value.
        This is a short-cut function designed designed to provide EssentialDB
        with semantics similar to a transparent key/value store (like redis).
        Under the hood, this is creating a document from 'value' and assigning
        it the _id of 'key'. Any additional sets will overwrite the current
        value.

        Args:
            key (string) The key for the value to be inserted.
            value (dict) The value to set.

        Returns:
            The unique identifier for the inserted document
        """
        self.collection.set(key, value)
        self._cleanup()
        return key

    def get(self, key):
        """
        Get a document previously inserted by 'set' or any document whose _id is
        equal to 'key'. This is a short-cut function designed designed to provide
        EssentialDB with semantics similar to a transparent key/value store
        (like redis).

        Args:
            key (string) The key (_id) of the item to be retrieved.

        Returns:
            The document (dict) if found.

        """
        return self.collection.get(key)

    def insert_many(self, documents):
        """
        Inserts a list of documents into the collection using the same process as oulined for insert_one

        Args:
            documents (list) A list of documents (dict) to insert.

        Returns
            The number of documents inserted into the store.

        Example:

            authors = [{'first': 'Langston', 'last': 'Hughes', 'born': 1902},
                       {'first': 'Ezra', 'last': 'Pound', 'born': 1885}]
            EssentialDB().insert_many(authors)

        """
        for doc in documents:
            self.insert_one(doc)
        self._cleanup()
        return True

    def find_one(self, query=None, filter=None):
        """
        Finds one document that matches the query. If multiple documents match (or query is not specified), a single
        random document is returned from the result set.

        Kwargs:
            query (dict): If specified, the query to be ran on the collection.

        Returns
            A single matching document or None if no documents match query or the collection is empty.

        Example:

            document = EssentialDB().find_one({'first': 'Ezra', 'last': 'Pound'})

        """
        return self.collection.find_one(query, filter)

    def find(self, query={}, filter=None):
        """
        Finds all documents that match the query. If query is not specified, all documents in the collection will be
        returned.

        Kwargs:
            query (dict): If specified, the query to be ran on the collection.
            filter (fund): If specified, results will be ran through provided function before inclustion in results
        Returns:
            A list of matching documents or None if no documents match query or the collection is empty.

        Example:

            documents = EssentialDB().find({'color': 'blue'}})

        """

        return self.collection.find(query, filter)

    def update(self, query, update):
        """
        Applies the specified update to all documents in the collection that match the specified query.

        Args:
            query (dict): The query to be ran on the collection. An empty dictionary {} matches all.
            update (dict): The update to be ran on matching documents.

        Returns:
            The number of documents updated.

        Example:

            updated = EssentialDB().update({'year': {'$gt': 1900}}, {'period': 'Modern'})

        """
        results = self.collection.update(query, update)
        self._cleanup()
        return results

    def count(self):
        """
        Get the total number of documents in the collection.
        """
        return self.collection.count()

    def remove(self, query=None):
        """
        Remove all documents that match query. If query is not specified, all documents will be removed.

        Kwargs:
            query (dict): The query to be ran on the collection. An empty dictionary {} matches all.

        Returns:
            The number of documents removed.

        Example:

            removed = EssentialDB().remove({'period':'Modern'))

        """
        results = self.collection.remove(query)
        self._cleanup()
        return results

    def sync(self):
        """
        Send a hint to the database that it should consider writing to disk soon.

        Currently, this blocks and writes to disk immediately.
        """
        return self.collection.sync(self.filepath)

    def branch(self):
        """
        NOT IMPLEMENTED!!! CREATE A BRANCH...
        """
        raise NotImplementedError("Not implemented yet...")
