from essentialdb import PickleSerializer
from essentialdb import LocalCollectionProxy
import datetime
from threading import Lock


class EssentialLocal():
    def __init__(self, filepath=None, serializer=None, autosync=False):
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

    def get_collection(self, name='default', create=True):
        if name not in self.collections:
            if create:
                self.collections[name] = LocalCollectionProxy({}, self.threading_lock, self.sync, self.autosync)
            else:
                return None
        return self.collections[name]

    def _load(self):
        # TODO: Test if file exists
        try:
            file_db = self.serializer.load(self.filepath)
            if 'collections' in file_db:
                self.collections = {}
                for collection in file_db['collections']:
                    self.collections[collection] = LocalCollectionProxy(file_db['collections'][collection],
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
