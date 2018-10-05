

from essentialdb import LocalCollection
from .essential_oid import EssentialOID

class Collection:

    def __init__(self,  documents,  threading_lock,  onsync_callback,  autosync=False, name=None):
        """

        Kwargs:
            filepath (str): Database file path, will be created if it doesn't exist.
            collection (Collection): Defaults to LocalCollection

        Returns:
            The unique identifier for the inserted document

        Example::

            library_db = EssentialDB(filepath="library.db")
            authors = library_db.authors
            books = library.books

        """

        self.collection = LocalCollection(documents)
        self.sync = onsync_callback
        self.threading_lock = threading_lock
        self.autosync = autosync
        self.collection_name = name
        self.dirty = False

    def __del__(self):
        # TODO: Test if dirty before forcing sync
        # self.sync()
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.dirty:
            self.sync()

    def __repr__(self):
        return self.collection.__class__.__name__ + ":" + str(self.collection_name)

    def _get_raw_documents(self):
        return self.collection._get_raw_documents()

    def insert_one(self, document):
        """
        Inserts one document into the collection. If the document already
        contains an _id, or one is specified in the key word arguments, it will
        be used as the documents primary identifier on insert.  If a document
        with the same identifier already exists, this operation will overwrite
        the existing document. If '_id' is not specified, a globally unique
        identifier will be generated and inserted.

        Args:
            document (dict) The document to insert.

        Returns:
            The unique identifier for the inserted document

        Example::

            with library_db.authors as author_collection:
                #documents are just dictionaries
                author = {'first': 'Langston', 'last': 'Hughes', 'born': 1902}
                author_collection.insert_one(author)

        """
        if "_id" not in document:
            document["_id"] = str(EssentialOID.generate_next_id())

        with self.threading_lock:
            results = self.collection.insert_one(document)

        self._cleanup()
        return results

    def _cleanup(self):
        """
        Internal function, used to finalize any outstanding tasks after inserts
        and other operations that alter the state of the database.
        """
        self.dirty = True
        if self.autosync:
            self.sync()


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

        Example::
            with my_db.cache as request_cache:
                request_cache.set( request.url, response.text )
        """
        with self.threading_lock:
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

        Example::

            with my_db.cache as request_cache:
                response.text = request_cache.get( request.url )

        """
        return self.collection.get(key)

    def insert_many(self, documents):
        """
        Inserts a list of documents into the collection using the same process as oulined for insert_one

        Args:
            documents (list) A list of documents (dict) to insert.

        Returns
            The number of documents inserted into the store.

        Example::

            with library_db.authors as author_collection:
                authors = [{'first': 'Langston', 'last': 'Hughes', 'born': 1902},
                {'first': 'Ezra', 'last': 'Pound', 'born': 1885}]
                author_collection.insert_many(authors)

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

        Example::

            with library_db.authors as author_collection:
                document = author_collection.find_one({'first': 'Ezra', 'last': 'Pound'})

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

        Example::

            with library_db.authors as author_collection:
                document = author_collection.find({'last': 'Smith'})

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

        Example::

            with library_db.books as book_collection:
                updated = book_collection.update({'year': {'$gt': 1900}}, {'period': 'Modern'})

        """
        with self.threading_lock:
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

        Example::

            with library_db.books as book_collection:
                document = book_collection.remove({'period': 'Modern'})
        """
        with self.threading_lock:
            results = self.collection.remove(query)
        self._cleanup()
        return results

    def createIndex(self, index, options=None):
        """
        Create an index.
        """
        results = self.collection.createIndex(index, options)
        self._cleanup()
        return results

    def dropIndexes(self):
        """
        Drop  all indexes.
        """
        results = self.collection.dropIndexes()
        self._cleanup()
        return results

    def _get_collection_documents_raw(self):
        return self.collection.documents

