
from local_collection_proxy import LocalCollectionProxy
import datetime
from threading import Lock
class EssentialLocal():
    def __init__(self,  filepath=None, collection=None, serializer=None, autosync=False):


        self.threading_lock = Lock()

        self.collections = {}
        self.filepath = filepath
        self.autosync = autosync
        if self.filepath is not None:
            with self.threading_lock:
                self._load()
                
            


    def get_collection(self,  name='default',  create=True):
        if name not in self.collections:
            self.collections[name]['documents'] = LocalCollectionProxy({},  self.threading_lock,  self.sync, self.autosync )
            self.collections[name]['indexes'] = {}
        return self.collections[name]['documents']
    
            
    def _load(self):
        # TODO: Test if file exists
        try:
            with open(self.filepath, "rb") as fp:
                file_db = self.serializer.load(fp)
                if 'collections' in file_db:
                    self.collections = file_db['collections']
                elif 'documents' in file_db:
                    #Handle db files created pre v0.5"
                    self.collections['default'] = file_db['documents']
                
        except:
            self.collections = {}

    def sync(self, filepath):
        output = {
            "meta": {
                "timestamp": datetime.datetime.now()
            },
            "collections": self.collections
        }
        self.serializer.dump(output, filepath)