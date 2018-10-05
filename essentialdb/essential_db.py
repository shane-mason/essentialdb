"""
.. module:: essentialdb
   :platform: Unix, Windows
   :synopsis: Embedded python document database

.. moduleauthor:: Shane C Mason <shane.c.mason@gmail.com>

"""

from essentialdb import PickleSerializer
from essentialdb import Collection
import datetime
from threading import Lock


class EssentialDB:

    def __init__(self, filepath=None, serializer=None, autosync=False):
        """

        EssentialDB class is the front end interface to the EssentialDB database::

            from essentialdb import EssentialDB

            # create or open the database
            db = EssentialDB(filepath="my.db")

            # get (or create) the collection like pymongo
            authors = db.authors

            # slightly safer way
            authors = db.get_collection('authors', create=False)

            #insert a document into the database
            authors.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902});

            #find some entries
            results = authors.find({'last':'Hughes'}

            #commit the changes to disk
            authors.sync()


        You can also use with semantics to assure that the database is closed and synced on exit::

            with EssentialDB(filepath="my.db").authors as authors:

                data = [{'first': 'Langston', 'last': 'Hughes', 'born': 1902},
                {'first': 'Ezra', 'last': 'Pound', 'born': 1885}]

                authors.insert_many(data)

        """

        self.threading_lock = Lock()
        self.collections = {}
        self.filepath = filepath
        self.autosync = autosync

        if serializer is None:
            serializer = PickleSerializer()
        self.serializer = serializer

        if self.filepath is not None:
            with self.threading_lock:
                self._load()

    def __getattr__(self, name):
        return self.get_collection(name)

    def __repr__(self):
        return "EssentialDB: " + str(self.filepath)

    def get_collection(self, name='default', create=True):
        if name not in self.collections:
            if create:
                self.collections[name] = Collection({}, self.threading_lock, self.sync, self.autosync, name)
            else:
                return None
        return self.collections[name]

    def get_collection_names(self):
        return list(self.collections.keys())

    def _load(self):
        # TODO: Test if file exists
        try:
            file_db = self.serializer.load(self.filepath)
            if 'collections' in file_db:
                self.collections = {}
                for collection in file_db['collections']:
                    self.collections[collection] = Collection(file_db['collections'][collection],
                                                              self.threading_lock, self.sync,
                                                              self.autosync)

            elif 'documents' in file_db:
                # Handle db files created pre v0.5"
                self.collections['default'] = file_db['documents']
            else:
                self.collections = {}
        except Exception as e:
            print(e)
            self.collections = {}

    def sync(self):
        output = {
            "meta": {
                "timestamp": datetime.datetime.now()
            },
            "collections": {}
        }
        for collection in self.collections:
            output['collections'][collection] = self.collections[collection]._get_raw_documents()
        self.serializer.dump(output, self.filepath)
